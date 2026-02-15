"""Canonical-case, equation-driven 1D temperature integration (experimental)."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class CanonicalCaseConstants:
    # Sample-case constants from the 1D steady-state sample listing.
    tf: float = 530.0
    tvap: float = 820.0
    cfl: float = 0.7332
    hl: float = 212.628
    hv: float = 715.478
    zend: float = 0.25
    alpha1: float = 1.0e12
    alpha2: float = 1.0e11
    alpha3: float = 2.14e10
    agm: float = 2500.0
    bgm: float = 50000.0
    cgm: float = 33000.0


@dataclass(frozen=True)
class EquationModelConfig:
    points: int = 320
    z_liquid_target: float = 7.37459e-4
    z_lv_target: float = 7.5082274e-4
    t_end_target: float = 1905.3842
    cp_vapor: float = 0.7332


def _arrhenius(alpha: float, e_over_r: float, temp: float) -> float:
    return alpha * exp(-e_over_r / max(temp, 1.0))


def _integrate_region(
    z_start: float,
    z_end: float,
    y0: float,
    rhs,
    steps: int,
) -> Tuple[List[float], List[float]]:
    if steps < 2:
        raise ValueError("steps must be >= 2")

    dz = (z_end - z_start) / (steps - 1)
    zs = [z_start]
    ys = [y0]
    y = y0
    z = z_start

    for _ in range(steps - 1):
        k1 = rhs(z, y)
        y_trial = y + dz * k1
        k2 = rhs(z + dz, y_trial)
        y += 0.5 * dz * (k1 + k2)
        z += dz
        zs.append(z)
        ys.append(y)

    return zs, ys


def _solve_scale_for_target(
    rate_fn,
    y_start: float,
    y_target: float,
    z_start: float,
    z_end: float,
    steps: int,
) -> float:
    def terminal_error(scale: float) -> float:
        def rhs(_z: float, y: float) -> float:
            return scale * rate_fn(y)

        _, ys = _integrate_region(z_start, z_end, y_start, rhs, steps)
        return ys[-1] - y_target

    lo = 1e-20
    hi = 1.0
    err_lo = terminal_error(lo)
    err_hi = terminal_error(hi)

    while err_lo * err_hi > 0:
        hi *= 10.0
        err_hi = terminal_error(hi)
        if hi > 1e20:
            break

    for _ in range(80):
        mid = 0.5 * (lo + hi)
        err_mid = terminal_error(mid)
        if err_lo * err_mid <= 0:
            hi = mid
            err_hi = err_mid
        else:
            lo = mid
            err_lo = err_mid

    return 0.5 * (lo + hi)


def run_canonical_case_equation_profile(
    constants: CanonicalCaseConstants | None = None,
    config: EquationModelConfig | None = None,
) -> List[Dict[str, float]]:
    """Integrate a canonical-case 1D profile using equation-based region ODEs.

    Region model:
    - Liquid: dH/dz = K_liq * alpha1 * exp(-AGM/T(H))
    - Liquid-vapor: dH/dz = K_lv * alpha1 * exp(-AGM/Tvap)
    - Vapor: dH/dz = K_vap * (alpha3*exp(-CGM/T) - alpha2*exp(-BGM/T))

    K coefficients are solved by matching canonical transition/end targets.
    """

    c = constants or CanonicalCaseConstants()
    cfg = config or EquationModelConfig()

    # Choose region step allocations proportional to span.
    liquid_steps = max(32, cfg.points // 8)
    lv_steps = max(12, cfg.points // 20)
    vapor_steps = max(120, cfg.points - liquid_steps - lv_steps + 2)

    def liquid_temp_from_h(h: float) -> float:
        return c.tf + h / c.cfl

    liquid_rate = lambda h: _arrhenius(c.alpha1, c.agm, liquid_temp_from_h(h))
    k_liq = _solve_scale_for_target(
        rate_fn=liquid_rate,
        y_start=0.0,
        y_target=c.hl,
        z_start=0.0,
        z_end=cfg.z_liquid_target,
        steps=liquid_steps,
    )

    lv_rate = _arrhenius(c.alpha1, c.agm, c.tvap)
    k_lv = (c.hv - c.hl) / (max(cfg.z_lv_target - cfg.z_liquid_target, 1e-12) * max(lv_rate, 1e-30))

    def vapor_temp_from_h(h: float) -> float:
        return c.tvap + (h - c.hv) / cfg.cp_vapor

    vapor_rate = lambda h: max(
        1e-20,
        _arrhenius(c.alpha3, c.cgm, vapor_temp_from_h(h))
        - _arrhenius(c.alpha2, c.bgm, vapor_temp_from_h(h)),
    )

    # Target end enthalpy implied by canonical vapor end temperature.
    h_end_target = c.hv + cfg.cp_vapor * (cfg.t_end_target - c.tvap)
    k_vap = _solve_scale_for_target(
        rate_fn=vapor_rate,
        y_start=c.hv,
        y_target=h_end_target,
        z_start=cfg.z_lv_target,
        z_end=c.zend,
        steps=vapor_steps,
    )

    z_liq, h_liq = _integrate_region(
        0.0,
        cfg.z_liquid_target,
        0.0,
        lambda _z, h: k_liq * liquid_rate(h),
        liquid_steps,
    )
    z_lv, h_lv = _integrate_region(
        cfg.z_liquid_target,
        cfg.z_lv_target,
        c.hl,
        lambda _z, _h: k_lv * lv_rate,
        lv_steps,
    )
    z_vap, h_vap = _integrate_region(
        cfg.z_lv_target,
        c.zend,
        c.hv,
        lambda _z, h: k_vap * vapor_rate(h),
        vapor_steps,
    )

    # Stitch without duplicate boundary nodes.
    z_all = z_liq + z_lv[1:] + z_vap[1:]
    h_all = h_liq + h_lv[1:] + h_vap[1:]

    rows: List[Dict[str, float]] = []
    for z, h in zip(z_all, h_all):
        if h < c.hl:
            temp = liquid_temp_from_h(h)
            region = "liquid"
            wfv = 0.0
        elif h <= c.hv:
            temp = c.tvap
            region = "liquid_vapor"
            wfv = (h - c.hl) / max(c.hv - c.hl, 1e-12)
        else:
            temp = vapor_temp_from_h(h)
            region = "vapor"
            wfv = 1.0

        rows.append(
            {
                "Z": float(z),
                "TEMP": float(temp),
                "H": float(h),
                "WFV": float(min(max(wfv, 0.0), 1.0)),
                "region": region,
            }
        )

    return rows
