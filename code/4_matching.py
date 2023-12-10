#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:12:42 2023

@author: anyamarchenko
"""

import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors

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
# Defin match function
###############################################################################

def match_counties(county_ceo):
    # Initialize df to store matched counties' information
    matched_counties = pd.DataFrame(columns=['state', 'high_tfe_county', 'low_tfe_county', 'high_tfe_ceos', 'low_tfe_ceos'])
    matching_vars = ['pop1950', 'tfe']

    # Drop rows with missing values in the matching_vars
    county_ceo = county_ceo.dropna(axis=0, subset=matching_vars)

    # Match counties
    for state in county_ceo['statea'].unique():
        # Filter county_ceo by just values of that state
        state_counties = county_ceo[county_ceo['statea'] == state]

        # Calculate the median TFE for the current state
        median_tfe = state_counties['tfe'].median()

        # Split into high and low TFE for the current state
        high_tfe = state_counties[state_counties['tfe'] >= median_tfe]
        low_tfe = state_counties[state_counties['tfe'] < median_tfe]

        # Check if there are enough counties in both high and low TFE groups
        if len(high_tfe) > 0 and len(low_tfe) > 0:
            # Nearest Neighbor Matching within the state
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(low_tfe[matching_vars])

            distances, indices = nn.kneighbors(high_tfe[matching_vars])

            # Store the matched counties' information
            for i, index in enumerate(indices.squeeze()):
                high_tfe_row = high_tfe.iloc[i]
                low_tfe_row = low_tfe.iloc[index]

                row_df = pd.DataFrame({
                    'state': [state],
                    'high_tfe_county': [high_tfe_row['name']],
                    'low_tfe_county': [low_tfe_row['name']],
                    'high_tfe_value': [high_tfe_row['tfe']],
                    'low_tfe_value': [low_tfe_row['tfe']],
                    'high_tfe_pop': [high_tfe_row['pop1950']],
                    'low_tfe_pop': [low_tfe_row['pop1950']],
                    'high_tfe_ceos': [high_tfe_row['num_ceos']],
                    'low_tfe_ceos': [low_tfe_row['num_ceos']]
                })

                matched_counties = pd.concat([matched_counties, row_df], ignore_index=True)

    return matched_counties

def return_ate(df):
    ate = df['high_tfe_ceos'].mean() - df['low_tfe_ceos'].mean()
    return ate

###############################################################################
# Match counties
###############################################################################

# Match 1
matched_counties = match_counties(county_ceo)

ate_matched = return_ate(matched_counties)
print(f"Difference between above median and below median TFE counties (by state) in their number of CEOs is {ate_matched}")


# Match 2
core_tfe_states = ["Minnesota", "Iowa", "Missouri", "Michigan", "Arkansas", "Louisiana", "Mississippi", "Alabama", "Florida", "Tennessee", "Kentucky", "Ohio", "Indiana", "Illinois", "Wisconsin"]
matched_counties_core_only = match_counties(county_ceo[county_ceo['statename'].isin(core_tfe_states)])

ate_matched_core = return_ate(matched_counties_core_only)
print(f"Difference between above median and below median TFE counties (by state) FOR CORE STATES in their number of CEOs is {ate_matched_core}")

