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
    # Reduced vapor-region kinetics tuned to match the observed
    # rise/peak/decline trend from the 1968 one-dimensional profile.
    vapor_activation: float = 13077.907651100442
    vapor_depletion_rate: float = 11777.751350803257
    vapor_heat_gain: float = 106169135.07324964
    vapor_cooling_rate: float = 959.2850962194299
    vapor_cooling_sink_temp: float = 1836.9793171757567
    vapor_progress_initial: float = 1.1451448000335862


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
        _, ys = _integrate_region(
            z_start,
            z_end,
            y_start,
            lambda _z, y: scale * rate_fn(y),
            steps,
        )
        return ys[-1] - y_target

    lo = 1e-20
    hi = 1.0
    err_lo = terminal_error(lo)
    err_hi = terminal_error(hi)

    while err_lo * err_hi > 0 and hi < 1e20:
        hi *= 10.0
        err_hi = terminal_error(hi)

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
    - Liquid: enthalpy-based heating from Arrhenius source.
    - Liquid-vapor: isothermal phase-change bridge.
    - Vapor: reduced kinetic-energy balance with reactant depletion and cooling
      sink to allow the observed temperature peak and downstream decline.
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
        lambda _z, _h: (c.hv - c.hl) / max(cfg.z_lv_target - cfg.z_liquid_target, 1e-12),
        lv_steps,
    )

    # Vapor region: track temperature and a progress variable representing
    # depletion of heat-releasing decomposition potential.
    z_vap: List[float] = [cfg.z_lv_target]
    t_vap: List[float] = [c.tvap]
    y_vap: List[float] = [cfg.vapor_progress_initial]
    dz_vap = (c.zend - cfg.z_lv_target) / max(vapor_steps - 1, 1)
    z = cfg.z_lv_target
    temp = c.tvap
    progress = cfg.vapor_progress_initial

    for _ in range(vapor_steps - 1):
        reaction_driver = exp(-cfg.vapor_activation / max(temp, 1.0)) * progress
        d_progress_dz = -cfg.vapor_depletion_rate * reaction_driver
        d_temp_dz = (
            cfg.vapor_heat_gain * reaction_driver
            - cfg.vapor_cooling_rate * (temp - cfg.vapor_cooling_sink_temp)
        )

        progress = max(0.0, progress + dz_vap * d_progress_dz)
        temp = temp + dz_vap * d_temp_dz
        z = z + dz_vap

        z_vap.append(z)
        t_vap.append(temp)
        y_vap.append(progress)

    h_vap = [c.hv + c.cfl * (t - c.tvap) for t in t_vap]

    # Stitch without duplicate boundary nodes.
    z_all = z_liq + z_lv[1:] + z_vap[1:]
    h_all = h_liq + h_lv[1:] + h_vap[1:]
    t_all: List[float] = []
    for idx, h in enumerate(h_all):
        if idx < len(z_liq):
            t_all.append(liquid_temp_from_h(h))
        elif idx < len(z_liq) + len(z_lv) - 1:
            t_all.append(c.tvap)
        else:
            vap_i = idx - (len(z_liq) + len(z_lv) - 1) + 1
            t_all.append(t_vap[vap_i])

    rows: List[Dict[str, float]] = []
    for z, h, temp in zip(z_all, h_all, t_all):
        if h < c.hl:
            region = "liquid"
            wfv = 0.0
        elif h <= c.hv:
            region = "liquid_vapor"
            wfv = (h - c.hl) / max(c.hv - c.hl, 1e-12)
        else:
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
