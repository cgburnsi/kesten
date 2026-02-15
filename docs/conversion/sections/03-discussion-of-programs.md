# 3. Discussion of One- and Two-Dimensional Steady-State Computer Programs
The equations representing the one and two-dimensional steady-state models have been programmed for the UNIVAC 1108 digital computer.
These computer programs are discussed below. Included in this discussion are input and output descriptions and descriptions of common operational problems associated with the programs.

## One-Dimensional Steady-State Model

### Input Description
The following is a listing of the necessary input for the one-dimensional steady-state computer program.
The input format is given in Table I. The coding of a sample data case is shown in Fig. 1 and a listing of the input data punch cards corresponding to this sample data case is shown in Fig. 2. The card numbers in the text below correspond to the card numbers (first column) of Table I. For each run there will be only one card number one.
Cards 2 through 16 should be repeated for each data case to be run.
- The first card contains the number **NCASE**. This number indicates the number of data cases with each run.
$1 \le \text{NCASE} \le 999$.
- The second card is the **title card** used for individual data case identification.
The title may be any alpha numeric information desired.
- The third card contains the indicators **OPTION** and **PRINT** and the number **NOFZ**.
**OPTION** is used to indicate which method of analyzing the liquid-vapor region is desired.
If **OPTION** = 2, the program will use the method in subroutine LQV2.
If **OPTION** $\ne$ 2, the program will use the method in subroutine LQVP.
These two methods are described in Appendix I. **PRINT** is used to indicate which type of printout is desired.
If **PRINT** = 0 or is blank, the "standard output" described in the section on output is printed.
If **PRINT** = 1, both "standard" and "nonstandard output" are printed.
"Nonstandard output" is also described in the section on output.
**NOFZ** is the number of axial stations (Z's) to be used in the three tables input on cards 8 through 16.
- The fourth card contains the eight constants **ZO**, **GO**, **FC**, **ALPHA3**, **HF**, **R**, **WM4**, and **WM3**.
- **ZO** is the axial distance to the end of a buried injector in ft. (Ref. 1).
- **GO** is the inlet mass flow rate in $lb/ft^{2}-sec$. It must be greater than zero.
- **FC** is the rate of feed of hydrazine from buried injectors (Ref. 1) into the system in $lb/ft^{3}$-sec.
- **ALPHA3** is the preexponential factor in the rate equation for the thermal decomposition of hydrazine (See Ref. 1).
It equals $2.14 \times 10^{10} sec^{-1}$.
- **HF** is the enthalpy of liquid hydrazine entering the bed in $Btu/lb$.
- **R** is a gas constant. It equals 10.73 $(psia-ft^{3})/(lb \text{ mole-deg } R)$.
- **WM4** is the molecular weight of hydrazine. It equals 32.048 lb/lb mole.
- **WM3** is the molecular weight of ammonia. It equals $17.032~lb/lb$ mole.
- The fifth card contains the eight constants **WM2**, **WM1**, **ALPHAL**, **ALPHA2**, **AGM**, **BGM**, **KP**, and **CGM**.
- **WM2** is the molecular weight of nitrogen. It equals 28.016 $lb/lb$ mole.
- **WM1** is the molecular weight of hydrogen. It equals $2.016~lb/lb$ mole.
- **ALPHAL** is the preexponential factor in the rate equation for the catalytic decomposition of hydrazine (See Ref. 1).
For the Shell 405 catalyst it equals $10^{10} sec^{-1}$.
- **ALPHA2** is the preexponential factor in the rate equation for the catalytic decomposition of ammonia (See Ref. 1).
For the Shell 405 catalyst it equals $10^{11}(lb/ft^{3})^{0.5}(sec)^{-1}$. (Note: the exponent 1.b in the original file was 0.5 in the PDF)
- **AGM** is the activation energy for the catalytic decomposition of hydrazine, divided by the gas constant.
For the Shell 405 catalyst it equals 2500 deg R.
- **BGM** is the activation energy for the catalytic decomposition of ammonia, divided by the gas constant.
For the Shell 405 catalyst it equals 50,000 deg R.
- **KP** is the thermal conductivity of the porous catalyst particle.
For the Shell 405 catalyst it equals $0.4\times10^{-4}$ Btu/ft-sec-deg R.
- **CGM** is the activation energy for the thermal decomposition of hydrazine, divided by the gas constant.
It equals 33,000 deg R.
- The sixth card contains the seven constants **TF**, **CFL**, **ENMX1**, **ENMX2**, **ENMX3**, **DIF3**, **DIF4**, and the inlet value of **PRES**.
- **TF** is the temperature of liquid hydrazine entering the bed in deg R.
- **CFL** is the specific heat of liquid hydrazine.
It equals 0.7332 Btu/lb-deg R.

- **ENMX1** is the constant used to determine the size of axial station increments in the liquid region. It equals 200. Increasing this number would result in a decrease in size of axial station increments (and an increase in computer run time).
- **ENMX2** is the constant used to determine the size of axial station increments in the liquid-vapor region. It equals 40. Increasing this number would result in a decrease in size of axial station increments (and an increase in computer run time).
- **ENMX3** is the constant used to determine the size of axial station increments in the vapor region. It equals 80. Increasing this number would result in a decrease in size of axial station increments (and an increase in computer run time).
- **DIF3** is the diffusion coefficient of ammonia in the gas phase at STP. It equals $0.17x10^{-3}ft^{2}/sec$.
- **DIF4** is the diffusion coefficient of hydrazine in the gas phase at STP. It equals $0.95x10^{-4}ft^{2}/sec$.
- **PRES** is the inlet chamber pressure in psia.
- The seventh card contains the four constants **ZEND**, **EN1**, **EN2**, and **EN3**.
- **ZEND** is the catalytic bed length in ft.
- **EN1** is the order of hydrazine catalytic decomposition reaction with respect to hydrazine.
For the Shell 405 catalyst it equals 1.0.
- **EN2** is the order of ammonia catalytic decomposition reaction with respect to ammonia.
For the Shell 405 catalyst it equals 1.0.
- **EN3** is the order of ammonia catalytic decomposition reaction with respect to hydrogen.
For the Shell 405 catalyst it equals -1.6.
- **Cards 8 through 10** contain **ZTBLA(I)**, the interpolation table used to obtain the catalyst particle radius (A) at any point along the reactor bed.
Subroutine UNBAR, an interpolation routine developed at the United Aircraft Research Laboratories, is used to obtain an appropriate particle radius, A, for a given axial station, $Z(I)$, along the bed.
For this table there should be a total of (NOFZ) Z's and (NOFZ) A's.
The table is set up as follows:
- **CARD NO. 8**: This card contains the four table descriptors used by UNBAR.
The first descriptor signifies the table number. For this program it equals 0.0.
The second descriptor tells at what location in the array the table starts;
the tables in this program are read in such that this number equals 1.0.
The third descriptor is the number of independent variables in the table (in this case, the number of Z's).
This number equals NOFZ. The fourth descriptor for a univariate table such as this one should equal 0.0.
- **CARD(S) NO. 9**: These cards contain the monotonically increasing Z values.
Enough cards should be used to contain NOFZ values of Z at the rate of ten per card.
For example, if NOFZ = 12, 12 values of Z should be input using two cards with ten values on the first card and the 2 remaining values on the second card.
- **CARD(S) NO. 10**: These cards contain the A's which correspond to the Z's listed on cards 9. Enough cards should be used to contain NOFZ values of A at the rate of ten per card.
- **Cards 11 through 13** contain **ZTBLAP(I)**, the interpolation table used to obtain the total external catalyst particle surface area per unit volume of bed (AP).
These AP values are obtained from UNBAR as functions of axial distance (Z) as in the ZTBLA table discussed above.
For this table there should be a total of (NOFZ) Z's and (NOFZ) AP's.
The table is set up as follows:
- **CARD NO. 11**: This card is exactly the same as card 8.
- **CARD(S) NO. 12**: These cards are exactly the same as cards 9.
- **CARD(S) NO. 13**: These cards contain the AP values which correspond to the Z's listed on cards 12. Enough cards should be used to contain NOFZ values of AP at the rate of ten per card.
- **Cards 14 through 16** contain **ZTBLD(T)**, the interpolation table used to obtain the interparticle void fraction (DELA).
These DELA values are obtained from UNBAR as functions of axial distance (Z) as in the ZTBLA table discussed above.
For this table there should be a total of (NOFZ) Z's and (NOFZ) DELA's.
The table is set up as follows:
- **CARD NO. 14**: This card is exactly the same as card 8.
- **CARD(S) NO. 15**: These cards are exactly the same as cards 9.
- **CARD(S) NO. 16**: These cards contain the DELA values which correspond to the Z's listed on cards 15. Enough cards should be used to contain NOFZ values of DELA at the rate of ten per card.


 

### Input Format


> [Table block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3 for full formatting.]


> [Table block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3 for full formatting.]


> [Table block omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3 for full formatting.]


### Output Description
Output from the one-dimensional steady-state program is entirely in printout form. Standard output, which is printed out when input option `PRINT = 0`, includes all printing normally done during execution of any representative data case, three messages which pertain to calculations which do not follow the normal pattern in a typical run, and one error message which is followed by program termination. Non-standard output is printed in addition to the standard output when `PRINT = 1`. This non-standard output includes additional calculated values and comments which pertain to intermediate calculations.

The print statements associated with each routine in which output is generated are described below.

### Standard Output
- **MAIN program**
- A complete listing of all program input including FORTRAN variable titles for all input variables.
- Axial position, (Z), temperature, (TEMP), enthalpy, (H), and rate of change of enthalpy with axial distance, (DHDZ), for each axial position in the liquid region.
- **Subroutine LQVP or LQV2**
- Axial position, (Z), temperature, (TEMP), enthalpy, (H), and weight fraction of vapor, (WFV), for each axial position in the liquid-vapor region.
- **Subroutine VAPOR**
- Axial position, (Z), temperature, (TEMP), pressure (PRES), enthalpy, (H), and concentrations of hydrogen, (C1), nitrogen, (C2), ammonia, (C3), and hydrazine, (C4), at each axial position in the vapor region.
- Mole fractions of hydrogen, (MFRAC1), nitrogen, (MFRAC2), ammonia, (MFRAC3), and hydrazine, (MFRAC4), and the fractional dissociation of ammonia, (FRAC3D), at each axial position in the vapor region.
- All axial positions, (Z values), in the vapor region listed consecutively and MBAR and G values at the end of the reactor for use in preparing input to the transient model computer program.
- "KOUNT = XX --- THIS INTERVAL HAS BEEN REDIVIDED XXXX TIMES"

For all cases involving a non-zero embedded injector feed rate, a check is made on the Z step size after each calculation. If the increment proves too large to yield satisfactory results, it is halved and re-checked. The procedure continues until a satisfactory interval size is found, and the above message is then printed.
- "THERE IS A PUDDLE OF COLD HYDRAZINE AT THE LIQUID-VAPOR/VAPOR INTERFACE.--- TRY USING A LARGER VALUE FOR GO"

When using a buried injector scheme it is possible to "flood" the region surrounding the injector tip with cold, liquid hydrazine. A sudden drop in axial temperatures at the liquid-vapor/vapor interface indicates that this has occurred, and in such cases the above message is printed and no further calculations are made.
- **Subroutine SGRAD**
- "WE HAVE CALCULATED A NEGATIVE XO DURING ITERATION NO. XX. SET $X0=0$, CALCULATE TPS = .XXXXX + XX, AND CONTINUE"

X0 represents an approximation of the radial distance to which hydrazine penetrates the catalyst particle before being dissipated. It is determined through an iterative procedure, and in some instances initial guesses do not yield satisfactory results. In this case, corrective measures to yield a better approximation to XO are instituted and the procedure repeated. This message indicates only that corrective calculations to improve on the accuracy of XO are being initiated.
- "UNABLE TO CONVERGE ON CPS IN 50 TRIES ---	$CP(X/A)=.xxxxxx \pm xx$"

If subroutine SGRAD cannot calculate a "converged" value for CPS after 50 iterations, the final value for CP at the particle surface is used to approximate CPS. This is a good approximation to CPS, however, and program calculations continue with the above message being printed.
- "UNABLE TO FIND SUITABLE X0 AFTER FOUR TRIES OF 25 ITERATIONS EACH --- PROGRAM STOP FOLLOWS"

If after four corrective attempts to approximate X0 the procedure still do not yield satisfactory results, this message along with all unacceptable values for X0 is printed and further calculations are stopped. An octal dump of core accompanies the program stop.


### Non-Standard Output
- **Subroutine SLOPE**
- "INITIAL CHOICE THROUGH ORIGIN IS TOO LARGE"

When iterating to find a satisfactory approximation to the radial depth of penetration of hydrazine in a catalyst particle (X0 calculation), an initial guess is the particle radius itself. If this proves to be an unsatisfactory choice, the above message is printed and a different initial guess is used.
- "SATISFACTORY STARTING CURVE FOUND AFTER XX TRAILS. THE VALUE OF B (X0) IS .XXXXXX + XX"

This message indicates that a satisfactory approximation to the radial depth of penetration of hydrazine in a catalyst particle has been found, and appears frequently in calculations involving the liquid region of the reactor.
- "INITIAL CHOICE THRU ORIGIN SEEMINGLY OK, BUT RESULTS ROTTEN AFTER 99 ITERATIONS --- SET X0 =.000001* A AND USE MORE REFINED TECHNIQUE"

When calculating a concentration vs radial position profile within the catalyst particle, an initial guess at the profile is used assuming a linear profile from the center of the particle to the surface. It can happen that this appears to be a satisfactory first guess, but ultimately yields unsatisfactory results for the final "converged" values of CPA. In such instances the above message is printed and the iteration procedure is repeated using a new initial guess.
- "ITERATION = XX ... [concentration-profile tabular printout omitted for readability] ... THE SLOPE CONVERGES TO XXXXXXX + xx"

When a converged value for the slope of the concentration profile curve at the catalyst particle surface has been calculated, the above "concentration profile" will be printed. The word "ITERATION" refers to the iteration count at the time of convergence. $X/A$ is the normalized distance from the center of the catalyst particle of radius A to the surface. CPA is the concentration of hydrazine within the particle at the corresponding normalized radial distance. The final message indicates the final converged value of the slope. This block will be printed for each axial station of the liquid region.
- "THE SLOPE CONVERGES TO $.xxxxxx \pm xx$"

This message indicates that the iterative procedure has achieved convergence on a value of the hydrazine concentration gradient at the catalyst particle surface, and appears frequently in calculations involving the liquid region of the reactor.
- **Subroutine SGRAD**
- A listing of converged reactant concentration $(CP(X/A))$ versus normalized radial distance within the catalyst particle $(X/A)$ at each axial position in the vapor region.
- (a) "CONCENTRATION GRADIENT FOUND AFTER XXX TRIES" \\
(b) "$CP(X)$ AT PARTICLE SURFACE  $.xxxxxx \pm xx$" \\
(c) "KC3* (C13-CPS) = $.xxxxxx \pm xx$" \\
(d) "HC* (T-TPS)= $.xxxxxx \pm xx$"

Print message (a) indicates the number of iterations that were needed to find a converged value for the concentration gradient. 

Print message (b) gives the converged value for the concentration at the particle surface $(c_{p})_{s}$. 

Print messages (c) and (d) give calculated values where KC3 is the mass transfer coefficient for ammonia, CI3 is the interstitial concentration of ammonia at the catalyst surface, HC is the heat transfer coefficient, T is the interstitial temperature, and TPS is the temperature at the surface of the catalyst. 

Print messages (a), (b), (c), and (d) appear at each axial position in the vapor region.
- "SATISFACTORY XO FOUND AFTER XXX TRIES, X0 = $.xxxxxx \pm xx$"

When calculating an ammonia concentration radial profile within a catalyst particle it is necessary to determine the radial depth of penetration of ammonia. The approximate radial position of "zero" concentration is referred to as XO in subroutine SGRAD, and when the iterative procedure employed has successfully determined a value of XO, the above message, with iteration count, is printed.


A sample listing of the output for a typical one-dimensional steady-state data case is shown in Figs. 3a through 3f.	

## Common Operational Problems
Many different data cases have been run with the one-dimensional steady-state computer program. During these runs, most of the problems which have developed have been eliminated through program modification. However, two problems which may still occur are noted below, together with appropriate techniques for solving them.
- "UNABLE TO FIND SUITABLE X0 AFTER FOUR TRIES OF 25 ITERATIONS EACH --- PROGRAM STOP FOLLOWS"

If a satisfactory value for X0 cannot be found after four attempts, this message is printed and program execution is terminated. An appropriate solution to this problem would be to try different values for $f_{i}$ [Eq. (I-11) in discussion of SGRAD, Appendix I]. These values could be greater than 0.95. To make this change, subroutine SGRAD would have to be recompiled using the new values of $f_{i}$.
- "THERE IS A PUDDLE OF COLD HYDRAZINE AT THE LIQUID-VAPOR/VAPOR INTERFACE --- TRY USING A LARGER VALUE FOR G0"

When using a buried injector scheme it is possible to "flood" the region surrounding the injector tip with cold, liquid hydrazine. A sudden drop in axial temperatures at the liquid-vapor/vapor interface indicates that this has occurred, and in such cases the above message in printed and no further calculations are made. An appropriate solution to this problem would be to try a larger input value for GO and rerun the program with the revised input.


## Figures 3a-3f: Listing of Output for Sample Data Case


> [Long table/sample listing omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3.]


	

## Two-Dimensional Steady-State Model

### Input Description
The following is a description of the necessary input for the two-dimensional steady-state computer program.
The input format is given in Table II. The coding of the sample data case for this program is shown in Figs.
4a and 4b, and a listing of the input data punch cards corresponding to this sample data case is shown in Figs.
5a and 5b. The statement numbers in the text below refer to the card numbers (first column) of Table II.
For each run there will be only one card number one. Cards two through twenty-one should be included for each data case to be run.
- The first card contains the number **NCASE**. This number indicates the number of data cases with each run. $1 \le \text{NCASE} \le 999$.
- The second card is the **title card** used for individual data case identification. The title may be any alpha numeric information desired.
- The third card contains the indicators **NRINGS** and **NOFZ**. **NRINGS** indicates the number of evenly spaced radial stations at which calculations are to be made where radial station number one is that one nearest the center of the reactor and radial station number (NRINGS) is that station nearest the reactor wall. For typical runs, **NRINGS** $= 10$ was found adequate to insure good results. Increasing this number would allow more detailed radial analysis, but it would also increase computer run time. **NOFZ** is the number of axial stations (Z's) to be used in the three tables input on cards 10 through 21.
- Cards four contain the values of **F(I)**, (the rates of feed of hydrazine from buried injectors (Ref. 1) into the system in $lb/ft^{3}-sec$). One value of F for each radial station (total number of radial stations = NRINGS) should be input. Ten numbers are allowed to a card. For the suggested NRINGS of 10, there would be one card with ten values of F.
- Cards five contain the values of **GO(I)**, (the inlet mass flow rates in $lb/ft^{2}$-sec) for each radial station. Ten numbers are allowed to a card. For the suggested NRINGS of 10, there would be one card with ten values of GO. All values of GO must be greater than zero.
- Cards six contain the values of **ZO(I)**, (the axial distance to the end of a buried injector in ft) for each radial station. Ten numbers are allowed to a card. For the suggested NRINGS of 10, there would be one card with ten values of ZO.
- The seventh card contains the eight constants **ALPHA3**, **HF**, **R**, **MN2H4**, **MNH3**, **MN2**, **MH2**, and **ALPHAL**.
- **ALPHA3** is the preexponential factor in the rate equation for the thermal decomposition of hydrazine. It equals $2.14 \times 10^{10} sec^{-1}$.
- **HF** is the enthalpy of liquid hydrazine entering the bed in deg R.
- **R** is the gas constant. It equals 10.73 (psia-ft³)/(lb-mole-deg R).
- **MN2H4** is the molecular weight of hydrazine. It equals 32.048 $lb/lb$ mole.
- **MNH3** is the molecular weight of ammonia. It equals $17.032~lb/lb$ mole.
- **MN2** is the molecular weight of nitrogen. It equals $28.016~lb/lb$ mole.
- **MH2** is the molecular weight of hydrogen. It equals 2.016 lb/lb mole.
- **ALPHAL** is the preexponential factor in the rate equation for the catalytic decomposition of hydrazine. For the Shell 405 catalyst it equals $10^{10} sec^{-1}$.
- The eighth card contains the eight constants **ALPHA2**, **AGM**, **BGM**, **KP**, **TF**, **CF**, **NMAX1**, and **NMAX2**.
- **ALPHA2** is the preexponential factor in the rate equation for the catalytic decomposition of ammonia. For the Shell 405 catalyst it equals $10^{11} sec^{-1}$.
- **AGM** is the activation energy for the catalytic decomposition of hydrazine, divided by the gas constant. For the Shell 405 catalyst it equals 2,500 deg R.
- **BGM** is the activation energy for the catalytic decomposition of ammonia, divided by the gas constant. For the Shell 405 catalyst it equals 50,000 deg R.
- **KP** is the effective thermal conductivity of the porous catalyst particle. For the Shell 405 catalyst it equals $0.4 \times 10^{-4}$ Btu/ft-sec-deg R.
- **TF** is the temperature of liquid hydrazine entering the bed in deg R.
- **CF** is the specific heat of liquid hydrazine. It equals 0.7332 Btu/lb-deg R.
- **NMAX1** is the constant used to determine the size of axial station increments in the liquid region. It equals 200. Increasing this number would result in a decrease in size of axial station increments (and an increase in computer run time).
- **NMAX2** is the constant used to determine the size of axial station increments in the liquid-vapor region. It equals 40. Increasing this number would result in a decrease in size of axial station increments (and an increase in computer run time).
- The ninth card contains the inlet value of **P** and five constants **ZEND**, **DON2H4**, **DONH3**, **CGM**, and **RADIUS**.
- **P** is the inlet chamber pressure in psia.
- **ZEND** is the catalyst bed length in feet.
- **DON2H4** is the diffusion coefficient of hydrazine in the gas phase at STP. It equals $0.95 \times 10^{-4} ft^{2}/sec$.
- **DONH3** is the diffusion coefficient of ammonia in the gas phase at STP. It equals $0.17 \times 10^{-3} ft^{2}/sec$.
- **CGM** is the activation energy for the thermal decomposition of hydrazine, divided by the gas constant. It equals 33,000 deg R.
- **RADIUS** is the radius of the catalyst bed in feet.
- Cards ten through thirteen contain **AVSZ(I)**, the bivariate interpolation table used to obtain the catalyst particle radius, $A(z,r)$. These A values are obtained from subroutine UNBAR, an interpolation routine developed at the United Aircraft Research Laboratories, as functions of axial distance, Z, and radial distance, RAD. For this table there should be a total of (NOFZ) Z's, (NRINGS) RAD's and (NOFZ x NRINGS) A's. The table is set up as follows:
- **CARD NO. 10**: This card contains the four table descriptors used by UNBAR. The first descriptor signifies the table number. For this program it equals 0.0. The second descriptor signifies the location in the array at which the table starts; the tables in this program are read in such that this number equals 1.0. The third descriptor for a bivariate table such as this one is the number of elements in the first set of independent variables in the table (in this case, the number of Z's). This number equals NOFZ. The fourth descriptor is the number of elements in the second set of independent variables in the table (in this case, the number of RAD's). This number equals NRINGS.
- **CARD(S) NO. 11**: These cards contain the monatonically increasing Z values. Enough cards should be used to contain NOFZ values of Z at the rate of ten per card. For example, if $NOFZ = 12$, 12 values of Z should be input using 2 cards with ten values on the first card and the 2 remaining values on the second card.
- **CARD(S) NO. 12**: These cards contain the monatonically increasing $RAD$'s. Enough cards should be used to contain NRINGS values of RAD at the rate of ten per card.
- **CARD(S) NO. 13**: These cards contain the values for $A(z,r)$. The A values are input at each Z value for all RAD's (i.e., (NRINGS) values of A for each Z) at the rate of ten per card. (See examples in text).
- Cards 14 through 17 contain **APVSZ(I)**, the bivariate interpolation table used to obtain the catalyst particle surface area, $AP(z,r)$. These AP values are obtained from UNBAR as functions of axial distance, Z, and radial distance, RAD, as in the AVSZ table discussed above. For this table there should be a total of (NOFZ) Z's, (NRINGS) RAD's, and (NOFZ x NRINGS) AP's. The table is set up as follows:
- **CARD NO. 14**: This card is exactly the same as card 10.
- **CARD(S) NO. 15**: These cards are exactly the same as cards 11.
- **CARD(S) NO. 16**: These cards are exactly the same as cards 12.
- **CARD(S) NO. 17**: These cards contain the values for $AP(z,r)$. These values are input at each Z value for all RAD's at the rate of ten values per card. (See examples in the discussion of the AVSZ table as the table setup is the same.)
- Cards 18 through 21 contain **DELVSZ(I)**, the bivariate interpolation table used to obtain the interparticle void fraction, DELTA $(z,r)$.^* These DELTA values are obtained from UNBAR as functions of axial distance, Z, and radial distance, RAD, as in the AVSZ table discussed above. For this table there should be a total of (NOFZ) Z's, (NRINGS) RAD's, and (NOFZ x NRINGS) DELTA's. The table is set up as follows:
- **CARD NO. 18**: This card is exactly the same as card 10.
- **CARD(S) NO. 19**: These cards are exactly the same as cards 11.
- **CARD(S) NO. 20**: These cards are exactly the same as cards 12.
- **CARD(S) NO. 21**: These cards contain the values for DELTA (z,r). These values are input at each Z value for all RAD's at the rate of ten values per card. (See examples in the discussion of the AVSZ table as the table setup is the same).


**NOTE:** The values for the orders of the decomposition reactions (called EN1, EN2, and EN3 in the one-dimensional model) are included in the equations in the two-dimensional model and therefore are not input.

> [Long table/sample listing omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3.]


## List of Symbols


> [Long table/sample listing omitted in milestone-1 markdown. See source: `docs/latex/kesten_1968.tex` section 3.]


## Conversion Notes

- This major section is converted for milestone 1 using the maintained LaTeX transcription source.
- Large tables and print listings are summarized inline for readability, with full source-faithful content preserved in the Fidelity Annex below.
- QA outcome: checklist satisfied for milestone-1 requirements with annex-backed completeness.
- Section status is `reviewed`.

## References

[1] Placeholder (first annual report).
[2] Placeholder (second annual report).
[7] Placeholder (Ergun and related correlations).

## Fidelity Annex (Section 3)

The following source-faithful LaTeX blocks preserve omitted table/listing content for milestone-1 completeness.

### Block A: One-Dimensional Input Format Table
```latex
	\begin{sidewaystable} 
		\centering
		\caption{One-Dimensional Steady-State Computer Program Input Format}
		\label{tab:input1d}
		\begin{tabular}{@{}lllllll@{}}
			\toprule
			CARD & NUMBER & FORMAT & USED & SYMBOL OR & SYMBOL USED & NOMENCLATURE \\
			NUMBER & OF CARDS & FORTRAN & COLUMNS & DESCRIPTION & IN EQUATIONS & \\
			\midrule
			1. & 1 & I3* & 1-3 & NCASE & & No. of cases \\
			2. & 1 & 14A6 & 1-80 & Title & & \\
			3. & 1 & 2I2, I3* & 1-2 & OPTION & & Liq.
			Vap. Indicator \\
			& & & 3-4 & PRINT & & Print Indicator \\
			& & & 5-7 & NOFZ & & No. of Z's in Input Tables \\
			\multicolumn{7}{l}{...} \\
			\multicolumn{7}{p{0.9\textwidth}}{(\textit{Note: The OCR for this table is heavily corrupted. The data must be manually transcribed from the original document.})} \\
			\bottomrule
		\end{tabular}
	\end{sidewaystable}
```

### Block B: Sample Data Case Coding (Figure 1)
```latex
	\begin{sidewaystable}
		\centering
		(NONE OF THIS DATA WAS VERIFIED.  WE JUST COPIED/PASTED FOR NOW.  COME BACK TO THIS AND CHECK THE DATA.)
		\caption{Figure 1: Coding of a Sample Data Case (Reconstructed from Fig. 2)} 
		\label{fig:punchcard}
		\begin{verbatim}
			| Card   | 1.......10........20........30........40........50........60........70........80 |
			|--------|----------------------------------------------------------------------------------|
			| 1      |   1                                                                              |
			| 2      | **SAMPLE DATA CASE (1-DIM SS)** MIXED BED G0= 3.0 P = 100.                       |
			| 3      |  1 0 20                                                                          |
			| 4      | 0.          3.0         0.          .214 E+11  0.          10.73       32.048      17.032 |
			| 5      | 28.016      2.016       1.E+11      1.E+11      2500.       50000.      .40 E-4     33000. |
			| 6      | 530.        .7332       200.        40.         80.         .17 E-3     .95 E-4     100.   |
			| 7      | .25         1.          1.          -1.6                                           |
			| 8      |  .0          1.          20.         0.                                            |
			| 9a     | 0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983 |
			| 9b     | .1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500 |
			| 10a    | .001        .001        .001        .001        .0064       .0064       .0064       .0064       .0064       .0064 |
			| 10b    | .0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064 |
			| 11     |  .0          1.          20.         0.                                            |
			| 12a    | 0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983 |
			| 12b    | .1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500 |
			| 13a    | 2100.       2100.       2100.       2100.       330.        330.        330.        330.        330.        330.  |
			| 13b    | 330.        330.        330.        330.        330.        330.        330.        330.        330.        330.  |
			| 14     |  .0          1.          20.         0.                                            |
			| 15a    | 0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983 |
			| 15b    | .1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500 |
			| 16a    | .34         .34         .34         .34         .34         .34         .34         .34         .34         .34   |
			| 16b    | .34         .34         .34         .34         .34         .34         .34         .34         .34         .34   |
		\end{verbatim}
	\end{sidewaystable}
```

### Block C: Input Data Punch Cards Table
```latex
	\begin{table}[ht]
		\centering
		\caption{Listing of Input Data Punch Cards: Sample Case (from Fig. 2)}
		\label{tab:samplecase}
		\begin{tabular}{@{}ll@{}}
			\toprule
			\textbf{Card Number} & \textbf{Data / Values} \\
			\midrule
			Card 1 & \texttt{  1} \\
			Card 2 & \texttt{**SAMPLE DATA CASE (1-DIM SS)** MIXED BED G0= 3.0 P = 100.} \\
			Card 3 & \texttt{ 1 0 20} \\
			Card 4 & \texttt{0.          3.0         0.          .214 E+11  0.          10.73       32.048      17.032} \\
			Card 5 & \texttt{28.016      2.016       1.E+11      1.E+11      2500.       50000.      .40 E-4     33000.} \\
			Card 6 & \texttt{530.        .7332       200.        40.         80.         .17 E-3     .95 E-4     100.} \\
			Card 7 & \texttt{.25         1.          1.          -1.6} \\
			Card 8 & \texttt{ .0          1.          20.         0.} \\
			Card 9a & \texttt{0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983} \\
			Card 9b & \texttt{.1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500} \\
			Card 10a & \texttt{.001        .001        .001        .001        .0064       .0064       .0064       .0064       .0064       .0064} \\
			Card 10b & \texttt{.0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064       .0064} \\
			Card 11 & \texttt{ .0          1.          20.         0.} \\
			Card 12a & \texttt{0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983} \\
			Card 12b & \texttt{.1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500} \\
			Card 13a & \texttt{2100.       2100.       2100.       2100.       330.        330.        330.        330.        330.        330.} \\
			Card 13b & \texttt{330.        330.        330.        330.        330.        330.        330.        330.        330.        330.} \\
			Card 14 & \texttt{ .0          1.          20.         0.} \\
			Card 15a & \texttt{0.          .0055       .0111       .0167       .0168       .0439       .0575       .0711       .0847       .0983} \\
			Card 15b & \texttt{.1119       .1255       .1391       .1527       .1663       .1799       .1935       .2207       .2343       .2500} \\
			Card 16a & \texttt{.34         .34         .34         .34         .34         .34         .34         .34         .34         .34} \\
			Card 16b & \texttt{.34         .34         .34         .34         .34         .34         .34         .34         .34         .34} \\
			\bottomrule
		\end{tabular}
	\end{table}
```

### Block D: Sample Output Long Listing (Figs. 3a-3f)
```latex
	\begin{longtable}{@{}l@{}} % Defines a one-column longtable
		
		% --- Header for the first page ---
		\caption{Listing of Output for Sample Data Case (Figs. 3a-3f)} \label{fig:outputdata} \\
		\toprule
		\textbf{Sample Data Output} \\
		\midrule
		\endfirsthead
		
		% --- Header for all subsequent pages ---
		\multicolumn{1}{c}%
		{{\tablename\ \thetable{} -- continued from previous page}} \\
		\toprule
		\textbf{Sample Data Output} \\
		\midrule
		\endhead
		
		% --- Footer for all pages except the last ---
		\bottomrule
		\multicolumn{1}{r}{{Continued on next page}} \\
		\endfoot
		
		% --- Footer for the very last page ---
		\bottomrule
		\endlastfoot
		
		% --- Now, the data from the verbatim block ---
		% I've wrapped each line in \texttt{} to keep the monospaced font
		\texttt{**SAMPLE DATA CASE (1-DIM SS)** MIXED BED G0= 3.0 P = 100.} \\
		\texttt{000000} \\
		\texttt{INPUT CONSTANTS} \\
		\texttt{HL         HV         TF         TVAP       CFL        PRESSURE   KP         F          G0} \\
		\texttt{.212628+03 .715478+03 .530000+03 .820000+03 .733200-00 .100000+03 .400000-04 .000000    .300000+01} \\
		\texttt{R          ALPHA3     CGM        DIF3       DIF4       WM4        WM3        WM2        WM1        ZEND} \\
		\texttt{.107300+02 .214000+11 .330000+05 .170000-03 .950000-04 .320480+02 .170320+02 .280160+02 .201600+01 .250000+00} \\
		\texttt{AGM        BGM        ALPHA1     ALPHA2     N1         N2         N3         ENMX1      ENMX2      ENMX3} \\
		\texttt{.250000+04 .500000+05 .100000+12 .100000+11 .100000+01 .100000+01 -.160000+01 .200000+03 .400000+02 .800000+02} \\
		\texttt{000000} \\
		\texttt{ZO} \\
		\texttt{.000000} \\
		\texttt{Z VS A TABLE} \\
		\texttt{.000000    .100000+01 .200000+02 .000000} \\
		\texttt{.000000    .550000-02 .111000-01 .167000-01 .168000-01 .439000-01 .575000-01 .711000-01 .847000-01 .983000-01} \\
		\texttt{.111900+00 .125500+00 .139100+00 .152700+00 .166300+00 .179900+00 .193500+00 .207100+00 .220700+00 .234300+00} \\
		\texttt{.100000-02 .100000-02 .100000-02 .100000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02} \\
		\texttt{.640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02 .640000-02} \\
		\texttt{Z VS AP TABLE} \\
		\texttt{.000000    .100000+01 .200000+02 .000000} \\
		\texttt{.000000    .550000-02 .111000-01 .167000-01 .168000-01 .439000-01 .575000-01 .711000-01 .847000-01 .983000-01} \\
		\texttt{.111900+00 .125500+00 .139100+00 .152700+00 .166300+00 .179900+00 .193500+00 .207100+00 .220700+00 .234300+00} \\
		\texttt{.210000+04 .210000+04 .210000+04 .210000+04 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03} \\
		\texttt{.330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03 .330000+03} \\
		\texttt{Z VS DELTA TABLE} \\
		\texttt{.000000    .100000+01 .200000+02 .000000} \\
		\texttt{.000000    .550000-02 .111000-01 .167000-01 .168000-01 .439000-01 .575000-01 .711000-01 .847000-01 .983000-01} \\
		\texttt{.111900+00 .125500+00 .139100+00 .152700+00 .166300+00 .179900+00 .193500+00 .207100+00 .220700+00 .234300+00} \\
		\texttt{.340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00} \\
		\texttt{.340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00 .340000-00} \\
		~\\ % Adds a little space
		\texttt{******************************* ENTERING LIQUID REGION *******************************} \\
		~\\
		\texttt{                   Z              TEMP              H              DHDZ} \\
		\texttt{.00000000      .530000+03      .000000        .377541+05} \\
		\texttt{.251216-03     .542936+03      .189619+02     .538926+05} \\
		\texttt{.484469-03     .555662+03      .379026+02     .945157+05} \\
		\texttt{.527298-03     .568781+03      .568781+02     .343787+06} \\
		\texttt{.593145-03     .581695+03      .757274+02     .221126+06} \\
		\texttt{.635941-03     .594602+03      .946115+02     .322530+06} \\
		\texttt{.665267-03     .607502+03      .113477+03     .467775+06} \\
		\texttt{.665477-03     .620396+03      .132323+03     .675305+06} \\
		\texttt{.699470-03     .633283+03      .151168+03     .962125+06} \\
		\texttt{.709286-03     .646164+03      .169992+03     .132107+07} \\
		\texttt{.716432-03     .659039+03      .188824+03     .183241+07} \\
		\texttt{.721580-03     .671907+03      .207641+03     .242181+07} \\
		\texttt{.725474-03     .684769+03      .226450+03     .316562+07} \\
		\texttt{.728452-03     .697625+03      .245250+03     .412827+07} \\
		\texttt{.730734-03     .710474+03      .264042+03     .577362+07} \\
		\texttt{.732365-03     .723316+03      .282827+03     .750974+07} \\
		\texttt{.733618-03     .736154+03      .301605+03     .935122+07} \\
		\texttt{.734627-03     .748989+03      .320377+03     .117621+08} \\
		\texttt{.735427-03     .761822+03      .339146+03     .151422+08} \\
		\texttt{.736046-03     .774653+03      .357912+03     .187859+08} \\
		\texttt{.736547-03     .787482+03      .376676+03     .225211+08} \\
		\texttt{.736964-03     .800310+03      .395438+03     .269846+08} \\
		\texttt{.737323-03     .813133+03      .414199+03     .342904+08} \\
		\texttt{.737459-03     .820000+03      .423306+03     .383323+08} \\
		~\\
		\texttt{*************************** ENTERING LIQUID VAPOR REGION ***************************} \\
		~\\
		\texttt{.73770-03     .82000+03      .25963+03      .093472-01} \\
		\texttt{.73895-03     .82000+03      .30663+03      .18594-00} \\
		\texttt{.74016-03     .82000+03      .35363+03      .28041-00} \\
		\texttt{.74138-03     .82000+03      .40064+03      .37389-00} \\
		\texttt{.74261-03     .82000+03      .44764+03      .46796-00} \\
		\texttt{.74384-03     .82000+03      .49464+03      .56083-00} \\
		\texttt{.74506-03     .82000+03      .54164+03      .65430-00} \\
		\texttt{.74629-03     .82000+03      .58865+03      .74777-00} \\
		\texttt{.74751-03     .82000+03      .63565+03      .84124-00} \\
		\texttt{.74874-03     .82000+03      .68265+03      .93472-00} \\
		\texttt{.75082-03     .82000+03      .71548+03      .10000+01} \\
		~\\
		\texttt{***************************** ENTERING VAPOR REGION *****************************} \\
		~\\
		\texttt{Z= .075082274-03 TEMP= .82000000+03 PRES= .10000000+03 H= .71547795+03} \\
		\texttt{C1= .31579918-02 C2= .43586062-01 C3= .53360037-01 C4= .10343207-00} \\
		\texttt{MFRAC1= .13782692-00 MFRAC2= .13782692-00 MFRAC3= .27565384-00 MFRAC4= .44869231-00 FRAC3D= -.00000000} \\
		~\\
		\texttt{Z= .090740574-03 TEMP= .86645369+03 PRES= .99981377+02 H= .73897909+03} \\
		\texttt{C1= .32506140-02 C2= .43334669-01 C3= .50454650-01 C4= .15041867-00} \\
		\texttt{MFRAC1= .14429730-00 MFRAC2= .14429730-00 MFRAC3= .27635187-00 MFRAC4= .42893217-00 FRAC3D= .21670607-01} \\
		~\\
		\texttt{Z= .10665796-02 TEMP= .91158767+03 PRES= .99960899+02 H= .76246590+03} \\
		\texttt{C1= .33173617-02 C2= .42790974-01 C3= .48003883-01 C4= .13356108-00} \\
		\texttt{MFRAC1= .16197901-00 MFRAC2= .15034878-00 MFRAC3= .27743711-00 MFRAC4= .41023511-00 FRAC3D= .40233626-01} \\
		~\\
		\texttt{Z= .12278735-02 TEMP= .95559712+03 PRES= .99938571+02 H= .78594348+03} \\
		\texttt{C1= .33603019-02 C2= .42236826-01 C3= .45931103-01 C4= .12162228+00} \\
		\texttt{MFRAC1= .17243814-00 MFRAC2= .15596628-00 MFRAC3= .27898882-00 MFRAC4= .39260677-00 FRAC3D= .55749761-01} \\
		~\\
		\texttt{... (Data continues) ...} \\
		~\\
		\texttt{Z= .17155202-00 TEMP= .19507243+04 PRES= .78863929+02 H= .14092872+04} \\
		\texttt{C1= .39661221-02 C2= .31522408-01 C3= .96198352-02 C4= .00000000} \\
		\texttt{MFRAC1= .53774555-00 MFRAC2= .30754914-00 MFRAC3= .15470531-00 MFRAC4= .00000000     FRAC3D= .59806513-00} \\
		~\\
		\texttt{Z= .24999999-00 TEMP= .19053842+04 PRES= .71680713+02 H= .13780029+04} \\
		\texttt{C1= .38096090-02 C2= .29667359-01 C3= .77733879-02 C4= .00000000} \\
		\texttt{MFRAC1= .55496938-00 MFRAC2= .31099591-00 MFRAC3= .13403673-00 MFRAC4= .00000000     FRAC3D= .64541664-00} \\
		~\\
		\texttt{Z'S FROM VAPOR REGION} \\
		\texttt{.7508227-03 .9074057-03 .1066580-02 .1227874-02 .1392110-02 .1559678-02 .1730142-02 .1905576-02 .2084807-02 .2269192-02} \\
		\texttt{.2459069-02 .2655209-02 .2858234-02 .3068889-02 .3288960-02 .3518443-02 .3755323-02 .4005866-02 .4269697-02 .4547898-02} \\
		\texttt{.4844697-02 .5157416-02 .5493968-02 .5856722-02 .6249363-02 .6676468-02 .7151910-02 .7680163-02 .8278725-02 .8971330-02} \\
		\texttt{.9737482-02 .1083580-01 .1225605-01 .1392110-01 .1465606-01 .1476369-01 .1487130-01 .1497891-01 .1508652-01 .1519400-01} \\
		\texttt{.1530174-01 .1540940-01 .1552457-01 .1659306-01 .1756156-01 .2046704-01 .2337252-01 .4080540-01 .6695473-01 .9310405-01} \\
		\texttt{.1194060-00 .1323280-00 .1715520-00 .1911640-00 .2107760-00 .2303880-00 .2500000-00} \\
		~\\
		\texttt{STEADY STATE VALUES FOR MBAR AND G AT END OF BED} \\
		\texttt{        MBAR= .12115+02     G= .30000+01} \\
		~\\
		\texttt{***** OPERATIONS COMPLETE *****} \\
		
	\end{longtable}
```

### Block E: Two-Dimensional Input Format (Table II)
```latex
		\begin{longtable}{@{}llll >{\raggedright\arraybackslash}p{0.25\textwidth} >{\raggedright\arraybackslash}p{0.15\textwidth} >{\raggedright\arraybackslash}p{0.35\textwidth}@{}}
			% --- END FIX ---
			
			% --- CAPTION AND HEADERS FOR FIRST PAGE ---
			\caption{Two-Dimensional Computer Program: Input Format (Table II)} \label{tab:input2d} \\
			\toprule
			CARD & NUMBER & FORMAT & USED & SYMBOL OR & SYMBOL USED & NOMENCLATURE \\
			NUMBER & OF CARDS & FORTRAN & COLUMNS & DESCRIPTION & IN EQUATIONS & \\
			\midrule
			\endfirsthead
			
			% --- HEADERS FOR CONTINUATION PAGES ---
			\multicolumn{7}{c}%
			{{\tablename\ \thetable{} -- continued from previous page}} \\
			\toprule
			CARD & NUMBER & FORMAT & USED & SYMBOL OR & SYMBOL USED & NOMENCLATURE \\
			NUMBER & OF CARDS & FORTRAN & COLUMNS & DESCRIPTION & IN EQUATIONS & \\
			\midrule
			\endhead
			
			% --- FOOTER FOR ALL PAGES EXCEPT LAST ---
			\midrule
			\multicolumn{7}{r}{{Continued on next page}} \\
			\endfoot
			
			% --- FOOTER FOR THE LAST PAGE ---
			\bottomrule
			\multicolumn{7}{@{}p{0.9\textwidth}@{}}{% <--- Adjusted width here too
				*All I format numbers should be right adjusted. \par
				**Enough cards should be used to contain (NRINGS) values at the rate of ten per card. \par
				***Enough cards should be used to contain (NRINGS) values for each Z at the rate of ten per card (see detailed example in text).
			}
			\endlastfoot
			
			% --- TABLE BODY ---
			1 & 1 & I3* & 1-3 & NCASE & & Number of data cases \\
			2 & 1 & 14A6 & 1-80 & Title & & \\
			3 & 1 & 2I3* & 1-3 & NRINGS & & Number of radial stations \\
			& & & 4-6 & NOFZ & & Number of Z's in input tables \\
			4 & ** & 10E8.4 & 1-8, 9-16, etc. & F(I) & $F$ & Distributed Feed Rate \\
			5 & ** & 10E8.4 & 1-8, 9-16, etc. & GO(I) & $G_0$ & Inlet mass flow rate \\
			6 & ** & 10E8.4 & 1-8, 9-16, etc. & ZO(I) & $Z_0$ & Axial distance to injector end \\
			7 & 1 & 8E10.5 & 1-10 & ALPHA3 & $\alpha_{hom}$ & Constant in rate equation \\
			& & & 11-20 & HF & $h_F$ & Enthalpy of feed \\
			& & & 21-30 & R & $R$ & Gas constant \\
			& & & 31-40 & MN2H4 & $M^{N2H4}$ & Molecular weight of N2H4 \\
			& & & 41-50 & MNH3 & $M^{NH3}$ & Molecular weight of NH3 \\
			& & & 51-60 & MN2 & $M^{N2}$ & Molecular weight of N2 \\
			& & & 61-70 & MH2 & $M^{H2}$ & Molecular weight of H2 \\
			& & & 71-80 & ALPHAL & $\alpha_{het}^{N2H4}$ & Preexponential factor \\
			8 & 1 & 8E10.5 & 1-10 & ALPHA2 & $\alpha_{het}^{NH3}$ & Preexponential factor \\
			& & & 11-20 & AGM & $Q_{het}^{N2H4}/R$ & Activation energy, deg R \\
			& & & 21-30 & BGM & $Q_{het}^{NH3}/R$ & Activation energy, deg R \\
			& & & 31-40 & KP & $K_p$ & Thermal conductivity \\
			& & & 41-50 & TF & $T_F$ & Feed temperature \\
			& & & 51-60 & CF & $C_F$ & Specific heat of liquid N2H4 \\
			& & & 61-70 & NMAX1 & & Determ. axial step size (liq. reg.) \\
			& & & 71-80 & NMAX2 & & Determ. axial step size (liq. vap. reg.) \\
			9 & 1 & 8E10.5 & 1-10 & P & $P$ & Inlet chamber pressure \\
			& & & 11-20 & ZEND & & Bed length \\
			& & & 21-30 & DON2H4 & $D_0^{N2H4}$ & Diffusion coefficient of N2H4 \\
			& & & 31-40 & DONH3 & $D_0^{NH3}$ & Diffusion coefficient of NH3 \\
			& & & 41-50 & CGM & $Q_{hom}^{N2H4}/R$ & Activation energy, deg R \\
			& & & 51-60 & RADIUS & & Bed radius \\
			10 & 1 & 4E8.4 & 1-8 & 0. & & Table descriptor \\
			& & & 9-16 & 1. & & Table descriptor \\
			& & & 17-24 & NOFZ. & & Table descriptor \\
			& & & 25-32 & NRINGS. & & Table descriptor \\
			11 & * & 10E8.4 & 1-8, 9-16, etc. & Z(I) & $Z$ & Axial station \\
			12 & ** & 10E8.4 & 1-8, 9-16, etc. & RAD(I) & $r$ & Radial station \\
			13 & *** & 10E8.4 & 1-8, 9-16, etc. & A(z,r) & $a$ & Catalyst particle radius \\
			14 & 1 & 4E8.4 & 1-8 & 0. & & Table descriptor \\
			& & & 9-16 & 1. & & Table descriptor \\
			& & & 17-24 & NOFZ. & & Table descriptor \\
			& & & 25-32 & NRINGS. & & Table descriptor \\
			15 & * & 10E8.4 & 1-8, 9-16, etc. & Z(I) & $Z$ & Axial station \\
			16 & ** & 10E8.4 & 1-8, 9-16, etc. & RAD(I) & $r$ & Radial station \\
			17 & *** & 10E8.4 & 1-8, 9-16, etc. & AP(z,r) & $A_p$ & Total external catalyst particle surface area per unit volume of bed \\
			18 & 1 & 4E8.4 & 1-8 & 0. & & Table descriptor \\
			& & & 9-16 & 1. & & Table descriptor \\
			& & & 17-24 & NOFZ. & & Table descriptor \\
			& & & 25-32 & NRINGS. & & Table descriptor \\
			19 & * & 10E8.4 & 1-8, 9-16, etc. & Z(I) & $Z$ & Axial station \\
			20 & ** & 10E8.4 & 1-8, 9-16, etc. & RAD(I) & $r$ & Radial station \\
			21 & *** & 10E8.4 & 1-8, 9-16, etc. & DELTA(z,r) & $\delta$ & Interparticle void fraction \\
			
		\end{longtable}
```

### Block F: List of Symbols Table
```latex
	\begin{longtable}{@{}p{1in}p{5in}@{}}
		\toprule
		\textbf{Symbol} & \textbf{Description} \\
		\midrule
		\endfirsthead
		
		\multicolumn{2}{c}%
		{{\tablename\ \thetable{} -- continued from previous page}} \\
		\toprule
		\textbf{Symbol} & \textbf{Description} \\
		\midrule
		\endhead
		
		\bottomrule
		\multicolumn{2}{r}{{Continued on next page}} \\
		\endfoot
		
		\bottomrule
		\endlastfoot
		
		% --- Page 62 Data ---
		$a$ & Radius of spherical particle, ft \\
		$A_{p}$ & Total external surface of catalyst particle per unit volume of bed, $ft^{-1}$ \\
		$c_{i}$ & Reactant concentration in interstitial fluid, $lb/ft^{3}$ \\
		$c_{p}$ & Reactant concentration in gas phase within the porous particle, $lb/ft^{3}$ \\
		$C_{F}$ & Specific heat of fluid in the interstitial phase, $Btu/lb$ deg R \\
		$\overline{C}_{F}$ & Average specific heat of fluid in the interstitial phase, Btu/lb deg R \\
		$D_{i}$ & Diffusion coefficient of reactant gas in the interstitial fluid, $ft^{2}/sec$ \\
		$D_{0}$ & Diffusion coefficient of reactant gas in the interstitial fluid at STP, $ft^{2}/sec$ \\
		$D_{p}$ & Diffusion coefficient of reactant gas in the porous particle, $ft^{2}/sec$ \\
		$f_{i}$ & Weighting factor in Eq. (I-11) \\
		$F$ & Rate of feed of hydrazine from buried injectors into the system (Ref. 1), $lb/ft^{3}-sec$ \\
		$g_{c}$ & Conversion factor, (lbm/lbe) $ft/sec^{2}$ \\
		$G$ & Mass flow rate, $lb/ft^{2}-sec$ \\
		$h$ & Enthalpy, $Btu/lb$ \\
		$h_{c}$ & Heat transfer coefficient, $Btu/ft^{2}$-sec-deg R \\
		$H$ & Heat of reaction (negative for exothermic reaction), $Btu/lb$ \\
		$k_{c}$ & Mass transfer coefficient, $ft/sec$ \\
		$k_{0}$ & Reaction rate constant, equals $\alpha e^{-\gamma}$ \\
		$K_{p}$ & Thermal conductivity of the porous catalyst particle, Btu/ft-sec-deg R \\
		
		% --- Page 63 Data ---
		$M$ & Molecular weight, lb/lb mole \\
		$\overline{M}$ & Average molecular weight, $lb/lb$ mole \\
		$n$ & Order of decomposition reaction \\
		$N_{r}$ & Radial mass flux, $lb/ft^{2}$-sec \\
		$P$ & Chamber pressure, psia \\
		$q_{r}$ & Radial heat flux, $Btu/ft^{2}-sec$ \\
		$Q_{het}$ & Activation energy for (heterogeneous) chemical reaction on the catalyst surfaces, $Btu/lb$ mole \\
		$Q_{hom}$ & Activation energy for (homogeneous) chemical reaction in the interstitial phase, $Btu/lb$ mole \\
		$r$ & Radial distance from the center of the cylindrical reaction chamber, ft \\
		$r_{het}$ & Rate of (heterogeneous) chemical reaction on the catalyst surfaces, $lb/ft^{3}-sec$ \\
		$r_{hom}$ & Rate of (homogeneous) chemical reaction in the interstitial phase, $lb/ft^{3}-sec$ \\
		$R$ & Gas constant, equals 10.73 psia $ft^{3}/lb$ mole deg R, or, Radius of reactor \\
		$T$ & Temperature, deg R \\
		$T_{vap}$ & Vaporization temperature, deg R \\
		$w_{i}$ & Weight fraction of reactant in interstitial phase \\
		$x$ & Radial distance from the center of the spherical catalyst particle, ft \\
		$x_{0}$ & Defined in Appendix I (Discussion of Subroutine SGRAD) \\
		$z$ & Axial distance, ft \\
		$z_{0}$ & Axial distance to the end of buried injectors, ft \\
		$\alpha$ & Preexponential factor in rate equation \\
		
		% --- Page 64 Data ---
		$\beta$ & Equals $[-(c_{p})_{s} H D_{p}]/[{K_{p}(T_{p})_{s}}]$ \\
		$\gamma$ & Equals $Q_{het}/[R (T_{p})_{s}]$ \\
		$\delta$ & Interparticle void fraction \\
		$\epsilon$ & Eddy diffusivity, $ft^{2}/sec$ \\
		$\lambda$ & Eddy conductivity, Btu/ft-sec-deg R \\
		$\mu$ & Viscosity of interstitial fluid, lb/ft sec \\
		$\rho_{i}$ & Density of interstitial fluid, $lb/ft^{3}$ \\
		\midrule
		\multicolumn{2}{l}{\textbf{Subscripts}} \\
		\midrule
		$F$ & Refers to feed \\
		$i$ & Refers to interstitial phase \\
		$P$ & Refers to gas within the porous catalyst particle \\
		$s$ & Refers to surface of catalyst particle \\
		\midrule
		\multicolumn{2}{l}{\textbf{Superscripts}} \\
		\midrule
		$j$ & Refers to chemical species \\
		$L$ & Refers to liquid at vaporization temperature \\
		$V$ & Refers to vapor at vaporization temperature \\
		
	\end{longtable}
```
