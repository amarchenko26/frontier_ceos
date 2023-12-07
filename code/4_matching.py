#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:12:42 2023

@author: anyamarchenko
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import statsmodels.api as sm


###############################################################################
# Path
###############################################################################

# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)


###############################################################################
# Load data
###############################################################################

county_ceo = pd.read_csv('data/clean_data/county_ceo.csv')


###############################################################################
# Match counties
###############################################################################

# Initialize df to store matched counties' information
matched_counties = pd.DataFrame(columns=['state', 'high_tfe_county', 'low_tfe_county', 'high_tfe_ceos', 'low_tfe_ceos'])
matching_vars = ['pop1950', 'tfe', ]

# Drop rows with missings in the matching_vars
county_ceo = county_ceo.dropna(axis = 0, subset = matching_vars)

# Iterate over each state
for state in county_ceo['statea'].unique():
    
    # Filters county_ceo by just values of that state
    state_counties = county_ceo[county_ceo['statea'] == state]
    
    print(f"Imported state {state}")

    # Calculate the median TFE for the current state
    median_tfe = state_counties['tfe'].median()

    # Split into high and low TFE for the current state
    high_tfe = state_counties[state_counties['tfe'] >= median_tfe]
    low_tfe = state_counties[state_counties['tfe'] < median_tfe]

    print(f"Got High vs Low TFE counties for state {state}")

    # Check if there are enough counties in both high and low TFE groups
    if len(high_tfe) > 0 and len(low_tfe) > 0:
                
        # Nearest Neighbor Matching within the state
        nn = NearestNeighbors(n_neighbors = 1)
        print(f"Got NN for state {state}")

        nn.fit(low_tfe['pop1950'])

        distances, indices = nn.kneighbors(high_tfe['pop1950'])

        # Store the matched counties' information
        for i, index in enumerate(indices.squeeze()):
            high_tfe_row = high_tfe.iloc[i]
            low_tfe_row = low_tfe.iloc[index]
        
            row_df = pd.DataFrame({
                'state': [state],
                'high_tfe_county': [high_tfe_row['name']],  # Assuming the county name is the index
                'low_tfe_county': [low_tfe_row['name']],
                'high_tfe_ceos': [high_tfe_row['num_ceos']],
                'low_tfe_ceos': [low_tfe_row['num_ceos']]
            })
            
            matched_counties = pd.concat([matched_counties, row_df], ignore_index = True)

del high_tfe_row
del low_tfe_row
del distances
del indices
del median_tfe

# Display the matched counties and their CEO counts
print(matched_counties)


###############################################################################
# Take means of matched 
###############################################################################

ate_matched = matched_counties['high_tfe_ceos'].mean() - matched_counties['low_tfe_ceos'].mean()
print(f"Difference between above median and below median TFE counties (by state) in their number of CEOs is {ate_matched}")
