import urllib.request, json
import pandas as pd
import time
import toolbox 

def mul_data_by_url(url_in, return_search=False, return_crumbs=False):
    """
    Query the MUL using the provided URL and return the unit list along with crumbs and search terms if desired

    Parameters
    ----------
    url_in : str
        Url for MUL query.
    return_search : bool, optional
        Query should return search used. The default is False.
    return_crumbs : bool, optional
        Query should return crumbs. The default is False.

    Returns
    -------
    json_url : json_url object
        handle for the json object.
    list
        query output.

    """
    
    json_url = urllib.request.urlopen(url_in)
    
    if not return_search and not return_crumbs:
        return json_url, json.load(json_url)['Units']
    elif return_search and not return_crumbs:
        return json_url, [json.load(json_url)['Units'], json.load(json_url)['Search']]
    elif not return_search and return_crumbs:
        return json_url, [json.load(json_url)['Units'], json.load(json_url)['Crumbs']]
    elif return_search and return_crumbs:
        return json_url, [json.load(json_url)['Units'], json.load(json_url)['Search'], json.load(json_url)['Crumbs']]
    else:
        print("Logic error in scrape_mul.mul_data_by_url, must investigate!")
        return

def mul_query_builder(era_id_in , faction_id_in, type_id_in, production_info = False):
    """
    Build and return MUL query string

    Parameters
    ----------
    era_id_in : int
        MUL ID of the era to be queried.
    faction_id_in : int
        MUL ID of the faction to be queried.
    type_id_in : int
        MUL type ID of the units to be queried.
    production_info : bool, optional
        Bool that changes functionality to query mech production. The default is False.

    Returns
    -------
    mul_query : str
        String containing MUL query, constructed with provided parameters.

    """
    
    mul_query = "https://masterunitlist.azurewebsites.net/Unit/QuickList?Name=&HasBV=false&MinTons=&MaxTons=&MinBV=&MaxBV=&MinIntro=&MaxIntro=&MinCost=&MaxCost=&HasBFAbility=&MinPV=&MaxPV=&&BookAuto=&FactionAuto="
    mul_query += "&Types=" + str(type_id_in)
    
    if production_info:
        mul_query += "&Eras=" + str(era_id_in)
    else:
        mul_query += "&AvailableEras=" + str(era_id_in)
        mul_query += "&Factions=" + str(faction_id_in)
        
    print("MUL query: " + mul_query)
    
    return mul_query

def prep_mul_dataframe(mul_df_in, b_production, era_tag, faction_tag):
    """
    

    Parameters
    ----------
    mul_df_in : Pandas DataFrrame
        DataFrame to be prepared.
    b_production : bool
        Tells function whether to treat input as a production table.
    era_tag : str
        era tag to be attached to the table.
    faction_tag : str
        faction tag to be attached to the table.

    Returns
    -------
    mul_df_out : Pandas DataFrame
        Prepared DataFrame.

    """
    
    mul_df_out = pd.DataFrame(mul_df_in)
    mul_df_out.set_index('Id', inplace=True)
    
    #Tech, role, and type colums are dicts, extract the name of each and create new columns
    dummy_col_tech = []
    dummy_col_role = []
    dummy_col_type = []
    
    for i in range(len(mul_df_in)):
        dummy_col_tech.append(mul_df_in.loc[ i, 'Technology']['Name'])
        dummy_col_role.append(mul_df_in.loc[ i, 'Role']['Name'])
        dummy_col_type.append(mul_df_in.loc[ i, 'Type']['Name'])
        
    mul_df_out['Technology'] = dummy_col_tech
    mul_df_out['Role'] = dummy_col_role
    mul_df_out['Type'] = dummy_col_type
    if b_production:   
        mul_df_out['Production Era'] = era_tag
    else:   
        mul_df_out['Availability Era'] = era_tag
        mul_df_out['Faction'] = faction_tag
        
    return mul_df_out
    
#create dataframes with the era and faction data for further use
era_df = pd.read_csv('mul_data/mul_era_data.csv')
era_ids = list(era_df.loc[ : , 'era_id'])
era_tags = list(era_df.loc[ :, 'era_tag'])
era_names = list(era_df.loc[ :, 'era_name'])

factions_df = pd.read_csv('mul_data/mul_faction_data.csv')
faction_ids = list(factions_df.loc[:, 'faction_id'].drop_duplicates())
faction_tags = list(factions_df.loc[:,'faction_tag'].drop_duplicates())
faction_names = list(factions_df.loc[:, 'faction_name'].drop_duplicates())

toolbox.cleanup_folder('unit_availability_data')
toolbox.cleanup_folder('unit_production_data')

for i in range(len(era_ids)):
    
    print('Query: mech production: era id = ' + str(era_ids[i]))
    
    json_url, unit_production_data = mul_data_by_url( mul_query_builder(era_ids[i], 0 , 18, True) )
    json_url.close()
    
    if len(unit_production_data) > 0:
        unit_production_df = prep_mul_dataframe(pd.DataFrame(unit_production_data), True, era_tags[i], '')
        unit_production_df.to_csv('unit_production_data/' +str(era_tags[i]) + '_mech_production.csv')
        
        print(str(era_tags[i]) + '_mech_production.csv saved!')
        print(str(len(unit_production_df)) + '\n')
    else:
        print('No mech production in ' + era_names[i] +'\n') 
   
    for j in range(len(faction_ids)):

        print('Query: mech availability: era id = ' + str(era_ids[i]) + ', faction id = ' + str(faction_ids[j]))
        
        json_url, unit_availability_data = mul_data_by_url( mul_query_builder(era_ids[i], faction_ids[j] , 18, False) )
        json_url.close()
        
        if len(unit_availability_data) > 0:
            unit_availability_df = prep_mul_dataframe(pd.DataFrame(unit_availability_data), False, era_tags[i], faction_tags[j])
            unit_availability_df.to_csv('unit_availability_data/' +str(era_tags[i]) + '_' + str(faction_tags[j]) + '_mech_availability.csv')
            
            print(str(era_tags[i]) + '_' + str(faction_tags[j]) + '_mech_availability.csv saved!\n')
            print(str(len(unit_availability_df)) + '\n')
        else:
            print('No mechs available in ' + era_names[i] + ' for ' + faction_names[j] + '\n')
        
        time.sleep(0.1)
    time.sleep(0.1) 

#Lyran Alliance tables for early replublic era need creating from the Lyran Comonwealth table
lc_df = pd.read_csv('unit_availability_data/early-republic_lc_mech_availability.csv')
la_df = lc_df[lc_df['DateIntroduced'] < 3085]
la_df.to_csv('unit_availability_data/early-republic_la_mech_availability.csv')                  