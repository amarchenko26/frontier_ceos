#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:02:08 2023

@author: anyamarchenko
"""

import pandas as pd
import numpy as np
import addfips
import os


# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)

######## Load data ############################################################

# Load the Excel file
file_path = 'data/raw_data/entrepreneurs_master.xlsx'
ceo_df = pd.read_excel(file_path, sheet_name = 'master')


######## Remove foreign countries ######################################

# List of countries to filter out
countries_to_filter = ["Australia", "Austria", "Belgium", "Canada", "China", "Cuba", "England", "France", "Germany",
                       "Germany (Prussia)", "Hawaii", "Hungary", "Ireland", "Norway", "Poland", "Rumania", "Russia",
                       "Scotland", "Sweden", "Switzerland", "Turkey", "Virgin Islands"]

# Filtering the DataFrame
ceo_df = ceo_df[~ceo_df['Birthstate'].isin(countries_to_filter)]



######## Merge in FIPS codes ##################################################

# Create an instance of the addfips.AddFIPS class
af = addfips.AddFIPS()

def assign_fips(row):
    try:
        # Get the FIPS code
        fips_code = af.get_county_fips(row['Birthcounty'], state=row['Birthstate'])
        return fips_code
    except Exception as e:
        # Handle any exception (e.g., county/state not found)
        print(f"Error for row {row}: {e}")
        return None

# Apply the function to each row
ceo_df['FIPS'] = ceo_df.apply(assign_fips, axis=1)


######## Merge in TFE to ceo_df ###############################################

# Read in TFE .dta from Bazzi et al. ECMA (2020) 
tfe = pd.read_stata("data/raw_data/proptaxvote.dta")

# Rename cols for merge
tfe.rename(columns={'fips': 'FIPS', 'tye_tfe890_500kNI_100_l6': 'tfe'}, inplace=True)

# Convert FIPS to strings in both df to avoid merge error
tfe['FIPS'] = tfe['FIPS'].astype(str)
ceo_df['FIPS'] = ceo_df['FIPS'].astype(str)

ceo_df = pd.merge(ceo_df, tfe[['FIPS', 'tfe']], how = 'left', on ='FIPS')

######## Assign average TFE in birth state to missing values

# Create a dictionary mapping state names to their average TFE
state_average_tfe = tfe.groupby('statename')['tfe'].mean().to_dict()

# Define a function to calculate tfe_imp
def calculate_tfe_imp(row):
    if pd.notna(row['tfe']):
        return row['tfe']
    else:
        state_name = row['Birthstate']
        return state_average_tfe.get(state_name, np.nan)

# Apply the function to create the tfe_imp column
ceo_df['tfe_imp'] = ceo_df.apply(calculate_tfe_imp, axis=1)


######## Merge in num_ceos to TFE #############################################

# Group and count CEOs by FIPS in ceo_df
ceo_count = ceo_df.groupby('FIPS').size().reset_index(name='num_ceos')

# Merge tfe_df and ceo_count to create the final dataframe
result_df = tfe.merge(ceo_count, on='FIPS', how='left')

# Fill missing values in num_ceos with 0
result_df['num_ceos'].fillna(0, inplace=True)





###############################################################################
######## Save clean .csv ######################################################

ceo_df.to_csv("data/clean_data/entrepreneurs_clean.csv")




