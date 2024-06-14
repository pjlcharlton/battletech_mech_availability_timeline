# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:44:09 2024

Combine faction availability tables into full table.

@author: pjlch
"""

import pandas as pd

column_names = list(pd.read_csv('faction_availability_data/aml_mech_availability.csv').columns)

era_df = pd.read_csv('mul_data/mul_era_data.csv', index_col='era_id')
faction_df = pd.read_csv('mul_data/mul_faction_data.csv')

full_availability_df = pd.DataFrame(columns=column_names)

for i in range(len(faction_df.index)): 
    print('Processing ' + faction_df['faction_name'].iat[i])           
    try:
        faction_availability_df = pd.read_csv('faction_availability_data/' + str(faction_df['faction_tag'].iloc[i]) + '_mech_availability.csv')
    except FileNotFoundError:
        continue
           
    full_availability_df = pd.concat([full_availability_df, faction_availability_df])
        
full_availability_df.index.name = 'TLId'
full_availability_df.rename({'Id' : 'MULId'}, inplace=True)
full_availability_df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'EraIcon', 'ImageUrl']+list(full_availability_df.columns)[25:45], axis=1, inplace=True)

full_availability_df.to_csv('full_mech_availability.csv')