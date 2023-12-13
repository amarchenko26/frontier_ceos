#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:27:25 2023

@author: anyamarchenko
"""

import pandas as pd


literacy = pd.read_excel("/Users/anyamarchenko/CEGA Dropbox/Anya Marchenko/frontier_ceos_data/raw_data/literacy_by_county.xlsx")

literacy.rename(columns={'FIPS_code': 'FIPS'}, inplace=True)

literacy['FIPS'] = literacy['FIPS'].astype(str)

# Add leading zero to standardize all FIPS
literacy['FIPS'] = literacy['FIPS'].apply(lambda x: '0' + x if len(x) == 4 else x)


literacy_corr = pd.merge(county_ceo, literacy, how='left', on='FIPS')

correlation = literacy_corr['tfe'].corr(literacy_corr['Lit_A'])



core_tfe_states = ["Minnesota", "Iowa", "Missouri", "Michigan", "Arkansas", "Louisiana", "Mississippi", "Alabama", "Florida", "Tennessee", "Kentucky", "Ohio", "Indiana", "Illinois", "Wisconsin"]
counties_core_only = county_ceo[county_ceo['statename'].isin(core_tfe_states)]



literacy_corr = pd.merge(counties_core_only, literacy, how='left', on='FIPS')

correlation = literacy_corr['tfe'].corr(literacy_corr['Lit_A'])


print("Correlation between 'tfe' and 'Lit_A':", correlation)