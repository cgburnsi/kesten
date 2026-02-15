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
    vapor_model: str = "reduced"

    # Reduced vapor-region kinetics tuned to match the observed
    # rise/peak/decline trend from the 1968 one-dimensional profile.
    vapor_activation: float = 13077.907651100442
    vapor_depletion_rate: float = 11777.751350803257
    vapor_heat_gain: float = 106169135.07324964
    vapor_cooling_rate: float = 959.2850962194299
    vapor_cooling_sink_temp: float = 1836.9793171757567
    vapor_progress_initial: float = 1.1451448000335862

    # Fortran-inspired vapor model parameters.
    wm1: float = 2.016
    wm2: float = 28.0134
    wm3: float = 17.031
    wm4: float = 32.045
    gas_constant: float = 10.7316
    pressure_init: float = 150.0
    mass_flux: float = 2.8
    feed_rate: float = 0.0
    hf: float = 0.0
    porosity: float = 0.42
    particle_radius: float = 0.010
    surface_area: float = 2500.0
    dif3: float = 1.8e-4
    dif4: float = 1.2e-4
    viscosity_ref: float = 1.8e-5
    viscosity_temp_exp: float = 0.70
    h4_reaction: float = -715.478
    h3_reaction: float = 980.0
    ammonia_rate_scale: float = 1.6
    heat_loss_coeff: float = 0.06
    heat_sink_temp: float = 1816.0
    cp1: float = 3.5
    cp2: float = 0.30
    cp3: float = 0.60
    cp4: float = 0.55


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
        else:
            lo = mid
            err_lo = err_mid

    return 0.5 * (lo + hi)


def _run_reduced_vapor_profile(
    constants: CanonicalCaseConstants,
    cfg: EquationModelConfig,
    vapor_steps: int,
) -> tuple[List[float], List[float], List[float]]:
    z_vap: List[float] = [cfg.z_lv_target]
    t_vap: List[float] = [constants.tvap]
    y_vap: List[float] = [cfg.vapor_progress_initial]
    dz_vap = (constants.zend - cfg.z_lv_target) / max(vapor_steps - 1, 1)
    z = cfg.z_lv_target
    temp = constants.tvap
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

    h_vap = [constants.hv + constants.cfl * (t - constants.tvap) for t in t_vap]
    return z_vap, t_vap, h_vap


def _concentrations_from_interface_state(
    temp: float,
    pressure: float,
    h: float,
    cfg: EquationModelConfig,
) -> tuple[float, float, float, float]:
    h4 = cfg.h4_reaction
    denom = h4 if abs(h4) > 1.0e-9 else -1.0e-9
    xv = -(h - cfg.hf) / denom
    xv = min(max(xv, 0.0), 1.0)
    denom2 = max(1.0 + xv, 1.0e-9)

    c4 = (pressure * cfg.wm4 / (cfg.gas_constant * temp)) * ((1.0 - xv) / denom2)
    c3 = (pressure * cfg.wm3 / (cfg.gas_constant * temp)) * (xv / denom2)
    c2 = (pressure * cfg.wm2 / (2.0 * cfg.gas_constant * temp)) * (xv / denom2)
    c1 = (pressure * cfg.wm1 / (2.0 * cfg.gas_constant * temp)) * (xv / denom2)
    return c1, c2, c3, c4


def _run_fortran_inspired_vapor_profile(
    constants: CanonicalCaseConstants,
    cfg: EquationModelConfig,
    vapor_steps: int,
) -> tuple[List[float], List[float], List[float]]:
    z = cfg.z_lv_target
    temp = constants.tvap
    h = constants.hv
    pressure = cfg.pressure_init
    c1, c2, c3, c4 = _concentrations_from_interface_state(temp, pressure, h, cfg)

    z_vap: List[float] = [z]
    t_vap: List[float] = [temp]
    h_vap: List[float] = [h]

    dz = (constants.zend - cfg.z_lv_target) / max(vapor_steps - 1, 1)
    for _ in range(vapor_steps - 1):
        temp_safe = max(temp, 1.0)
        pressure_safe = max(pressure, 1.0e-6)
        rho = max(c1 + c2 + c3 + c4, 1.0e-9)

        reciprocal_wm = c1 / cfg.wm1 + c2 / cfg.wm2 + c3 / cfg.wm3 + c4 / cfg.wm4
        wmav = rho / max(reciprocal_wm, 1.0e-12)

        dif4 = cfg.dif4 * (temp_safe / 492.0) ** 1.823 * (14.7 / pressure_safe)
        viscosity = cfg.viscosity_ref * (temp_safe / constants.tf) ** cfg.viscosity_temp_exp
        akc = (
            0.61
            * cfg.mass_flux
            / rho
            * (max(viscosity / max(rho * dif4, 1.0e-20), 1.0e-20) ** -0.667)
            * (max(cfg.mass_flux / max(cfg.surface_area * viscosity, 1.0e-20), 1.0e-20) ** -0.41)
        )

        t2 = cfg.porosity * constants.alpha3 * max(c4, 0.0) * exp(-constants.cgm / temp_safe)
        t4 = cfg.surface_area * akc * max(c4, 0.0)
        t3 = cfg.ammonia_rate_scale * constants.alpha2 * max(c3, 0.0) * exp(-constants.bgm / temp_safe)

        source4 = cfg.feed_rate - t2 - t4
        source3 = t2 * cfg.wm3 / cfg.wm4 + t4 * cfg.wm3 / cfg.wm4 - t3
        source2 = 0.5 * t2 * cfg.wm2 / cfg.wm4 + 0.5 * t4 * cfg.wm2 / cfg.wm4 + 0.5 * t3 * cfg.wm2 / cfg.wm3
        source1 = 0.5 * t2 * cfg.wm1 / cfg.wm4 + 0.5 * t4 * cfg.wm1 / cfg.wm4 + 1.5 * t3 * cfg.wm1 / cfg.wm3

        t1 = pressure_safe * wmav / (cfg.gas_constant * temp_safe * max(cfg.mass_flux, 1.0e-12))
        dc4_dz = t1 * source4
        dc3_dz = t1 * source3
        dc2_dz = t1 * source2
        dc1_dz = t1 * source1

        cp_mix = (c1 * cfg.cp1 + c2 * cfg.cp2 + c3 * cfg.cp3 + c4 * cfg.cp4) / max(rho, 1.0e-12)
        dh_dz = (
            -cfg.h4_reaction / cfg.mass_flux * (t2 + t4)
            - cfg.h3_reaction / cfg.mass_flux * t3
            - cfg.feed_rate / cfg.mass_flux * (h - cfg.hf)
        )
        dtemp_dz = dh_dz / max(cp_mix, 1.0e-9) - cfg.heat_loss_coeff * (temp - cfg.heat_sink_temp)

        dp_dz = (
            (cfg.porosity - 1.0)
            / max(cfg.porosity**3, 1.0e-12)
            * (1.75 + 75.0 * viscosity * (1.0 - cfg.porosity) / max(cfg.particle_radius * cfg.mass_flux, 1.0e-12))
            * cfg.mass_flux**2
            / (64.4 * max(cfg.particle_radius, 1.0e-12) * rho)
        )
        dp_dz /= 144.0

        c1 = max(0.0, c1 + dz * dc1_dz)
        c2 = max(0.0, c2 + dz * dc2_dz)
        c3 = max(0.0, c3 + dz * dc3_dz)
        c4 = max(0.0, c4 + dz * dc4_dz)
        h += dz * dh_dz
        temp += dz * dtemp_dz
        pressure = max(0.1, pressure + dz * dp_dz)
        z += dz

        z_vap.append(z)
        t_vap.append(temp)
        h_vap.append(h)

    return z_vap, t_vap, h_vap


def run_canonical_case_equation_profile(
    constants: CanonicalCaseConstants | None = None,
    config: EquationModelConfig | None = None,
) -> List[Dict[str, float]]:
    """Integrate a canonical-case 1D profile using equation-based region ODEs.

    Region model:
    - Liquid: enthalpy-based heating from Arrhenius source.
    - Liquid-vapor: isothermal phase-change bridge.
    - Vapor: reduced closure (default) or Fortran-inspired coupled balances.
    """

    c = constants or CanonicalCaseConstants()
    cfg = config or EquationModelConfig()

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

    if cfg.vapor_model == "reduced":
        z_vap, t_vap, h_vap = _run_reduced_vapor_profile(c, cfg, vapor_steps)
    elif cfg.vapor_model == "fortran_inspired":
        z_vap, t_vap, h_vap = _run_fortran_inspired_vapor_profile(c, cfg, vapor_steps)
    else:
        raise ValueError(f"Unsupported vapor model '{cfg.vapor_model}'")

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
        if z < cfg.z_liquid_target:
            region = "liquid"
            wfv = 0.0
        elif z <= cfg.z_lv_target:
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
