
cd "/Users/anyamarchenko/CEGA Dropbox/Anya Marchenko/frontier_ceos_data/"

import delimited "clean_data/county_ceo.csv", clear 

drop v1

* Alabama Arizona Arkansas California Colorado Connecticut are all 4 digit fips
* Usually coded as five digit with leading zero
* Need to add 0 to their fips to merge
tostring fips, replace

gen leadzero = "0"
replace fips = leadzero + fips if statename == "Alabama" | statename == "Arkansas" | statename == "Arizona" | statename == "California" | statename == "Colorado" | statename == "Connecticut"

* Merge in population
merge 1:m fips using "raw_data/cencounts.dta"

* use "raw_data/cencounts.dta", clear 

gen ceos_norm = num_ceos / pop1900
replace ceos_norm = ceos_norm*10000

********************************************************************************

reg num_ceos tfe pop1900, robust
eststo a

reg num_ceos tfe pop1900, robust cluster(fips)
eststo b

poisson num_ceos tfe  pop1900, vce(robust) irr //reports estimated coefficients transformed to incidence-rate ratios
eststo c

nbreg num_ceos tfe pop1900, vce(robust)
eststo d

reg ceos_norm tfe pop1900, robust
eststo e

estout a b c d e using "/Users/anyamarchenko/CEGA Dropbox/Anya Marchenko/Apps/Overleaf/homestead/tables/table1.tex", style(tex) replace label starlevels(* .1 ** .05 *** .01 ) cells("b(fmt(4)star)" "se(fmt(4)par)") ///
	eqlabels(none) collabels(none) mlabels("OLS" "OLS, county clustered" "Poisson" "Neg Binomial" "Normalized by pop") mgroups(none) ///
	nobaselevels noomitted /// //this omits the baselevels of factor variables
	stats(N r2,  /// 
	labels(`"Observations"' `" \(R^{2}\)"') fmt(%9.0fc 3)) ///
	prehead("\begin{tabular}{l*{@E}{c}}" ///
	"\toprule")  ///
	posthead("\midrule") ///
	prefoot("\\" "\midrule" "\multicolumn{1}{c}{}\\")   ///
	postfoot("\bottomrule" "\end{tabular}")
		
	cap n estimates clear 


/*
- among equally small places, is tfe predictive 
- creating synthetic controls for counties 
- look at mining places with mining endowmnets and historical mining / oil deposits. look at high tfe places with resource endowments and low tfe places with resource endowments, see if they produced more of these star guys. 
- control for population (1) - (4). 
- create a line graph / scatterplot with counties. x is tfe and y = number entrepreneurs. each dot is a county. 
*/

sum pop1900, d
* For small places, the correlation b/w tfe and # ents is positive 
reg num_ceos tfe lnpop if pop1900 < `r(p25)', robust











