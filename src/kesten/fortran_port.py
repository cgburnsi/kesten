"""Direct ports of selected legacy FORTRAN helper routines."""

from __future__ import annotations

from math import exp
from typing import List, Tuple

from .property_tables import unbar


def conc_port(
    temp: float,
    pressure: float,
    wm4: float,
    wm3: float,
    wm2: float,
    wm1: float,
    gas_constant: float,
    h: float,
    hf: float,
) -> tuple[float, float, float, float]:
    """Port of CONC.f style vapor-interface concentration initialization."""

    h4 = unbar("TBLH4", temp)
    xv = -(h - hf) / max(abs(h4), 1.0e-12)
    xv = min(max(xv, 0.0), 1.0)
    denom = max(1.0 + xv, 1.0e-12)

    c4 = (pressure * wm4) / (gas_constant * temp) * ((1.0 - xv) / denom)
    c3 = (pressure * wm3) / (gas_constant * temp) * (xv / denom)
    c2 = (pressure * wm2) / (2.0 * gas_constant * temp) * (xv / denom)
    c1 = (pressure * wm1) / (2.0 * gas_constant * temp) * (xv / denom)
    return c1, c2, c3, c4


def param_port(
    temp: float,
    z: float,
    cc: float,
    hr: float,
    lvop: int,
    z0: float,
    g0: float,
    fc: float,
    gatz0: float,
    agm: float,
    bgm: float,
    alpha1: float,
    alpha2: float,
    dif3: float,
    dif4: float,
    pressure: float,
    kp: float,
    c1: float,
) -> tuple[float, float, float, float, float]:
    """Port of PARAM.f for G, rate prefactor, and diffusivity terms."""

    if (z - z0) < 0.0:
        g = g0 + fc * z
    else:
        g = gatz0

    if lvop == 1:
        gmma = bgm / max(temp, 1.0)
        k = alpha2 * exp(-gmma) / max(c1, 1.0e-12) ** 1.6
        dp = dif3 * (temp / 492.0) ** 1.832 * (14.7 / pressure) * (
            1.0 - exp(-0.0672 * (pressure * 492.0) / (14.7 * temp))
        )
    else:
        gmma = agm / max(temp, 1.0)
        k = alpha1 * exp(-gmma)
        dp = dif4 * (temp / 492.0) ** 1.832 * (14.7 / pressure) * (
            1.0 - exp(-0.0672 * (pressure * 492.0) / (14.7 * temp))
        )

    # Keep the early-port form; this is a known uncertain term.
    beta = -(cc * hr * dp) / max(kp * temp, 1.0e-12)
    return g, gmma, k, beta, dp


def lqvp_port(
    h_start: float,
    z_start: float,
    deriv_start: float,
    dhdz_start: float,
    temp_vap: float,
    hl: float,
    hv: float,
    enmx2: float,
    max_steps: int,
    z0: float,
    g0: float,
    fc: float,
    gatz0: float,
    agm: float,
    bgm: float,
    alpha1: float,
    alpha2: float,
    dif3: float,
    dif4: float,
    pressure: float,
    kp: float,
    c1: float,
) -> Tuple[List[float], List[float], List[float], float]:
    """Port of LQVP stepping logic for the liquid-vapor bridge."""

    z_values: List[float] = [z_start]
    h_values: List[float] = [h_start]
    wfv_values: List[float] = [max(0.0, min(1.0, (h_start - hl) / max(hv - hl, 1.0e-12)))]
    deriv = deriv_start
    dhdz = dhdz_start
    h = h_start
    z = z_start

    for _ in range(max_steps):
        h4 = unbar("TBLH4", temp_vap)
        ap = unbar("ZTBLAP", z)

        g, _gmma, _k, _beta, dpa = param_port(
            temp=temp_vap,
            z=z,
            cc=0.0,
            hr=0.0,
            lvop=0,
            z0=z0,
            g0=g0,
            fc=fc,
            gatz0=gatz0,
            agm=agm,
            bgm=bgm,
            alpha1=alpha1,
            alpha2=alpha2,
            dif3=dif3,
            dif4=dif4,
            pressure=pressure,
            kp=kp,
            c1=c1,
        )

        dhdz = -(h4 * dpa * ap * deriv + fc * (h - 0.0)) / max(g, 1.0e-12)
        if abs(dhdz) <= 1.0e-18:
            break

        dz = -h4 / max(enmx2 * dhdz, 1.0e-18)
        h_new = h + dhdz * dz

        if h_new >= hv:
            dz = (hv - h) / max(dhdz, 1.0e-18)
            h = hv
            z = z + dz
            z_values.append(z)
            h_values.append(h)
            wfv_values.append(1.0)
            break

        h = h_new
        z = z + dz
        wfv = max(0.0, min(1.0, (h - hl) / max(hv - hl, 1.0e-12)))
        z_values.append(z)
        h_values.append(h)
        wfv_values.append(wfv)

        if h >= hv:
            break

    return z_values, h_values, wfv_values, dhdz


def sgrad_approx_port(
    temp: float,
    pressure: float,
    g: float,
    c1: float,
    c2: float,
    c3: float,
    c4: float,
    dif3: float,
    dif4: float,
    a: float,
    ap: float,
    kp: float,
) -> tuple[float, float]:
    """Compact approximation to SGRAD-derived gradients from early port equations."""

    rho = max(c1 + c2 + c3 + c4, 1.0e-12)
    mu = max(unbar("VISVST", temp), 1.0e-20)
    cf1 = unbar("CFTBL1", temp)
    cf2 = unbar("CFTBL2", temp)
    cf3 = unbar("CFTBL3", temp)
    cf4 = unbar("CFTBL4", temp)
    cfbar = (c1 * cf1 + c2 * cf2 + c3 * cf3 + c4 * cf4) / rho
    hc = 0.74 * g * cfbar * (max(g / max(ap * mu, 1.0e-20), 1.0e-20) ** -0.41)

    di3 = dif3 * (14.7 / pressure) * (temp / 492.0) ** 1.823
    di4 = dif4 * (14.7 / pressure) * (temp / 492.0) ** 1.823

    kc3 = (0.61 * g / rho) * (max(mu / max(rho * di3, 1.0e-20), 1.0e-20) ** -0.667) * (
        max(g / max(ap * mu, 1.0e-20), 1.0e-20) ** -0.41
    )
    kc4 = (0.61 * g / rho) * (max(mu / max(rho * di4, 1.0e-20), 1.0e-20) ** -0.667) * (
        max(g / max(ap * mu, 1.0e-20), 1.0e-20) ** -0.41
    )

    dp3 = 14.7 * dif3 / pressure * (temp / 492.0) ** 1.823 * (
        1.0 - exp(-0.0672 * pressure * 492.0 / (14.7 * temp))
    )
    cps = c3 / (1.0 + dp3 / max(a * kc3, 1.0e-20))
    dcpdx = kc3 / max(dp3, 1.0e-20) * (c3 - cps)
    grad = dcpdx * dp3

    h4 = unbar("H4TBL", temp)
    h3 = unbar("H3TBL", temp)
    tps = temp - (h4 * kc4 * c4 + h3 * dp3 * dcpdx) / max(hc, 1.0e-20)
    tgrad = hc * (temp - tps)
    return grad, tgrad
