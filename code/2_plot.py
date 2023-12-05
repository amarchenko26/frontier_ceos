#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:15:02 2023

@author: anyamarchenko
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import subprocess # for sleep

######## Paths & sleep functions #############################################

def prevent_sleep():
    return subprocess.Popen(['caffeinate'])

def allow_sleep(process):
    process.terminate()

# Uncomment to prevent comp from sleeping
process = prevent_sleep()

# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)


######## Load data ############################################################

# Read in clean ceo_df
ceo_df = pd.read_csv("data/clean_data/entrepreneurs_clean.csv")

# Read in codes & state pop data
file_path = 'data/raw_data/entrepreneurs_master.xlsx'
all_sheets = pd.read_excel(file_path, sheet_name=None)

# Access a specific sheet from the dictionary
ceo_codes = all_sheets['codes']
state_pop_1850 = all_sheets['state_pop_1850']
state_pop_1900 = all_sheets['state_pop_1900']
state_pop_1950 = all_sheets['state_pop_1950']



##################################### Histogram of birthplaces 

# Checking unique values and their frequencies in the 'Birthplace' column
birthplace_counts = ceo_df['Birthstate'].value_counts()

# Creating the histogram for the birthplaces
plt.figure(figsize=(15, 8))
birthplace_counts.plot(kind='bar')
plt.title('Histogram of CEO\'s Birthplaces')
plt.xlabel('Birthplace (State)')
plt.ylabel('Number of Leaders')
plt.xticks(rotation=90)  # Rotate labels to make them readable

plt.style.use('bmh')
plt.tight_layout()

plt.savefig('output/figures/state_hist.png', format='png')


##################################### Histogram of birthplaces by pop

state_pop = pd.merge(state_pop_1900, state_pop_1950, how = 'left', on ='state')
state_pop = pd.merge(state_pop, state_pop_1850, how = 'left', on ='state')

del state_pop_1850 
del state_pop_1900 
del state_pop_1950

# Setting the 'State' column as the index for easy lookup
state_pop.set_index('state', inplace=True)

# First, map the population data to the birthplaces
ceo_df['State Population 1900'] = ceo_df['Birthstate'].map(state_pop['1900_census_pop'])

# Calculate number of leaders divided by state population
ceo_df['Scaled Leaders'] = 1 / ceo_df['State Population 1900']

# Summing the scaled values for each state to get the final values for the histogram
scaled_birthplace_counts = ceo_df.groupby('Birthstate')['Scaled Leaders'].sum()

# Sort the values for better visualization
scaled_birthplace_counts = scaled_birthplace_counts.sort_values(ascending=False)

# Create the rescaled histogram for the birthplaces
plt.figure(figsize=(15, 8))
scaled_birthplace_counts.plot(kind='bar')
plt.title('Histogram of CEOs\' Birthstates (Normalized by 1900 State Population)')
plt.xlabel('Birthplace (State)')
plt.ylabel('Scaled Number of CEOs by State Population')
plt.xticks(rotation=90)  # Rotate labels to make them readable

plt.style.use('bmh')
plt.tight_layout()

plt.savefig('output/figures/state_hist_rescaled.png', format='png')
