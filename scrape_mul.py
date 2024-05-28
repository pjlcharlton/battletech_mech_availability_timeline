import os
import urllib.request, json
import pandas as pd
 
#the generic query form http://www.masterunitlist.info/Unit/QuickList?AvailableEras= + era_id + &Factions= + faction_id + &Types=18&HasBV=true
#sample url "http://www.masterunitlist.info/Unit/QuickList?AvailableEras=255&Factions=29&Types=18&HasBV=true"

def mul_data_by_url(url_in, return_search=False, return_crumbs=False):
    """"Query the MUL using the provided URL and return the unit list along with crumbs and search terms if desired"""
    json_url = urllib.request.urlopen(url_in)
    if not return_search and not return_crumbs:
        return json_url, json.load(json_url)['Units']]
    elif return_search and not return_crumbs:
        return json_url, [json.load(json_url)['Units'], *json.load(json_url)['Search']]
    elif not return_search and return_crumbs:
        return json_url, [json.load(json_url)['Units'], json.load(json_url)['Crumbs']]
    elif return_search and return_crumbs:
        return json_url, [json.load(json_url)['Units'], json.load(json_url)['Search'], json.load(json_url)['Crumbs']]
    else:
        print("Logic error in scrape_mul.mul_data_by_url, must investigate!")
        return

def mul_query_builder(era_id_in , faction_id_in, type_id_in, has_bv = True, production_info = False):
    mul_query = "https://masterunitlist.azurewebsites.net/Unit/QuickList?"
    if has_bv: mul_query += "&HasBV=true"
    mul_query += "&Types=" + str(type_id_in)
    if production_info:
        mul_query += "&Eras=" + str(era_id_in)
    else:
        mul_query += "&AvailableEras=" + str(era_id_in)
        mul_query += "&Factions=" + str(faction_id_in)
    print("MUL query: " + mul_query)
    return mul_query

def create_folder(foldername):
    if os.path.exists(foldername): 
        os.remove(foldername)
    os.mkdir(foldername)

def prep_folders(era_list, faction_list):
    create_folder('unit_data')
    create_folder('unit_production_data')
    for era in era_list:
        os.mkdir('unit_data/' + era)
        os.mkdir('unit_production_data/' + era)
        for faction in faction_list:
            os.mkdir('unit_data/' + era + '/' + 'faction_list')
    return

def process_unit_data(unit_data_in):
    

#create dataframes with the era and faction data for further use
era_df = pd.read_csv('mul_data/mul_era_data.csv')
factions_df = pd.read_csv('mul_data/mul_faction_data.csv')

prep_folders(era_df.loc[ : , "era_tag"], factions_df.loc[ : , "faction_tag"])

for era_id in era_df.loc[ : , "era_id"]:
    print('Query: mech production: era id = ' + str(era_id))
    json_url, unit_production_data = mul_data_by_url( mul_query_builder(era_id, 0 , 18, True, True) )
    for faction_id in list(set(factions_df.loc[ : , "faction_id"])):
        print('Query: mech availability: era id = ' + str(era_id) + ', faction id = ' + str(faction_id))
        json_url, unit_data = mul_data_by_url( mul_query_builder(era_id, faction_id , 18, True, False) )
        json_url.close()
        unit_data
            

test_url = mul_query_builder(256,102,18, True, False)
test = mul_data_by_url(test_url)

test_df = pd.DataFrame.from_dict(test) 

