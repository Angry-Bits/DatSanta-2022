import requests
import pprint
import json


ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
URL = 'https://datsanta.dats.team/json/map/{}.json'


def get_map(id=ID):
    r = requests.get(URL.format(id))
    s = json.dumps(r.text, indent=10)
    print(s)


get_map(ID)