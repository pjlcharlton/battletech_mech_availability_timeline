import urllib.request, json
 
#the generic query form http://www.masterunitlist.info/Unit/QuickList?AvailableEras= + era_id + &Factions= + faction_id + &Types=18&HasBV=true
 
url = urllib.request.urlopen("http://www.masterunitlist.info/Unit/QuickList?AvailableEras=255&Factions=29&Types=18&HasBV=true")
units = json.load(url)['Units']

for unit in units:
    print(unit['Class'])

