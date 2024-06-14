# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:44:09 2024

Combine faction availability tables split by era into one for each faction.

@author: pjlch
"""

import pandas as pd
import numpy as np

#Several factions have a gap in t their existence, rather than redo the tags, handle them here

special_cases = {'fwl' : [ [2271, 3079], [3139, 3152] ]
                 ,'lc' : [ [2341, 3057], [3084, 3152] ]
                 ,'c_sf' : [ [2807, 2895], [3100, 3152] ]
                 ,'c_b' : [ [2807, 3059], [3072, 3074] ]}

def handle_special_case(faction_tag, era_start, split_year, special_case_dict):
    if (era_start < split_year):
        return special_case_dict[faction_tag][0][0], special_case_dict[faction_tag][0][1]
    else:
        return special_case_dict[faction_tag][1][0], special_case_dict[faction_tag][1][1]


outcolumns = list(pd.read_csv('unit_availability_data/clan-invasion_sl_2_mech_availability.csv').columns)
outcolumns.append('EraAvailabilityStart') 
outcolumns.append('EraAvailabilityEnd')

era_df = pd.read_csv('mul_data/mul_era_data.csv')
faction_df = pd.read_csv('mul_data/mul_faction_data.csv')

for i in range(len(faction_df.index)):
   
    faction_start = faction_df['faction_start'].iat[i]
    faction_end = faction_df['faction_end'].iat[i]
    
    faction_availability_df = pd.DataFrame(columns = outcolumns)
    
    for j in range(len(era_df.index)):
        print('Processing ' + faction_df['faction_name'].iat[i] + ' ' + era_df['era_name'].iat[j])
        
        era_start = era_df['era_start'].iat[j]
        era_end = era_df['era_end'].iat[j]
                   
        try:
            unit_availability_df = pd.read_csv('unit_availability_data/' + str(era_df['era_tag'].iloc[j]) + '_' + str(faction_df['faction_tag'].iloc[i]) + '_mech_availability.csv')
        except FileNotFoundError:
            continue
        
        unit_availability_df = unit_availability_df[pd.to_numeric(unit_availability_df['DateIntroduced'], errors='coerce').notnull()]
        
        #Check for special cases
        if faction_df['faction_tag'].iat[i] == 'fwl':
            faction_star, faction_end = handle_special_case('fwl', era_start, 3131, special_cases)
        elif faction_df['faction_tag'].iat[i] == 'lc':
            faction_start, faction_end = handle_special_case('lc', era_start, 3081, special_cases)
        elif faction_df['faction_tag'].iat[i] == 'c_sf':
            faction_start, faction_end = handle_special_case('c_sf', era_start, 3100, special_cases)
        elif faction_df['faction_tag'].iat[i] == 'c_b':
            faction_start, faction_end = handle_special_case('c_b', era_start, 3068, special_cases)
        
        #use np arrays and max to crate start and end date columns for each era
        compare_date_start = max(era_start, faction_start) * np.ones_like(unit_availability_df['DateIntroduced'])
        compare_date_end = min(era_end, faction_end) * np.ones_like(unit_availability_df['DateIntroduced'])
        
        unit_availability_df['EraAvailabilityStart'] = np.maximum(unit_availability_df['DateIntroduced'].to_numpy(dtype='int'), compare_date_start )
        unit_availability_df['EraAvailabilityEnd'] = compare_date_end
        unit_availability_df['Era Name'] = era_df['era_name'].iat[j]
        
        faction_availability_df = pd.concat([faction_availability_df, unit_availability_df])
            
    faction_availability_df['Faction Name'] = faction_df['faction_name'].iat[i]    
   
    faction_availability_df.to_csv('faction_availability_data/' + faction_df['faction_tag'][i] + '_mech_availability.csv')