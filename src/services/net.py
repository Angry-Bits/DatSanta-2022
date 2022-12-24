import json

import requests


MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'


def get_map(id: str = MAP_ID):
    r = requests.get(URL_MAP_GET.format(id))
    data = json.loads(r.text)
    return data
