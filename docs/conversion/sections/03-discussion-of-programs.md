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
- Large tables and print listings were collapsed to placeholders for readability; detailed fidelity review remains.
- Section status is `converted` pending full QA checklist sign-off.

## References

[1] Placeholder (first annual report).
[2] Placeholder (second annual report).
[7] Placeholder (Ergun and related correlations).
