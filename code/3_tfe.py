#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:18:36 2023

@author: anyamarchenko
"""

import pandas as pd
import os
import statsmodels.api as sm


# Regression is # of entrepreneurs from county X on tfe of county X. 

# Define the dependent variable (y) and independent variable (X)
y = result_df['num_ceos']
X = result_df['tfe']

# Add a constant term to the independent variable (intercept)
X = sm.add_constant(X)

# Fit the OLS regression model
model = sm.OLS(y, X).fit()

# Print the regression summary
print(model.summary())