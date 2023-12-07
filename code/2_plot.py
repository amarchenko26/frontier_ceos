#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:15:02 2023

@author: anyamarchenko
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gpd


###############################################################################
# Path
###############################################################################

# Set the base directory
base_directory = "/Users/anyamarchenko/Documents/Github/frontier_ceos"
os.chdir(base_directory)


###############################################################################
# Load data
###############################################################################

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


###############################################################################
# FUNCTIONS
###############################################################################

# Constants
BIRTHSTATE_COL = 'Birthstate'
STATE_POP_1950_COL = 'State Population 1950'
SCALED_LEADERS_COL = 'Scaled Leaders'
CEO_COUNT_COL = 'CEO_count'
CEO_COUNT_SCALED_COL = 'CEO_count_scaled'
FIGURE_PATH = 'output/figures/'

def merge_state_populations(*pop_dfs):
    state_pop = pd.DataFrame()
    for df in pop_dfs:
        if state_pop.empty:
            state_pop = df
        else:
            state_pop = pd.merge(state_pop, df, how='left', on='state')
    return state_pop


def scale_ceo_counts_by_population(ceo_df, population_df, population_column):
    """
    Scales CEO counts by state population.

    :param ceo_df: DataFrame containing CEO data.
    :param population_df: DataFrame containing population data.
    :param population_column: Column name in population_df to be used for scaling.
    :return: A Series with scaled CEO counts by state.
    """
    # Map the population data to the birthplaces
    ceo_df['State Population'] = ceo_df[BIRTHSTATE_COL].map(population_df[population_column])

    # Calculate number of leaders divided by state population
    ceo_df[SCALED_LEADERS_COL] = 1 / ceo_df['State Population']

    # Summing the scaled values for each state
    scaled_state_ceo_counts = ceo_df.groupby('Birthstate')['Scaled Leaders'].sum()

    # Sort the values for better visualization
    scaled_state_ceo_counts = scaled_state_ceo_counts.sort_values(ascending=False)

    return scaled_state_ceo_counts


def plot_histogram(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(15, 8))
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.style.use('bmh')
    plt.tight_layout()
    plt.savefig(f'{FIGURE_PATH}{filename}', format='png')
    plt.show()


def prepare_map_data(counts, map_template, count_column_name):
    """
    Prepares map data by merging counts with the map template.

    :param counts: Series containing counts to be mapped.
    :param map_template: GeoDataFrame of the map template (e.g., continental_usa).
    :param count_column_name: Column name to assign to the counts.
    :return: GeoDataFrame ready for plotting.
    """
    # Initialize all states with default count 0
    all_states = pd.Series(0, index=map_template['name'])

    # Update with actual counts
    updated_counts = all_states.add(counts, fill_value=0)

    # Merge the counts with the map template
    return map_template.set_index('name').join(updated_counts.rename(count_column_name))


def plot_map(map_data, column, title, filename):
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    map_data.plot(column=column, ax=ax, legend=True, legend_kwds={'orientation': "horizontal"})
    plt.title(title, fontsize=14, pad=20)
    plt.savefig(f'{FIGURE_PATH}{filename}', format='png')
    plt.show()


# Create df with state pop
state_pop = merge_state_populations(state_pop_1850, state_pop_1900, state_pop_1950)
state_pop.set_index('state', inplace=True)

# Create CEO counts from 'Birthplace' column
state_ceo_counts = ceo_df[BIRTHSTATE_COL].value_counts()

# Create scaled CEO counts
scaled_counts_1950 = scale_ceo_counts_by_population(ceo_df, state_pop, '1950_census_pop')



###############################################################################
# Histograms
###############################################################################

# Plot histogram of counts
plot_histogram(data = state_ceo_counts, title="Histogram of CEO's Birthplaces", xlabel='Birthplace (State)', ylabel='Number of Leaders', filename='state_hist.png')
plot_histogram(data = scaled_counts_1950, title="Histogram of CEO's Birthplaces (Normalized by 1950 State Pop", xlabel='Birthplace (State)', ylabel='Number of Leaders', filename='state_hist_rescaled.png')


###############################################################################
# Maps
###############################################################################

# Load U.S. states map
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
usa = gpd.read_file(url)

# Filter out Alaska and Hawaii
continental_usa = usa[~usa['name'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]


# Prepare Map 1
map_data = prepare_map_data(state_ceo_counts, continental_usa, CEO_COUNT_COL)

# Map 1
plot_map(map_data = map_data, column = CEO_COUNT_COL, title="Number of CEOs Born per State", filename='map_ceos.png')


# Prepare Map 2
map_data_scaled = prepare_map_data(scaled_counts_1950, continental_usa, CEO_COUNT_SCALED_COL)

# Map 2
plot_map(map_data = map_data_scaled, column = CEO_COUNT_SCALED_COL, title="Number of CEOs Born per State (Normalized by 1950 State Population)", filename='map_ceos_norm.png')


