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


def _kcf(g: float, rho: float, mu: float, diff: float, ap: float) -> float:
    return (0.61 * g / max(rho, 1.0e-20)) * (
        max(mu / max(rho * diff, 1.0e-20), 1.0e-20) ** -0.667
    ) * (max(g / max(ap * mu, 1.0e-20), 1.0e-20) ** -0.41)


def _dp3f(temp: float, dif3: float, pressure: float) -> float:
    return 14.7 * dif3 / max(pressure, 1.0e-12) * (temp / 492.0) ** 1.823 * (
        1.0 - exp(-0.0672 * pressure * 492.0 / max(14.7 * temp, 1.0e-12))
    )


def _rhetf(cps: float, cpx: float, gamma: float, beta: float, k0: float, order: float) -> float:
    cpsi = max(cps, 1.0e-20)
    cpxi = max(cpx, 0.0)
    one_minus = 1.0 - cpxi / cpsi
    denom = 1.0 + beta * one_minus
    expo = 0.0 if abs(denom) <= 1.0e-12 else gamma * beta * one_minus / denom
    return k0 * cpsi ** (1.0 - order) * cpxi**order * exp(expo)


def _trapp(u: float, v: float, npart: int, x0a: float, cps: float, gamma: float, beta: float, k0: float) -> float:
    n = max(npart, 4)
    h = (v - u) / float(n)
    total = 0.0
    for i in range(n + 1):
        x = u + i * h
        cpx = ((x - x0a) / max(1.0 - x0a, 1.0e-12)) * cps
        cpx = min(max(cpx, 0.0), cps)
        rhet = _rhetf(cps, cpx, gamma, beta, k0, 1.0)
        val = x * x * rhet
        w = 0.5 if i in (0, n) else 1.0
        total += w * val
    return h * total


def sgrad_full_port(
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
    bgm: float,
    kp: float,
    alpha2: float,
    en3: float,
    max_iter: int = 50,
) -> tuple[float, float]:
    """Iterative SGRAD-style concentration/thermal gradient approximation."""

    t = max(temp, 1.0)
    p = max(pressure, 1.0e-6)
    rho = max(c1 + c2 + c3 + c4, 1.0e-12)
    mu = max(unbar("VISVST", t), 1.0e-20)
    cf1 = unbar("CFTBL1", t)
    cf2 = unbar("CFTBL2", t)
    cf3 = unbar("CFTBL3", t)
    cf4 = unbar("CFTBL4", t)
    cfbar = (c1 * cf1 + c2 * cf2 + c3 * cf3 + c4 * cf4) / rho
    hc = 0.74 * g * cfbar * (max(g / max(ap * mu, 1.0e-20), 1.0e-20) ** -0.41)

    di3 = dif3 * (14.7 / p) * (t / 492.0) ** 1.823
    di4 = dif4 * (14.7 / p) * (t / 492.0) ** 1.823
    kc3 = _kcf(g, rho, mu, di3, ap)
    kc4 = _kcf(g, rho, mu, di4, ap)

    cps = max(c3 / 2.0, 1.0e-12)
    cmcpn = max(c3 - cps, 1.0e-12)
    cmcpo = cmcpn
    tmtpn = 1.0
    tmtpo = 1.0
    tpsp = t
    tpspp = t
    dcpdx = 0.0
    dp3 = _dp3f(t, dif3, p)
    tps = t

    waf1 = 0.8
    while waf1 <= 0.95 + 1.0e-12:
        for _ in range(max_iter):
            dp3 = _dp3f(t, dif3, p)
            dcpdx = kc3 / max(dp3, 1.0e-20) * (c3 - cps)
            x0 = a - cps / max(dcpdx, 1.0e-20)

            h4 = unbar("H4TBL", t)
            h3_now = unbar("H3TBL", t)
            tps = t - (h4 * kc4 * c4 + h3_now * dp3 * dcpdx) / max(hc, 1.0e-20)
            tps = max(tps, 1.0)
            h3 = unbar("H3TBL", tps)
            dp3 = _dp3f(tps, dif3, p)
            gamma = bgm / max(tps, 1.0)
            beta = -cps * h3 * dp3 / max(kp * tps, 1.0e-20)
            k0 = alpha2 * exp(-gamma) * max(c1, 1.0e-20) ** en3

            if x0 < 0.0:
                x0 = 0.0
                cps = c3 / (1.0 + dp3 / max(a * kc3, 1.0e-20))
                dcpdx = c3 / max(a, 1.0e-20)
                tps = t - (h4 * kc4 * c4 + h3 * dp3 * dcpdx) / max(hc, 1.0e-20)
                tps = max(tps, 1.0)

            riesum = _trapp(0.0, 1.0, 50, x0 / max(a, 1.0e-20), cps, gamma, beta, k0)
            cps_prev = cps
            cmcpo = cmcpn
            cps = c3 - a * riesum / max(kc3, 1.0e-20)
            cps = max(cps, 0.0)
            cmcpn = max(c3 - cps, 1.0e-20)

            tmtpo = tmtpn
            tmtpn = max(t - tps, 1.0e-20)
            dtemp_rel = abs(tmtpo - tmtpn) / tmtpn
            dconc_rel = abs(cmcpo - cmcpn) / cmcpn
            if dtemp_rel < 0.05 and dconc_rel < 0.05:
                grad = dcpdx * dp3
                tgrad = hc * (t - tps)
                return grad, tgrad

            if min(tps, tpsp, tpspp) < tpsp < max(tps, tpsp, tpspp):
                tps = 0.5 * (tpsp + tpspp)
                h3 = unbar("H3TBL", tps)
                dp3 = _dp3f(tps, dif3, p)
                dcpdx = (hc * (t - tps) - h4 * kc4 * c4) / max(h3 * dp3, 1.0e-20)
                cps = max(c3 - dp3 / max(kc3, 1.0e-20) * dcpdx, 0.0)
            else:
                cps = 0.2 * cps + 0.8 * cps_prev

            tpspp = tpsp
            tpsp = tps

        waf1 += 0.05

    grad = dcpdx * dp3
    tgrad = hc * (t - tps)
    return grad, tgrad
