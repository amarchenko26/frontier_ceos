

********************************************************************************
* Set up
********************************************************************************

cd "/Users/anyamarchenko/CEGA Dropbox/Anya Marchenko/frontier_ceos_data/"

import delimited "clean_data/county_df.csv", clear 
la var tfe "Frontier Exposure"
la var pop1950 "Pop 1950"

gen lnpop = ln(pop1950)
la var lnpop "Ln(Pop 1950)"

* Drop extra var from Python
drop v1
tostring fips, replace

* Alabama Arizona Arkansas California Colorado Connecticut are all 4 digit fips
* Usually coded as five digit with leading zero
* Need to add 0 to their fips to merge
gen leadzero = "0"
replace fips = leadzero + fips if statename == "Alabama" | statename == "Arkansas" | statename == "Arizona" | statename == "California" | statename == "Colorado" | statename == "Connecticut"

********************************************************************************
* Scatterplot of CEOs vs. TFE
********************************************************************************

preserve
drop if ceos_norm == 0 //Remove counties with no CEOs

twoway scatter ceos_norm tfe || lfit ceos_norm tfe, title("Number CEOs per 10,000 people versus TFE (excluding zeroes)") legend(position(6))

graph export "/Users/anyamarchenko/Documents/GitHub/frontier_ceos/output/figures/scatter.png", as(png) replace

restore


********************************************************************************
* Regression - OLS
********************************************************************************

estimates clear

reg num_ceos tfe, robust cluster(fips)
eststo a

reg num_ceos c.tfe##c.pop1950, robust cluster(fips)
eststo b

reg ceos_norm c.tfe##c.pop1950, robust cluster(fips)
eststo c

reg ceos_norm c.tfe##c.lnpop, robust cluster(fips)
eststo d

reg ceos_norm c.tfe##c.lnpop i.statea, robust cluster(fips)
eststo e

sum pop1950, d
* For small places, the correlation b/w tfe and # ents is positive 
	reg ceos_norm tfe lnpop if pop1950 < `r(p25)', robust cluster(fips)
	eststo f

preserve 
* keep only states that have TFE info for all counties
	keep if statename == "Minnesota" | statename == "Iowa" | statename == "Missouri" | statename == "Michigan" | statename == "Arkansas" | statename == "Louisiana" | statename == "Mississippi" | statename == "Alabama" | statename == "Florida" | statename == "Tennessee" | statename == "Kentucky" | statename == "Ohio" | statename == "Indiana" | statename == "Illinois" | statename == "Wisconsin"
	reg ceos_norm c.tfe##c.pop1950, robust cluster(fips)
	eststo g
restore 

preserve 
* keep only resource endowment industries 
	keep if agricultureandmining == 1 | metals == 1 | woodpaperforestry == 1 | utilitiesenergy== 1 | constructionrealestate == 1
	reg ceos_norm c.tfe##c.lnpop, robust cluster(fips)
	eststo h
restore 


preserve 
* keep resource endowment industries + hospitality 
	keep if agricultureandmining == 1 | metals == 1 | woodpaperforestry == 1 | utilitiesenergy== 1 | constructionrealestate == 1 | foodtobacco == 1 | restaurantslodging == 1
	reg ceos_norm c.tfe##c.lnpop, robust cluster(fips)
	eststo i
restore 

estout a b c d e f g h i using "/Users/anyamarchenko/Documents/GitHub/frontier_ceos/output/tables/table1.tex", style(tex) replace label starlevels(* .1 ** .05 *** .01 ) cells("b(fmt(4)star)" "se(fmt(4)par)") ///
	eqlabels(none) collabels(none) mlabels(none) mgroups(none) ///
	drop(*.statea _cons) ///
	stats(N r2,  /// 
	labels(`"Observations"' `" \(R^{2}\)"') fmt(%9.0fc 3)) ///
	prehead("\begin{tabular}{l*{@E}{c}}" ///
	"\toprule" ///
	"& \multicolumn{2}{c}{|--------- \textbf{CEO counts} --------|}  & \multicolumn{7}{c}{---------------------------------------------------- \textbf{CEOs per 10,000 people} -------------------------------------------} \\ & All counties & All counties & All counties & All counties & All counties (State FE) & \multicolumn{1}{c}{\shortstack{Small \\ counties}} & \multicolumn{1}{c}{\shortstack{Core \\ states}} & \multicolumn{1}{c}{\shortstack{Resource \\ Industries}} &\multicolumn{1}{c}{\shortstack{Resource + Hospitality \\ Industries}}   \\")  ///
	posthead("\midrule") ///
	prefoot("\\" "\midrule" "\multicolumn{1}{c}{}\\")   ///
	postfoot("\bottomrule" "\end{tabular}")
				

********************************************************************************
* Regression - POISSON
********************************************************************************


estimates clear

poisson num_ceos tfe, robust cluster(fips)
eststo a

poisson num_ceos c.tfe##c.pop1950, robust cluster(fips)
eststo b

poisson ceos_norm c.tfe##c.pop1950, robust cluster(fips)
eststo c

poisson ceos_norm c.tfe##c.lnpop, robust cluster(fips)
eststo d

poisson ceos_norm c.tfe##c.lnpop i.statea, robust cluster(fips)
eststo e

sum pop1950, d
* For small places, the correlation b/w tfe and # ents is positive 
	poisson ceos_norm tfe lnpop if pop1950 < `r(p25)', robust cluster(fips)
	eststo f

preserve 
* keep only states that have TFE info for all counties
	keep if statename == "Minnesota" | statename == "Iowa" | statename == "Missouri" | statename == "Michigan" | statename == "Arkansas" | statename == "Louisiana" | statename == "Mississippi" | statename == "Alabama" | statename == "Florida" | statename == "Tennessee" | statename == "Kentucky" | statename == "Ohio" | statename == "Indiana" | statename == "Illinois" | statename == "Wisconsin"
	poisson ceos_norm c.tfe##c.pop1950, robust cluster(fips)
	eststo g
restore 

preserve 
* keep only resource endowment industries 
	keep if agricultureandmining == 1 | metals == 1 | woodpaperforestry == 1 | utilitiesenergy== 1 | constructionrealestate == 1
	poisson ceos_norm c.tfe##c.lnpop, robust cluster(fips)
	eststo h
restore 


preserve 
* keep resource endowment industries + hospitality 
	keep if agricultureandmining == 1 | metals == 1 | woodpaperforestry == 1 | utilitiesenergy== 1 | constructionrealestate == 1 | foodtobacco == 1 | restaurantslodging == 1
	poisson ceos_norm c.tfe##c.lnpop, robust cluster(fips)
	eststo i
restore 

estout a b c d e f g h i using "/Users/anyamarchenko/Documents/GitHub/frontier_ceos/output/tables/table1_poisson.tex", style(tex) replace label starlevels(* .1 ** .05 *** .01 ) cells("b(fmt(4)star)" "se(fmt(4)par)") ///
	eqlabels(none) collabels(none) mlabels(none) mgroups(none) ///
	drop(*.statea _cons) ///
	stats(N r2,  /// 
	labels(`"Observations"' `" \(R^{2}\)"') fmt(%9.0fc 3)) ///
	prehead("\begin{tabular}{l*{@E}{c}}" ///
	"\toprule" ///
	"& \multicolumn{2}{c}{|--------- \textbf{CEO counts} --------|}  & \multicolumn{7}{c}{--------------------------------------------- \textbf{CEOs per 10,000 people} -------------------------------------------} \\ & All counties & All counties & All counties & All counties & All counties (State FE) & \multicolumn{1}{c}{\shortstack{Small \\ counties}} & \multicolumn{1}{c}{\shortstack{Core \\ states}} & \multicolumn{1}{c}{\shortstack{Resource \\ Industries}} &\multicolumn{1}{c}{\shortstack{Resource + Hospitality \\ Industries}}   \\")  ///
	posthead("\midrule") ///
	prefoot("\\" "\midrule" "\multicolumn{1}{c}{}\\")   ///
	postfoot("\bottomrule" "\end{tabular}")

		
/*
- among equally small places, is tfe predictive 
- creating synthetic controls for counties 
- look at mining places with mining endowmnets and historical mining / oil deposits. look at high tfe places with resource endowments and low tfe places with resource endowments, see if they produced more of these star guys. 
*/












