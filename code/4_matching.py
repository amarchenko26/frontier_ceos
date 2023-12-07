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


# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)

county_ceo = pd.read_csv('data/clean_data/county_ceo.csv')

# Select columns to be used for matching
matching_columns = ['tfe', 'pop1950', 'statea']  

# Need to drop NA for NN to work - FIX THIS, currently 
county_ceo_no_na = county_ceo.dropna(subset=matching_columns)

# Create Nearest Neighbors model
nn = NearestNeighbors(n_neighbors = 2)  # Change '2' to however many matches you want
nn.fit(county_ceo_no_na[matching_columns])

# Find the nearest neighbors for each county (excluding the county itself)
distances, indices = nn.kneighbors(county_ceo_no_na[matching_columns])

# Example of how to use the indices to find matches
for i in range(len(county_ceo_no_na)):
    matched_county_index = indices[i, 1]  # Index 1 because 0 is the county itself
    print(f"County {county_ceo_no_na.iloc[i]['statename']} is matched with {county_ceo_no_na.iloc[matched_county_index]['statename']}")
