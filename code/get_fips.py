#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:02:08 2023

@author: anyamarchenko
"""

import pandas as pd
import addfips

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

# Now ceo_df has a new column 'FIPS' with the FIPS codes
print(ceo_df)
