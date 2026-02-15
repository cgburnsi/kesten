# 4. Description of Subroutines

The following is a list and brief description of the subroutines which comprise the UNIVAC 1108 computer programs describing the one and two-dimensional steady-state models of a hydrazine catalytic reactor. Subroutine SGRAD, since it is the key subroutine in each program is described in detail. The flow charts for the main programs and major subroutines are included immediately after this list in Figs. I-l through I-8. The number outside of and next to any block on the flow charts indicates the approximate statement number in that routine at which that particular operation occurs.

## One-Dimensional Model
- **MAIN (Fig. I-1)**: Controls input and calculates concentrations and temperatures in the liquid region of the reactor.
- **SLOPE (Fig. I-1)**: Calculates concentration and temperature profiles within the catalyst particles for the liquid and liquid vapor regions of the reactor. This subroutine is similar to SGRAD which is described in detail later in this section.
- **LQVP (Fig. 1-2)**: Calculates enthalpy during the liquid vapor region of the reactor (concentration of N2H4 and temperature remain constant).
- **LQV2 (Fig. 1-2)**: Calculates hydrazine concentration, enthalpy and temperatures during the liquid-liquid vapor region of the reactor (concentration of hydrazine varies).
- **VAPOR (Figs. 1-3 \& 1-4)**: Calculates concentrations, temperatures and pressures in the vapor region of the reactor.
- **PARAM (Fig. 1-5)**: Calculates parameters needed for calculations done in subroutine SLOPE.
- **CONC (Fig. 1-5)**: Calculates reactant concentrations at the liquid vapor-vapor interface of the reactor.
- **UNBAR**: Interpolation routine used to obtain values from a table.
- **BLOCK DATA TABLES**: Tables of:
- temperature vs. viscosity
- temperature vs. vapor pressure
- temperature vs. heats of reaction
- temperature vs. specific heat
- vapor pressure vs. temperature
- enthalpy vs. temperature
- **SGRAD (Fig. 1-5)**: This routine is the same as it is in the two-dimensional model. For a detailed description, see the section describing two-dimensional subroutines.


## Two-Dimensional Model
- **MAIN (Fig. 1-6)**: Controls input and calculates concentrations and temperatures in the liquid region of the reactor for all annular regions.
- **SLOPE (Fig. 1-6)**: Calculates concentration and temperature profiles within the catalyst particles for the liquid and liquid vapor regions of the reactor for all annular regions. This subroutine is similar to SGRAD which is described in detail later in this section.
- **LQVP (Fig. 1-6)**: Calculates enthalpy during the liquid vapor region of the reactor for all annular regions (concentration of $N_{2}H_{4}$ and temperature remain constant).
- **VAPOR (Fig. 1-7)**: Calculates concentrations, temperatures and pressures in the vapor region of the reactor for all annular regions.
- **DELTAZ (Fig. 1-8)**: Calculates axial increments for the vapor region.
- **ORDER (Fig. 1-8)**: Arranges an array of numbers in ascending order.
- **UNBAR**: Interpolation routine used to obtain values from a table.
- **BLOCK DATA TABLES**: Tables of:
- temperature vs. viscosity
- temperature vs. vapor pressure
- temperature vs. heats of reaction
- temperature vs. specific heat
- vapor pressure vs. temperature
- enthalpy vs. temperature
- **SGRAD (Fig. 1-8)**: Detailed description follows:


## SGRAD (Fig. 1-8)
The purpose of subroutine SGRAD is to solve the implicit integral equations describing reactant concentration and temperature profiles in the porous catalyst particles and to calculate the slope of the reactant concentration gradient at the surface of the catalyst particles. This routine is used for calculations in the vapor region of the reactor only. In the hydrazine catalytic reactor system, ammonia concentration profiles are calculated but the subroutine is very general and can be used for many other reactants. The key equation to be solved is an implicit integral equation of the form (Refs. 2 and 9):

$$ 

c_{p}^{NH_{3}}(x/a) = c_{i}^{NH_{3}} - a^{2}\left[\frac{1}{x/a} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right]\int_{x_{0}/a}^{x/a} \xi^{2} \frac{r_{het}^{NH_{3}}[c_{p}^{NH_{3}}(x/a)]}{D_{p}^{NH_{3}}} d\xi \\
- a^{2}\int_{x/a}^{1}\left[\frac{1}{\xi} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right]\xi^{2} \frac{r_{het}^{NH_{3}}[c_{p}^{NH_{3}}(x/a)]}{D_{p}^{NH_{3}}} d\xi

$$

where $c_{p}^{NH_{3}}(x)$ is the reactant (ammonia) concentration as a function of x (the radial position within the catalyst particle), $c_{i}^{NH_{3}}$ is the interstitial reactant concentration and $a$ is the radius of the spherical catalyst particle. To solve this equation, a two-phase iterative scheme is used. First, an initial estimate for $c_{p}^{NH_{3}}(x)$ is found through an iterative method of calculating successively better approximations. Second, using the good initial estimate found in the first phase, a similar iterative method is used to arrive at converged values of the actual $c_{p}^{NH_{3}}(x)$ distribution.

### Phase I
It was found through hand calculation that solutions of Eq. (eq:I-1) were very likely to diverge if the initial estimate was not a very good estimate. Therefore, in the first phase of this subroutine the iterative scheme is used to find this good first estimate. A linear function of the type shown in Fig. I-9 was found to be a fairly close approximation to the actual concentration distribution. The point at which the reactant concentration profile changes slope is referred to as $x_{0}$.


> [Figure/flowchart block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]


The final solution to Phase I is a distribution of this type.

#### Iterative Procedure: Phase I
- First a guess is made at a value for the reactant concentration at the surface of the catalyst particle: $(c_{p})_{s}^{NH_{3}} = c_{i}^{NH_{3}} / 2$.
- Using this value, a value is found for the slope of the concentration profile at the surface, $[dc_{p}^{NH_{3}}/dx]_{x=a}$.
$$ 
\left[\frac{dC_{p}^{NH_{3}}}{dx}\right]_{x=a} = \frac{k_{c}^{NH_{3}}}{D_{p}^{NH_{3}}}\left[c_{i}-(c_{p})_{s}\right]^{NH_{3}}
$$
where $k_{c}^{NH_{3}}$ is calculated from an equation given in Ref. 1 and $D_{p}^{NH_{3}}$ is calculated from Eq. (eq:I-3).
$$ 
D_{p}^{NH_{3}} = D_{0}^{NH_{3}}\left\{\left(\frac{(T_{p})_{s}}{492}\right)^{1.823} \cdot \left(\frac{14.7}{P}\right) \cdot \left[1-e^{-0.0672(P/14.7)(492/(T_p)_{s})}\right]\right\}
$$
- The temperature at the particle surface, $(T_{p})_{s}$, is calculated from
$$ 
(T_{p})_{s} = T_{i} - \frac{1}{h_{c}}\left[(H \cdot k_{c} \cdot c_{i})^{N_{2}H_{4}} + (H \cdot D_{p} \cdot [dc_{p}/dx]_{x=a})^{NH_{3}}\right]
$$
where $T_{i}$ and $c_{i}^{N_{2}H_{4}}$ are input to the subroutine, $H^{N_{2}H_{4}}$ and $H^{NH_{3}}$ are taken from tables in the computer program, and $h_{c}$ and $k_{c}^{N_{2}H_{4}}$ are calculated according to the equations in Ref. 1.
- Using the point $[a, (c_{p})_{s}^{NH_{3}}]$ and the slope $[dc_{p}^{NH_{3}}/dx]_{x=a}$, a line is established and extrapolated to the $c_{p}^{NH_{3}} = 0$ axis, intersecting the line at $x_{0}$ (as in Fig. I-9).
- The value for $x_{0}$ is calculated from
$$ 
x_{0} = a - \left\{ \frac{(c_{p})_{s}}{[dc_{p}/dx]_{x=a}} \right\}^{NH_{3}}
$$
Since the region of primary interest is the particle surface, it is at this point that convergence on a value for $c_{p}^{NH_{3}}(x)$ is tested. To test for convergence, a new $(c_{p})_{s}^{NH_{3}}$ is calculated and compared to the previous $(c_{p})_{s}^{NH_{3}}$. The new value for $(c_{p})_{s}^{NH_{3}}$ can be calculated from Eq. (eq:I-1) by noting that, at the catalyst particle surface, where $x=a$, the second integral term in Eq. (eq:I-1) drops out leaving
$$ 
(c_{p})_{s}^{NH_{3}} = c_{i}^{NH_{3}} - \left[\frac{1}{X} - \frac{ak_{c}-D_{p}^{NH_{3}}}{a^{2}k_{c}^{NH_{3}}}\right]\int_{0}^{a} \xi^{2} \frac{r_{het}[c_{p}^{NH_{3}}(x)]}{D_{p}^{NH_{3}}} d\xi
$$
As can be seen in Fig. (I-9) in distributions of this type all values of $c_{p}^{NH_{3}}(x)$ between 0 and $x_{0}$ are zero. Therefore, in evaluating the integrals, all points between 0 and $x_{0}$ can be ignored. If this is done and if $x$ is normalized by dividing by $a$, Eq. (eq:I-6) reduces to
$$ 
(c_{p})_{s}^{NH_{3}} = c_{i}^{NH_{3}} - a^{2}\left[1 - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right]\int_{x_{0}/a}^{1} \xi^{2} \frac{r_{het}[c_{p}^{NH_{3}}(x)]}{D_{p}^{NH_{3}}} d\xi
$$
where all terms have been previously determined except $r_{het}$ which is calculated from
$$ 
r_{het}^{NH_{3}} = k_{0}(c_{i}^{NH_{3}})^{1-n} \cdot [c_{p}^{NH_{3}}(x)]^{n} \exp \left\{ \frac{\gamma\beta(1 - c_{p}^{NH_{3}}(x) / c_{i}^{NH_{3}})}{[1 + \beta(1 - c_{p}^{NH_{3}}(x) / c_{i}^{NH_{3}})]} \right\}
$$
where n, $k_{0}$, $\gamma$, and $\beta$ are defined in the List of Symbols.
- A new value for $(c_{p})_{s}^{NH_{3}}$ is calculated using Eq. (eq:I-7) where the integral is evaluated numerically using the trapezoidal method.
- A new value for $[dc_{p}^{NH_{3}}/dx]_{x=a}$ is calculated from Eq. (eq:I-2) using the newly calculated $(c_{p})_{s}^{NH_{3}}$.
- New values are calculated for $(T_{p})_{s}$, $D_{p}^{NH_{3}}$, $\gamma$, $\beta$, $k_{0}$.
- The following convergence tests are made:
$$ 
\left| \frac{[T_{i}-(T_{p})_{s}]_{OLD} - [T_{i}-(T_{p})_{s}]_{NEW}}{[T_{i}-(T_{p})_{s}]_{NEW}} \right| \le 0.05
$$
and
$$ 
\left| \frac{[c_{i}-(c_{p})_{s}]_{OLD}^{NH_{3}} - [c_{i}-(c_{p})_{s}]_{NEW}^{NH_{3}}}{[c_{i}-(c_{p})_{s}]_{NEW}^{NH_{3}}} \right| \le 0.05
$$
If these tests are both satisfied, the value of $x_{0}$ calculated in Eq. (eq:I-5) is saved and the program moves on to Phase II. 

If both tests are not satisfied, an averaged value of $(c_{p})_{s}^{NH_{3}}$ is calculated using as many as three averaging techniques to insure rapid convergence. Using this new value of $(c_{p})_{s}^{NH_{3}}$, steps 2 through 9 are repeated up to a maximum of twenty-five times. If no convergence is reached after twenty-five iterations, a "weighted" estimate of $x_{0}$ is tried:
$$ 
x_{0} = f_{i} (x_{0})_{\text{previously calculated}} + (1-f_{i}) (x_{0})_{\text{last calculated}}
$$
Steps 1 through 9 are repeated up to twenty-five times. Succeeding values $f_{i} = 0.80, 0.85, 0.90, \text{and } 0.95$ are tried until convergence is reached. If convergence still is not reached and therefore a satisfactory $x_{0}$ is not found, a program termination with an appropriate error message follows.


### Phase II
Using as an initial approximation the straight line determined by the convergent $x_{0}$ and $[dc_{p}^{NH_{3}}/dx]_{x=a}$ found in Phase I, an iterative scheme similar to that in Phase I is now employed to find convergent values for the entire $c_{p}^{NH_{3}}(x)$ distribution within the catalyst particle. It was found through hand calculations that the convergent values of $c_{p}^{NH_{3}}(x)$ near the surface were not changed by more than 5 percent when the values of $c_{p}^{NH_{3}}(x)$ between 0 and $x_{0}$ were not considered in the iterative procedure. Therefore, the points in this range are ignored.

#### Iterative Procedure: Phase II
The values of $c_{p}^{NH_{3}}(x)$, $(T_{p})_{s}$, $k_{o}^{NH_{3}}$, $\beta^{NH_{3}}$, $\gamma^{NH_{3}}$, etc. found in the last iteration in Phase I are the initial input to the following iteration.
- A new $c_{p}^{NH_{3}}(x)$ profile is calculated from Eq. (eq:I-12).
$$ 

c_{p}^{NH_{3}}(x/a) = c_{i}^{NH_{3}} - a^{2}\left[\frac{1}{x/a} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right]\int_{x_{0}/a}^{x/a} \xi^{2} \frac{r_{het}^{NH_{3}}[c_{p}^{NH_{3}}(x/a)]}{D_{p}^{NH_{3}}} d\xi \\
- a^{2}\int_{x/a}^{1}\left[\frac{1}{\xi} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right]\xi^{2} \frac{r_{het}^{NH_{3}}[c_{p}^{NH_{3}}(x/a)]}{D_{p}^{NH_{3}}} d\xi

$$
As before, the limits of the integral have been normalized by dividing by $a$. The integrals are evaluated numerically using the finite sum approximation described below.

To evaluate the integral terms in Eq. (eq:I-12) the following procedure, using a finite sum approximation, is used:
- **(a)**: the interval $x_{0}/a \le x/a \le 1$ is divided into 24 equally spaced subdivisions, and an average value for $r_{het}[c_{p}^{NH_{3}}(x/a)]$ is calculated for each of these divisions.
- **(b)**: treating $r_{het}[c_{p}^{NH_{3}}(x/a)]$ as constant over each of these subdivisions, Eq. (eq:I-12) can be approximated by
$$ 

C_{p}^{NH_{3}}(x/a) = c_{i}^{NH_{3}} - \frac{a}{D_{p}^{NH_{3}}} \left[\frac{1}{x/a} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right] \left\{ r_{het}^{1} \int_{x_{0}/a}^{x_{0}/a+\Delta x/a} \xi d\xi \right. \\
+ r_{het}^{2} \int_{x_{0}/a+\Delta x/a}^{x_{0}/a+2\Delta x/a} \xi d\xi + \dots + \left. r_{het}^{24} \int_{x_{0}/a+(k-1)\Delta x/a}^{x_{0}/a+k\Delta x/a} \xi d\xi \right\} \\
- \frac{a^{2}}{D_{p}^{NH_{3}}} \left\{ r_{het}^{1} \int_{x_{0}/a+k\Delta x/a}^{x_{0}/a+(k+1)\Delta x/a} \left[\frac{1}{\xi} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right] \xi^{2} d\xi \right. \\
+ r_{het}^{2} \int_{x_{0}/a+(k+1)\Delta x/a}^{x_{0}/a+(k+2)\Delta x/a} \left[\frac{1}{\xi} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right] \xi^{2} d\xi + \dots \\
+ \left. r_{het}^{24} \int_{x_{0}/a+23\Delta x/a}^{x_{0}/a+24\Delta x/a} \left[\frac{1}{\xi} - \frac{ak_{c}^{NH_{3}}-D_{p}^{NH_{3}}}{ak_{c}^{NH_{3}}}\right] \xi^{2} d\xi \right\}

$$
where $k = 1, 2, ..., 24$
- **(c)**: the integrals in Eq. (eq:I-13) can now be evaluated directly viz
$$ \int_{a}^{b} \xi d\xi = \frac{\xi^{2}}{2}\bigg|_{a}^{b} = \frac{b^{2}}{2} - \frac{a^{2}}{2} $$
$$ \int_{a}^{b} \text{constant} \cdot \xi^{2} d\xi = \text{constant} \cdot \frac{\xi^{3}}{3}\bigg|_{a}^{b} = \text{constant} \cdot \left(\frac{b^{3}}{3} - \frac{a^{3}}{3}\right) $$
- **(d)**: rearranging and integrating term by term in Eq. (eq:I-13) yields the finite sum approximation for $c_{p}^{NH_{3}}(x/a)$ at each subdivision of the interval from $x_{0}/a$ to 1:
$$ 

C_{p}^{NH_{3}}(x/a)_{k+1} = C_{i}^{NH_{3}} - \frac{a^{2}}{D_{p}^{NH_{3}}} \left\{ \left(\frac{1}{x_{k}/a} - \frac{av+1}{av}\right) \right. \\
\sum_{j=1}^{k} \frac{r_{het}^{j}}{3} \left[ \left(\frac{x_{j}}{a}\right)^{3} - \left(\frac{x_{j-1}}{a}\right)^{3} \right] + \sum_{j=k}^{24} \frac{r_{het}^{j+1}}{2} \left[ \left(\frac{x_{j+1}}{a}\right)^{2} - \left(\frac{x_{j}}{a}\right)^{2} \right] \\
- \left. \left(\frac{av+1}{av}\right) \sum_{j=k}^{24} \frac{r_{het}^{j+1}}{3} \left[ \left(\frac{x_{j+1}}{a}\right)^{3} - \left(\frac{x_{j}}{a}\right)^{3} \right] \right\}

$$
where $v = (ak_{c} - D_{p})^{NH_{3}} / ak_{c}^{NH_{3}}$ and $k = 1, 2, ..., 24$.
- **(e)**: the values for $c_{p}^{NH_{3}}(x/a)|_{x=x_{0}}$ and $c_{p}^{NH_{3}}(x/a)|_{x=a}$ are special cases where one or the other of the integral terms in Eq. (eq:I-12) vanishes. Evaluation follows from a simple reduction of Eq. (eq:I-14).
- A new value for $[dc_{p}^{NH_{3}}/dx]_{x=a}$ is calculated from Eq. (eq:I-2) using the newly calculated $(c_{p})_{s}^{NH_{3}}$.
- A new value for $(T_{p})_{s}$ is calculated from Eq. (eq:I-4).
- Convergence tests are made (as they were in Phase I) using Eqs. (eq:I-9) and (eq:I-10).
- **(a)**: If the convergence tests are both satisfied, the quantities GRAD and TGRAD are calculated according to Eqs. (eq:I-15) and (eq:I-16), and the program returns to the point from which the subroutine was called.
$$ 
GRAD = [dC_{p}^{NH_{3}}/dx]_{x=a} \cdot D_{p}^{NH_{3}}
$$
$$ 
TGRAD = h_{c}[T_{i}-(T_{p})_{s}]
$$
- **(b)**: If the tests are not both satisfied, a new $c_{p}^{NH_{3}}(x)$ distribution is calculated using one of various averaging techniques. Corresponding $[dc_{p}^{NH_{3}}/dx]_{x=a}$, $(T_{p})_{s}$, $x_{0}$, $\gamma$, $\beta$, etc. are also calculated. Then steps 1 through 4 are repeated up to a maximum of 50 times. If convergence criteria are not met after 50 iterations, approximations to acceptable values of GRAD and TGRAD are made using the results of the Phase I iterative procedure, an appropriate message is printed, and the program returns to the point from which the subroutine was called.


Distributions of the type shown in Fig. (I-10) are typical of those found in this iterative procedure.


> [Figure/flowchart block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]

- **(1)**: converged linear approximation from Phase I
- **(2)**: curve calculated from curve (1) using Eq. (I-11) (Phase II, step 1)
- **(3)**: averaged curve calculated from curves (1) and (2) (Phase II, step 4b)


> [Figure/flowchart block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]


> [Figure/flowchart block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]


> [Figure/flowchart block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]


## Appendix II: Listing of Computer Programs

## One-Dimensional Steady-State Model


> [Fortran listing block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 4.]


> [Appendix listing source include omitted in milestone-1 markdown. See `docs/latex/app-NASA9.tex`]


## Conversion Notes

- This major section is converted for milestone 1 using the maintained LaTeX transcription source.
- Figure, flowchart, and listing blocks were collapsed to placeholders for readability; detailed fidelity review remains.
- QA outcome: checklist is partially satisfied; section is not yet `reviewed` because figure/listing completeness checks are still open.
- Section status is `converted` pending full QA checklist sign-off.

## References

[1] Placeholder (report reference used in subroutine equations).
[2] Placeholder.
[9] Placeholder.
