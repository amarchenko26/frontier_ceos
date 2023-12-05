#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:02:08 2023

@author: anyamarchenko
"""

import pandas as pd
import addfips
import os


# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)

######## Load data ############################################################

# Load the Excel file
file_path = 'data/raw_data/entrepreneurs_master.xlsx'
ceo_df = pd.read_excel(file_path, sheet_name = 'master')


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


######## Remove foreign countries ######################################

# List of countries to filter out
countries_to_filter = ["Australia", "Austria", "Belgium", "Canada", "China", "Cuba", "England", "France", "Germany",
                       "Germany (Prussia)", "Hawaii", "Hungary", "Ireland", "Norway", "Poland", "Rumania", "Russia",
                       "Scotland", "Sweden", "Switzerland", "Turkey", "Virgin Islands"]

# Filtering the DataFrame
ceo_df = ceo_df[~ceo_df['Birthstate'].isin(countries_to_filter)]

# Save clean df
ceo_df.to_csv("data/clean_data/entrepreneurs_clean.csv")