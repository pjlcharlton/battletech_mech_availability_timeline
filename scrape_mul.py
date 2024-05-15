import urllib.request, json
import numpy as np
 
#the generic query form http://www.masterunitlist.info/Unit/QuickList?AvailableEras= + era_id + &Factions= + faction_id + &Types=18&HasBV=true
#sample url "http://www.masterunitlist.info/Unit/QuickList?AvailableEras=255&Factions=29&Types=18&HasBV=true"

def mul_data_by_url(url_in, return_search=False, return_crumbs=False):
    """"Query the MUL using the provided URL and return the unit list along with crumbs and search terms if desired"""
    json_url = urllib.request.urlopen(url_in)
    if not return_search and not return_crumbs:
        return json.load(json_url)['Units']
    elif return_search and not return_crumbs:
        return [json.load(json_url)['Units'], *json.load(json_url)['Search']]
    elif not return_search and return_crumbs:
        return [json.load(json_url)['Units'], json.load(json_url)['Crumbs']]
    elif return_search and return_crumbs:
        return [json.load(json_url)['Units'], json.load(json_url)['Search'], json.load(json_url)['Crumbs']]
    else:
        print("Logic error in scrape_mul.mul_data_by_url, must investigate!")
        return

def mul_query_builder(era_id_in , faction_id_in, types_id_in, has_bv = True):
    """&MinIntro=&MaxIntro=&Types=&FactionAuto=&AvailableEras="""
    mul_query = "http://www.masterunitlist.info/Unit/QuickList?"
    mul_query = mul_query + has_bv*"&HasBV=true"
    mul_query = mul_query + FactionAuto
    
    
#test = mul_data_by_url("http://www.masterunitlist.info/Unit/QuickList?AvailableEras=255&Factions=29&Types=18&HasBV=true")



