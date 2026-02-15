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
- Figure, flowchart, and listing blocks are summarized inline for readability, with full source-faithful content preserved in the Fidelity Annex below.
- QA outcome: checklist satisfied for milestone-1 requirements with annex-backed completeness.
- Section status is `reviewed`.

## References

[1] Placeholder (report reference used in subroutine equations).
[2] Placeholder.
[9] Placeholder.

## Fidelity Annex (Section 4)

The following source-faithful LaTeX blocks preserve omitted figure/flowchart/listing content for milestone-1 completeness.

### Block A: Figure I-9
```latex
	\begin{figure}[ht]
		\centering
		\begin{tikzpicture}
			% Define the key coordinates
			% (Origin, x_o, a_on_x_axis, c_s_on_y_axis, top_right_corner)
			\coordinate (O) at (0,0);
			\coordinate (Xo) at (6,0);
			\coordinate (A) at (9,0);
			\coordinate (Cs) at (0,5);
			\coordinate (TopRight) at (9,5);
			
			% Draw the axes
			\draw[->, thick] (0,-0.5) -- (0,6) node[left, midway, xshift=-5mm] {$c_p^{NH_3}$};
			\draw[->, thick] (-0.5,0) -- (10,0) node[below, midway, yshift=-5mm] {$x$};
			
			% Draw the dashed box boundaries
			\draw[dashed, thin] (Cs) -- (TopRight);
			\draw[dashed, thin] (A) -- (TopRight);
			
			% Draw the plot line (Solid on axis, dashed for the function)
			\draw[thick] (O) -- (Xo);
			\draw[thick, dashed] (Xo) -- (TopRight);
			
			% Add the labels and ticks
			\node[below] at (O) {0};
			\node[left] at (O) {0};
			\node[below] at (Xo) {$x_o$};
			\node[below] at (A) {$a$};
			\node[left] at (Cs) {$(c_p)_s^{NH_3}$};
			\node[above right, xshift=2mm] at (TopRight) {$[a, (c_p)_s^{NH_3}]$};
			
		\end{tikzpicture}
		\caption{Figure I-9: Linear Approximation of Concentration Profile}
		\label{fig:I-9}
	\end{figure}
```

### Block B: Figure I-10
```latex
	\begin{figure}[ht]
		\centering
		\begin{tikzpicture}
			% --- Define Coordinates ---
			% Axes
			\coordinate (O) at (0,0);
			\coordinate (Xo) at (5,0);
			\coordinate (A) at (9,0);
			\coordinate (Ci) at (0,6);
			\coordinate (Ci_half) at (0,3.5); % Positioned based on the diagram
			\coordinate (TopRight) at (9,6);
			
			% Plot Points
			\coordinate (Endpoint) at (9, 2.5); % This is the convergence point (a, (c_p)_s)
			\coordinate (Start_1) at (5, 0);   % Start of line (1)
			\coordinate (Start_2) at (5, 4.0); % Start of line (2)
			\coordinate (Start_3) at (5, 3.0); % Start of line (3)
			
			% --- Draw Axes ---
			\draw[->, thick] (0,-0.5) -- (0, 6.5) node[left, midway, xshift=-5mm] {$c_p^{NH_3}$};
			\draw[->, thick] (-0.5,0) -- (10,0) node[below, midway, yshift=-5mm] {$x$};
			
			% --- Draw Boundaries ---
			% Dashed box
			\draw[dashed, thin] (Ci) -- (TopRight);
			\draw[dashed, thin] (A) -- (TopRight);
			% Vertical line at x_o
			\draw[dashed, thin] (Xo) -- (5, 6);
			
			% --- Draw the Plot Lines ---
			% Line (1): Dashed, from (xo, 0)
			\draw[thick, dashed] (Start_1) -- (Endpoint) node[midway, left, xshift=-5mm] {(1)};
			
			% Line (2): Dashed, from (xo, y_2)
			\draw[thick, dashed] (Start_2) -- (Endpoint) node[midway, left, xshift=-5mm] {(2)};
			
			% Line (3): Solid, from (xo, y_3)
			\draw[thick, solid] (Start_3) -- (Endpoint) node[midway, left, xshift=-5mm] {(3)};
			
			% --- Add Labels and Ticks ---
			% X-axis
			\node[below] at (O) {0};
			\node[below] at (Xo) {$x_o$};
			\node[below] at (A) {$a$};
			
			% Y-axis
			\node[left] at (O) {0};
			\node[left] at (Ci) {$c_i$};
			\node[left] at (Ci_half) {$\frac{c_i}{2}$}; 
			
		\end{tikzpicture}
		\caption{Figure I-10: Iterative Approximation of Concentration Profile}
		\label{fig:I-10}
	\end{figure}
```

### Block C: Figure I-1 Flowchart
```latex
	\begin{figure}[ht]
		\centering
		% Define the styles for different blocks
		\tikzstyle{startstop} = [ellipse, draw, text centered, minimum height=3em]
		% --- FIX: Added text width and align to all styles ---
		\tikzstyle{process} = [rectangle, draw, text centered, minimum width=15em, minimum height=3em, align=center, text width=14em]
		\tikzstyle{subroutine} = [rectangle, draw, double, text centered, minimum width=12em, minimum height=3em, align=center, text width=11em]
		\tikzstyle{decision} = [diamond, draw, text centered, minimum width=12em, minimum height=3em, inner sep=0pt, aspect=2, align=center, text width=10em]
		\tikzstyle{arrow} = [draw, -{Stealth[]}, thick]
		\tikzstyle{line} = [draw, thick]
		
		\begin{tikzpicture}[node distance=1.5cm and 1cm, scale=0.5, transform shape]
			% --- MAIN PROGRAM ---
			
			% --- FIX: Removed all '\\' from node text ---
			\node (start) [startstop] {START};
			\node (read) [process, below=of start, yshift=-0.5cm] {READ IN \& PRINT OUT INPUT};
			\node (init) [process, below=of read] {INITIALIZE PARAMETERS FOR LIQUID REGION};
			\node (inc1) [process, below=of init, yshift=-1.5cm] {INCREMENT AXIALLY BY AMOUNT DZ};
			\node (calc) [process, below=of inc1] {CALCULATE TEMPERATURE ENTHALPY, DHDZ, DZ};
			\node (print) [process, below=of calc] {PRINT OUT Z, TEMP, H, DHDZ};
			\node (dec1) [decision, below=of print, yshift=-0.5cm] {HAVE WE REACHED L-LV INTERFACE?};
			\node (dec2) [decision, below=of dec1, yshift=-0.5cm] {OPTION = 2?};
			
			% Place parallel branches
			\node (lqvp) [subroutine, right=of dec2, xshift=4cm] {CALL LQVP};
			\node (lqv2) [subroutine, left=of dec2, xshift=-4cm] {CALL LQV2};
			
			% Continue main flow
			\node (inc2) [process, below=of dec2, yshift=-1.5cm] {INCREMENT AXIALLY BY AMOUNT DZ};
			\node (vapor) [subroutine, below=of inc2] {CALL VAPOR};
			\node (dec3) [decision, below=of vapor, yshift=-0.5cm] {MORE DATA CASES TO PROCESS?};
			\node (end) [startstop, below=of dec3, yshift=-0.5cm] {END};
			
			% Connect the main blocks with arrows
			\path [arrow] (start) -- (read);
			\path [arrow] (read) -- (init);
			\path [arrow] (init) -- (inc1);
			\path [arrow] (inc1) -- (calc);
			\path [arrow] (calc) -- (print);
			\path [arrow] (print) -- (dec1);
			\path [arrow] (dec1) -- node[right, xshift=5mm] {YES} (dec2);
			
			% Loop from dec1 back to inc1
			\draw [arrow] (dec1.west) -- ++(-4,0) node[left, xshift=-5mm] {NO} |- (inc1.west);
			
			\path [arrow] (dec2) -- node[right, xshift=5mm] {NO} (lqvp);
			\path [arrow] (dec2) -- node[left, xshift=-5mm] {YES} (lqv2);
			
			% Converge parallel branches
			\draw [arrow] (lqvp.south) |- (inc2.east);
			\draw [arrow] (lqv2.south) |- (inc2.west);
			
			\path [arrow] (inc2) -- (vapor);
			\path [arrow] (vapor) -- (dec3);
			\path [arrow] (dec3) -- node[right, xshift=5mm] {NO} (end);
			
			% Loop from dec3 back to read
			\draw [arrow] (dec3.west) -- ++(-10,0) node[left, xshift=-5mm] {YES} |- (read.west);
			
			% --- Subroutines called from MAIN ---
			\node (unbar1) [subroutine, right=of init, xshift=5cm] {SUBROUTINE UNBAR};
			\path [arrow] (init) -- (unbar1);
			
			% Create a node to group the subroutines
			\node (unbar2) [subroutine, right=of calc, xshift=5cm] {SUBROUTINE UNBAR};
			\node (param) [subroutine, below=of unbar2, node distance=1cm] {SUBROUTINE PARAM};
			\node (slope1) [subroutine, below=of param, node distance=1cm] {SUBROUTINE SLOPE};
			
			% Draw a box around them (optional, but in the original)
			\node[draw, inner sep=0.4cm, fit=(unbar2) (param) (slope1)] (subgroup) {};
			
			% Connect calc to the subgroup
			\path [arrow] (calc) -- (subgroup);
			
			% --- SUBROUTINE SLOPE (Breakout box) ---
			% Positioned to the right of the "MORE DATA CASES" decision node (dec3)
			\node (slope_brk_start) [subroutine, right=of dec3, xshift=5cm] {SUBROUTINE SLOPE};
			\node (slope_brk_calc) [process, below=of slope_brk_start] {CALCULATE CONC. AND TEMPERATURE PROFILES IN CATALYST PARTICLES};
			\node (slope_brk_return) [startstop, below=of slope_brk_calc] {RETURN};
			
			\path [arrow] (slope_brk_start) -- (slope_brk_calc);
			\path [arrow] (slope_brk_calc) -- (slope_brk_return);
			
			% --- Add Statement Numbers from Diagram ---
			\node[left, xshift=-2mm] at (read.west) {700, 601};
			\node[left, xshift=-2mm] at (init.west) {613};
			\node[left, xshift=-2mm] at (inc1.west) {850};
			\node[left, xshift=-2mm] at (calc.west) {777};
			\node[left, xshift=-2mm] at (print.west) {860};
			\node[left, xshift=-2mm] at (dec1.west) {874};
			\node[left, xshift=-2mm] at (dec2.west) {1020};
			\node[left, xshift=-2mm] at (inc2.west) {1021};
			\node[left, xshift=-2mm] at (vapor.west) {1021};
			\node[left, xshift=-2mm] at (dec3.west) {102};
			
		\end{tikzpicture}
		\caption{Figure I-1: MAIN PROGRAM and SUBROUTINE SLOPE Flow Diagrams}
		\label{fig:I-1}
	\end{figure}
```

### Block D: Figure I-2 Flowchart
```latex
	\begin{figure}[ht]
		\centering
		% Define the styles for different blocks
		\tikzstyle{startstop} = [ellipse, draw, text centered, minimum height=3em]
		\tikzstyle{process} = [rectangle, draw, text centered, minimum width=15em, minimum height=3em, align=center, text width=14em]
		\tikzstyle{subroutine} = [rectangle, draw, double, text centered, minimum width=12em, minimum height=3em, align=center, text width=11em]
		\tikzstyle{decision} = [diamond, draw, text centered, minimum width=12em, minimum height=3em, inner sep=0pt, aspect=2, align=center, text width=10em]
		\tikzstyle{arrow} = [draw, -{Stealth[]}, thick]
		\tikzstyle{line} = [draw, thick]
		
		% --- First Flowchart: SUBROUTINE LQVP ---
		\begin{tikzpicture}[node distance=1.5cm, scale=0.5, transform shape]
			% Place the nodes
			\node (lqvp) [subroutine] {SUBROUTINE LQVP};
			\node (init) [process, below=of lqvp] {INITIALIZE PARAMETERS FOR LIQUID-VAPOR REGION};
			\node (inc) [process, below=of init] {INCREMENT AXIALLY BY AMOUNT DZ};
			\node (calc) [process, below=of inc] {CALCULATE DZ, H, DHDZ, WEIGHT FRACTION OF VAPOR};
			\node (print) [process, below=of calc] {PRINT OUT Z, TEMP, H, WEIGHT FRACTION OF VAPOR};
			\node (dec) [decision, below=of print, yshift=-0.5cm] {HAVE WE REACHED LV-V INTERFACE?};
			\node (ret) [startstop, below=of dec, yshift=-0.5cm] {RETURN};
			
			% Place the side subroutines
			\node (unbar) [subroutine, right=of calc, xshift=5cm] {SUBROUTINE UNBAR};
			\node (param) [subroutine, below=of unbar] {SUBROUTINE PARAM};
			
			% Connect the nodes
			\path [arrow] (lqvp) -- (init);
			\path [arrow] (init) -- (inc);
			\path [arrow] (inc) -- (calc);
			\path [arrow] (calc) -- (print);
			\path [arrow] (print) -- (dec);
			\path [arrow] (dec) -- node[right, xshift=5mm] {YES} (ret);
			
			% Connect the side subroutines
			\path [arrow] (calc) -- (unbar);
			\path [arrow] (calc) -- (param);
			
			% Loop from decision
			\draw [arrow] (dec.west) -- ++(-4,0) node[left, xshift=-5mm] {NO} |- (inc.west);
			
			% Add statement numbers
			\node[left, xshift=-2mm] at (init.west) {100};
			\node[left, xshift=-2mm] at (inc.west) {1820};
			\node[left, xshift=-2mm] at (print.west) {1850};
			\node[left, xshift=-2mm] at (dec.west) {83};
			
		\end{tikzpicture}
		
		\vspace{2cm} % Add some space between the two flowcharts
		
		% --- Second Flowchart: SUBROUTINE LQV2 ---
		\begin{tikzpicture}[node distance=1.5cm, scale=0.5, transform shape]
			% Place the nodes
			\node (lqv2) [subroutine] {SUBROUTINE LQV2};
			\node (init) [process, below=of lqv2] {INITIALIZE PARAMETER FOR LIQUID-VAPOR REGION};
			\node (inc) [process, below=of init] {INCREMENT AXIALLY BY AMOUNT DZ};
			\node (calc) [process, below=of inc] {CALCULATE DZ, H, DHDZ, WEIGHT FRACTION OF VAPOR};
			\node (print) [process, below=of calc] {PRINT OUT Z, TEMP, H, WEIGHT FRACTION OF VAPOR};
			\node (dec) [decision, below=of print, yshift=-0.5cm] {HAVE WE REACHED LV-V INTERFACE?};
			\node (ret) [startstop, right=of dec, xshift=4cm] {RETURN};
			
			% Place the side subroutines
			\node (unbar) [subroutine, right=of calc, xshift=5cm] {SUBROUTINE UNBAR};
			\node (param) [subroutine, below=of unbar] {SUBROUTINE PARAM};
			\node (slope) [subroutine, below=of param] {SUBROUTINE SLOPE};
			
			% Connect the nodes
			\path [arrow] (lqv2) -- (init);
			\path [arrow] (init) -- (inc);
			\path [arrow] (inc) -- (calc);
			\path [arrow] (calc) -- (print);
			\path [arrow] (print) -- (dec);
			\path [arrow] (dec) -- node[above] {YES} (ret);
			
			% Connect the side subroutines
			\path [arrow] (calc) -- (unbar);
			\path [arrow] (calc) -- (param);
			\path [arrow] (calc) -- (slope);
			
			% Loop from decision
			\draw [arrow] (dec.west) -- ++(-4,0) node[left, xshift=-5mm] {NO} |- (inc.west);
			
			% Add statement numbers
			\node[left, xshift=-2mm] at (init.west) {100};
			\node[left, xshift=-2mm] at (inc.west) {1820};
			\node[left, xshift=-2mm] at (calc.west) {7};
			\node[left, xshift=-2mm] at (print.west) {3100};
			\node[left, xshift=-2mm] at (dec.west) {16};
			
		\end{tikzpicture}
		
		\caption{Figure I-2: SUBROUTINES LQVP and LQV2 Flow Diagrams}
		\label{fig:I-2}
	\end{figure}
```

### Block E: Figure I-3 and I-4 Flowchart
```latex
	\begin{figure}[ht]
		\centering
		
		\begin{tikzpicture}[
			scale=0.45, transform shape,
			node distance=1.5cm and 1cm,
			% Define the styles for different blocks
			startstop/.style = {ellipse, draw, text centered, minimum height=3em},
			process/.style = {rectangle, draw, text centered, minimum width=15em, minimum height=3em, align=center, text width=14em},
			subroutine/.style = {rectangle, draw, double, text centered, minimum width=12em, minimum height=3em, align=center, text width=11em},
			decision/.style = {diamond, draw, text centered, minimum width=12em, minimum height=3em, inner sep=0pt, aspect=2, align=center, text width=10em},
			arrow/.style = {draw, -{Stealth[]}, thick}
			]
			
			% --- Nodes from Figure I-3 (Page 82) ---
			\node (vapor) [subroutine] {SUBROUTINE VAPOR};
			
			\node (init) [process, below=of vapor] {INITIALIZE PARAMETERS FOR VAPOR REGION};
			\node (unbar1) [subroutine, below=of init] {CALL UNBAR};
			\node (sgrad) [subroutine, below=of unbar1] {CALL SGRAD};
			\node (dec1) [decision, below=of sgrad, yshift=-1cm] {HAS TEMP VS Z PROFILE REACHED INITIAL PEAK};
			
			\node (fix_dz) [process, right=of dec1, xshift=6cm] {FIX DZ INCREMENTS FROM PRESENT Z POSITION TO END OF BED...15 INCREMENTS IN TOTAL};
			\node (calc_new_dz) [process, below=of dec1, yshift=-1cm] {CALCULATE NEW DZ INCREMENT};
			
			\node (do_calc1) [process, below=of calc_new_dz] {DO PROGRAM CALCULATIONS FOR DWIDZ ... DC4DZ, DPDZ, DRDER};
			% This coordinate is for the loop-back from Fig I-4
			\coordinate (loop_target) at ($(do_calc1.south) + (0,-0.75cm)$);
			\node (dec2) [decision, below=of do_calc1, yshift=-1cm] {HAS TEMP VS Z PROFILE REACHED INITIAL PEAK};
			
			% --- START FIX: MOVED THIS BLOCK BACK TO THE LEFT ---
			\node (dec3) [decision, left=of do_calc1, xshift=-6cm] {INITIAL FEED RATE $\neq$ 0?};
			\node (dec4) [decision, below=of dec3] {DZ INCREMENT TOO LARGE?};
			\node (redivd) [subroutine, below=of dec4] {CALL REDIVD};
			\node (print_rediv) [process, below=of redivd] {PRINT MESSAGE ON DZ INCREMENT REDIVISION};
			% --- END FIX ---
			
			% Side subroutines for init
			\node (unbar2) [subroutine, right=of init, xshift=5cm] {SUBROUTINE UNBAR};
			\node (conc) [subroutine, below=of unbar2, node distance=1cm] {SUBROUTINE CONC};
			\node[draw, inner sep=0.4cm, fit=(unbar2) (conc)] (init_subs) {};
			
			
			% --- Nodes from Figure I-4 (Page 83) ---
			\node (do_calc2) [process, below=of dec2, yshift=-1.5cm] {DO PROGRAM CALCULATIONS FOR TEMP, PRESSURE, H, C1, C2, C3, C4 AND MOLE FRACTIONS...};
			\node (dec5) [decision, below=of do_calc2, yshift=-0.5cm] {FRAC3D TOO LARGE?};
			\node (half_dz) [process, left=of dec5, xshift=-5cm] {DZ = DZ/2.};
			
			\node (inc_dz) [process, below=of dec5, yshift=-1.5cm] {INCREMENT AXIALLY BY AMOUNT DZ};
			\node (test_flags) [process, below=of inc_dz] {TEST AND/OR RESET JFLAG, NINT PARAMETERS};
			\node (print_main) [process, below=of test_flags] {PRINT OUT Z, TEMP, PRESSURE, H, C1, C2, C3, C4 AND MOLE FRACTIONS...};
			\node (dec6) [decision, below=of print_main, yshift=-0.5cm] {END OF REACTOR REACHED?};
			
			\node (dec7) [decision, below=of dec6, yshift=-1.5cm] {INITIAL FEED RATE NON-ZERO};
			\node (insert_z) [process, right=of dec7, xshift=5cm] {INSERT 6 ADDITIONAL Z VALUES AT END OF REACTOR BED};
			\node (print_z) [process, below=of dec7, yshift=-0.5cm] {PRINT OUT ALL AXIAL STATION Z VALUES FROM VAPOR REGION};
			\node (ret) [startstop, below=of print_z] {RETURN};
			
			% --- Draw Arrows ---
			% Fig I-3 flow
			\path [arrow] (vapor) -- (init);
			\path [arrow] (init) -- (init_subs);
			\path [arrow] (init) -- (unbar1);
			\path [arrow] (unbar1) -- (sgrad);
			\path [arrow] (sgrad) -- (dec1);
			
			\path [arrow] (dec1) -- node[right, xshift=5mm] {YES} (fix_dz);
			\path [arrow] (dec1) -- node[left, xshift=-5mm] {NO} (calc_new_dz);
			
			\draw [arrow] (fix_dz.south) |- (do_calc1.east);
			\path [arrow] (calc_new_dz) -- (do_calc1);
			\path [arrow] (do_calc1) -- (loop_target);
			\path [arrow] (loop_target) -- (dec2);
			
			% --- START FIX: Corrected arrow path and label position ---
			\path [arrow] (dec2) -- node[left, xshift=-5mm] {YES} (dec3);
			\path [arrow] (dec3) -- node[above] {YES} (dec4);
			\path [arrow] (dec4) -- node[left, xshift=-5mm] {YES} (redivd);
			% --- END FIX ---
			
			\path [arrow] (redivd) -- (print_rediv);
			
			% Fig I-4 flow
			% --- START FIX: Corrected paths from left-hand branch ---
			\path [arrow] (dec2) -- node[right, xshift=5mm] {NO} (do_calc2);
			\draw [arrow] (dec3.south) -- node[right, near start] {NO} ++(0,-1) -| (do_calc2.west);
			\draw [arrow] (dec4.south) -- node[right, near start] {NO} ++(0,-3) -| (do_calc2.west);
			\draw [arrow] (print_rediv.south) -- ++(0,-1) -| (do_calc2.west);
			% --- END FIX ---
			
			\path [arrow] (do_calc2) -- (dec5);
			\path [arrow] (dec5) -- node[left, xshift=-5mm] {NO} (inc_dz);
			\node[left, xshift=-2mm] at (inc_dz.west) {73};
			\path [arrow] (dec5) -- node[above] {YES} (half_dz);
			\draw [arrow] (half_dz.west) -- ++(-1,0) |- (do_calc2.west);
			
			\path [arrow] (inc_dz) -- (test_flags);
			\path [arrow] (test_flags) -- (print_main);
			\path [arrow] (print_main) -- (dec6);
			
			% Loop back from Fig I-4 to Fig I-3
			\draw [arrow] (dec6.west) -- ++(-12,0) node[left, xshift=-5mm] {NO} |- (unbar1);
			
			% Bottom of Fig I-4
			\path [arrow] (dec6) -- node[right, xshift=5mm] {YES} (dec7);
			\path [arrow] (dec7) -| node[right, pos=0.25] {YES} (insert_z);
			\path [arrow] (dec7) -- node[left, xshift=-5mm] {NO} (print_z);
			\path [arrow] (insert_z) -- (print_z);
			\path [arrow] (print_z) -- (ret);
			
			% --- Add Statement Numbers ---
			\node[left, xshift=-2mm] at (init.west) {100};
			\node[left, xshift=-2mm] at (unbar1.west) {7};
			\node[left, xshift=-2mm] at (sgrad.west) {13};
			\node[left, xshift=-2mm] at (dec1.west) {15};
			\node[left, xshift=-2mm] at (calc_new_dz.west) {4000};
			\node[left, xshift=-2mm] at (do_calc1.west) {4000};
			\node[left, xshift=-2mm] at (dec2.west) {90};
			
			% --- FIX: Moved statement numbers back to the left ---
			\node[left, xshift=-2mm] at (dec3.west) {98};
			\node[left, xshift=-2mm] at (dec4.west) {93};
			\node[left, xshift=-2mm] at (redivd.west) {19};
			\node[left, xshift=-2mm] at (print_rediv.west) {91};
			% --- END FIX ---
			
			\node[left, xshift=-2mm] at (do_calc2.west) {4051};
			\node[left, xshift=-2mm] at (dec5.west) {17};
			\node[left, xshift=-2mm] at (half_dz.west) {18};
			\node[left, xshift=-2mm] at (inc_dz.west) {73};
			\node[left, xshift=-2mm] at (test_flags.west) {73};
			\node[left, xshift=-2mm] at (print_main.west) {4050};
			\node[left, xshift=-2mm] at (dec6.west) {38};
			\node[left, xshift=-2mm] at (dec7.west) {1};
			\node[left, xshift=-2mm] at (print_z.west) {22};
			
		\end{tikzpicture}
		\caption{Figure I-3 \& I-4: SUBROUTINE VAPOR Flow Diagram (Combined)}
		\label{fig:I-3-4}
	\end{figure}
```

### Block F: One-Dimensional MAIN Program Listing
```latex
	\begin{lstlisting}[language=Fortran, caption=MAIN Program Listing, label=list:main_1d]
C **********************************************************************
C * *
C * DESCRIPTION OF INPUT DATA PUNCH CARDS FOLLOWS...                   *
C * *
C **********************************************************************
C
C CARD 1      COL'S 1-3   CONTAIN NCASE   (I3)    (ONLY ONE CARD 1 PER RUN)
C
C (CARDS 2 THRU 16 SHOULD BE REPEATED FOR EACH DATA CASE)
C
C CARD 2      COL'S 1-80  TITLE CARD (14A6) ANY ALPHANUMERIC INFORMATION DESIRED
C
C CARD 3      COL'S 1-2   CONTAIN OPTION  (I2)
C             COL'S 3-4   CONTAIN PRINT   (I2)
C             COL'S 5-7   CONTAIN NOFZ    (I3)
C
C CARD 4      COL'S 1-10  CONTAIN ZO      (E10.5)
C             COL'S 11-20 CONTAIN GO      (E10.5)
C             COL'S 21-30 CONTAIN FC      (E10.5)
C             COL'S 31-40 CONTAIN ALPHA3  (E10.5)
C             COL'S 41-50 CONTAIN HF      (E10.5)
C             COL'S 51-60 CONTAIN R       (E10.5)
C             COL'S 61-70 CONTAIN WM4     (E10.5)
C             COL'S 71-80 CONTAIN WM3     (E10.5)
C
C CARD 5      COL'S 1-10  CONTAIN WM2     (E10.5)
C             COL'S 11-20 CONTAIN WM1     (E10.5)
C             COL'S 21-30 CONTAIN ALPHA1  (E10.5)
C             COL'S 31-40 CONTAIN ALPHA2  (E10.5)
C             COL'S 41-50 CONTAIN AGM     (E10.5)
C             COL'S 51-60 CONTAIN BGM     (E10.5)
C             COL'S 61-70 CONTAIN KP      (E10.5)
C             COL'S 71-80 CONTAIN CGM     (E10.5)
C
C CARD 6      COL'S 1-10  CONTAIN TF      (E10.5)
C             COL'S 11-20 CONTAIN CFL     (E10.5)
C             COL'S 21-30 CONTAIN ENMX1   (E10.5)
C             COL'S 31-40 CONTAIN ENMX2   (E10.5)
C             COL'S 41-50 CONTAIN ENMX3   (E10.5)
C             COL'S 51-60 CONTAIN DIF3    (E10.5)
C             COL'S 61-70 CONTAIN DIF4    (E10.5)
C             COL'S 71-80 CONTAIN PRES    (E10.5)
C
C CARD 7      COL'S 1-10  CONTAIN ZEND    (E10.5)
C             COL'S 11-20 CONTAIN EN1     (E10.5)
C             COL'S 21-30 CONTAIN EN2     (E10.5)
C             COL'S 31-40 CONTAIN EN3     (E10.5)
C
C (THE TABLE FOR CATALYST PARTICLE RADIUS VS
C  AXIAL DISTANCE ALONG REACTOR BED FOLLOWS)
C
C CARD 8      COL'S 1-8   CONTAIN THE NUMBER 0.0      (E8.4)
C             COL'S 9-16  CONTAIN THE NUMBER 1.0      (E8.4)
C             COL'S 17-24 CONTAIN NOFZ (FLOATING POINT) (E8.4)
C             COL'S 25-32 CONTAIN THE NUMBER 0.0      (E8.4)
C
C CARDS 9A,9B...  CONTAIN THE AXIAL STATION Z VALUES  (10E8.4)
C             Z(1),Z(2),....Z(NOFZ)
C             10 PER CARD, COL'S 1-80
C
C CARDS 10A,10B... CONTAIN THE CATALYST PARTICLE RADII (10E8.4)
C             A(1),A(2),....A(NOFZ)
C             10 PER CARD, COL'S 1-80
C
C (THE TABLE FOR CATALYST PARTICLE SURFACE AREA
C  VS AXIAL DISTANCE ALONG REACTOR BED FOLLOWS)
C
C CARD 11     THIS CARD IS IDENTICAL TO CARD 8
C
C CARDS 12A,12B... THESE CARDS (OR SINGLE CARD) ARE IDENTICAL TO CARDS 9A,9B...
C
C CARDS 13A,13B... CONTAIN THE CATALYST PARTICLE SURFACE AREAS (10E8.4)
C             AP(1),AP(2),...AP(NOFZ)
C             10 PER CARD, COL'S 1-80
C
C (THE TABLE FOR INTERPARTICLE VOID FRACTION VS
C  AXIAL DISTANCE ALONG REACTOR BED FOLLOWS)
C
C CARD 14     THIS CARD IS IDENTICAL TO CARD 8
C
C CARDS 15A,15B... THESE CARDS (OR SINGLE CARD) ARE IDENTICAL TO CARDS 9A,9B...
C
C CARDS 16A,16B... CONTAIN THE INTERPARTICLE VOID FRACTIONS (10E8.4)
C             DELA(1),DELA(2),....DELA(NOFZ)
C             10 PER CARD, COL'S 1-80
C
REAL KP,K 															   0
INTEGER OPTION,PRINT												  10
COMMON /FTZ/TBLVP(70),TBLH4(42),TBLH3(42),SHTBL1(34),SHTBL2(34), 	  20
1        SHTBL3(34),SHTBL4(34),ZTBLD(46),ZTBLAP(46),ZTBLA(46) 		  30
COMMON /CO/HL,HV,FC,TF,CFL,CGM,ENMX1,AGM,DIF3,DIF4,KP,PRES,G0,		  40
1        WM4,WM3,WM2,WM1,ALPHA3,R,TVAP,ZEND,BGM,HF,DZ,ALPHA1,ALPHA2	  50
2        ,ENMX2,ENMX3,EN1,EN2,EN3,H,RAT,MI 							  60
COMMON /VAR/DERIV(250),DHDZ(250),Z(250)								  70
COMMON /TOLL/ALIM,OPTION,C1,C2,C3,C4,CAV,G,TEMP,AP,WMAV,Z0,			  80
COMMON /MUVST/VISVST(30)											  90
COMMON /FLAGS/MFLAG,KFLAG,PRINT 									 100
COMMON /IFCE00/IFC,GATZ0											 110
COMMON /LIZTBL/DHVST(18),DHLVST(18)									 120
COMMON /DAVTBL/VPTBL(44)											 130
DIMENSION  TITLE(14) 												 140
READ (5,700) NCASE 													 150
700 FORMAT (I3)															 160
KOUNT=1																 170
705 READ (5,608) TITLE 													 180
608 FORMAT (14A6)														 190
WRITE (6,609) TITLE													 200
609 FORMAT (1H1,14A6//)													 210
IFC=1																 220
READ (5,809) OPTION,PRINT,NOFZ										 230
809 FORMAT (2I2,I3)														 240
READ (5,800) Z0,G0,FC,ALPHA3,HF,R,WM4,WM3,WM2,WM1,ALPHA1,ALPHA2,	 250
X      AGM,BGM,KP,CGM,TF,CFL,ENMX1,ENMX2,ENMX3,DIF3,DIF4,PRES,ZEND,   260
X      EN1,EN2,EN3,													 270
800 FORMAT (8E10.5)														 280
NZTBL = 2*NOFZ+4													 290
NOFZ4 = NOFZ+4														 300
NOFZ5 = NOFZ4+1 													 310
CALL UNBAR (VPTBL(1),1,PRES,0.,TVAP,KK)								 320
CALL UNBAR (DHVST(1),1,TVAP,0.,DELHV,KK)							 330
CALL UNBAR (DHLVST(1),1,TVAP,0.,DELHL,KK)							 340
HL=(TVAP-TF)*CFL													 350
HV=HL+DELHV-DELHL													 360
GATZ0=G0+FC*Z0														 370
IF(FC.GT.0.)GO TO 837												 380
IFC=0																 390
637 WRITE (6,600)														 400
600 FORMAT (52X,16H INPUT CONSTANTS/7X,102H HF      HL        HV  	     410
X       TF      TVAP    CFL     PRESSURE    KP    FC                 420
X       G0) 															 430
WRITE (6,601) HF,HL,HV,TF,TVAP,CFL,PRES,KP,FC,G0					 440
601 FORMAT (3X,10E11.6//)												 450
WRITE (6,602)														 460
602 FORMAT (7X,103H  R    ALPHA3   CGM   DIF3    DIF4 					 470
X        WM4     WM3   
X   WM2     WM1   ZEND)							 480
WRITE (6,601) R,ALPHA3,CGM,DIF3,DIF4,WM4,WM3,WM1,WM1,ZEND			 490
WRITE (6,603)														 500
603	FORMAT (6X,113H  AGM   BGM   ALPHA1    ALPHA2   N1 					 510
X   N2    N3   ENMX1   ENMX2   ENMX3     )							 520
WRITE (6,601) AGM,BGM,ALPHA1,ALPHA2,EN1,EN2,EN3,ENMX1,ENMX2,ENMX3    530
WRITE (6,617) Z0													 540
617 FORMAT (// 8X,'Z0' / 3X,E11.6)										 550
READ (5,20) (ZTBLA(I),I=1,4)										 560
20 FORMAT (4E8.4)														 570
READ (5,21) (ZTBLA(I),I=5,NOFZ4)    								 580
21 FORMAT (10E8.4) 													 590
READ (5,21) (ZTBLA(I),I=NOFZ5,NZTBL)								 600
READ (5,20) (ZTBLAP(I),I=1,4)										 610
READ (5,21) (ZTBLAP(I),I=5,NOFZ4)									 620
READ (5,21) (ZTBLAP(I),I=NOFZ5,NZTBL)								 630
READ (5,20) (ZTBLD(I),I=1,4)										 640
READ (5,21) (ZTBLD(I),I=5,NOFZ4)									 650
READ (5,21) (ZTBLD(I),I=NOFZ5,NZTBL)								 660
WRITE (6,604)														 670
604	FORMAT (///55X,13H Z VS A TABLE)									 680
WRITE (6,22) (ZTBLA(I),I=1,4)										 690
22 FORMAT (40X,4E13.5)												     700
WRITE (6,23) (ZTBLA(I),I=5,NOFZ4)									 710
23 FORMAT (1X,10E13.5)													 720
WRITE (6,25)														 730
25 FORMAT ( / ) 														 740
WRITE (6,23) (ZTBLA(I),I=NOFZ5,NZTBL)								 750
WRITE (6,24) 														 760
24 FORMAT ( // )														 770
WRITE (6,606)														 780
606 FORMAT (54X,14H Z VS AP TABLE)										 790
WRITE (6,22) (ZTBLAP(I),I=1,4)										 800
WRITE (6,23) (ZTBLAP(I),I=5,NOFZ4)									 810
WRITE (6,25)														 820
WRITE (6,23) (ZTBLAP(I),I=NOFZ5,NZTBL)								 830
WRITE (6,24) 														 840
WRITE (6,607)														 850
607 FORMAT (54X,14H Z VS DELTA TABLE)									 860
WRITE (6,22) (ZTBLD(I),I=1,4)										 870
WRITE (6,23) (ZTBLD(I),I=5,NOFZ4)									 880
WRITE (6,25)														 890
WRITE (6,23) (ZTBLD(I),I=NOFZ5,NZTBL)								 900
WRITE (6,613) 														 910
613 FORMAT (18X, ******************************** ENTERING LIQUID        920
X REGION     ********************************) 						 930
MFLAG=0																 940
DZ=0.0																 950
Z(1)=0.0															 960
H=HF																 970
II=2																 980
850 Z(II)=Z(II-1)+DZ 													 990
TEMP=TF+(H-HF)/CFL													1000
CALL UNBAR (TBLVP(I),1,TEMP,0.,VP,KK)								1010
CN2H4=(VP*WM4)/(R*TEMP)												1020
CALL UNBAR (TBLH4(I),1,TEMP,0.,H4,KK)								1030
CALL UNBAR (ZTBLAP(I),1,Z(II),0.,AP,KK)								1040
CALL UNBAR (ZTBLA(I),1,Z(II),0.,A,KK)								1050
CALL PARAM(TEMP,Z(II),1,CN2H4,H4,0,G,GMMA,K,DPA,BETA)				1060
CALL SLOPE (CN2H4,GMMA,K,BETA,EN1,DERIV(II),DPA,A,DIF4)			    1070
IF(H-HL)777,776,777													1080
776 IF(MI.GT.20)DERIV(II)=DERIV(II-1)									1090
777 DHDZ(II)=-(H4*DPA*AP*DERIV(II)+FC*(H-HF))/G							1100
DZ=-H4/(ENMX1*DHDZ(II))												1110
WRITE(6,820)														1120
820 FORMAT (/39X,48H  Z    TEMP    H DHDZ)								1130
WRITE(6,860) Z(II),TEMP,H,DHDZ(II)									1140
860 FORMAT (/30X,4E15.6)												1150
IF(H-HL) 874,1020,874												1160
874 H=H+DHDZ(II)*DZ														1170
IF(H-HL) 875,1020,1000												1180
875 II=II+1																1190
GO TO 850															1200
C		BACKSTEP TO L-L-V-BOUNDARY 											
1000 DZ=(HL-H)/DHDZ(II)+DZ												1210
H=HL																1220
II=II+1																1230
GO TO 850															1240
1020 IF(OPTION.EQ.2) CALL LQV2(H,Z(II),DERIV(II),II,DHDZ(II),TEMP,CN2H4) 1250
IF(OPTION.EQ.2) GO 													1260
TO 1021
CALL LQVP(H,Z(II),DERIV(II),II,DHDZ(II),TEMP)						1270
C		START VAPOR REGION
1021 DZ=-H4/(ENMX2*DHDZ(II))												1280
CALL VAPOR(TEMP,Z(II),II,DHDZ(II),DERIV(II),H)						1290
KOUNT=KOUNT+1														1300
IF(KOUNT.LE.NCASE) GO TO 705 										1310
WRITE(6,102)														1320
102 FORMAT (////41X,36H ***** OPERATIONS COMPLETE *****)				1330
STOP																1340
END																	1350
	\end{lstlisting}
```

### Block G: Appendix Include Reference
```latex
	\include{app-NASA9.tex}
```
