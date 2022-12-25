import json

import requests


MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'
URL_JSON_POST = 'https://datsanta.dats.team/api/round'
TEAM_SECRET_TOKEN = 'bf31be91-70a6-476e-ae99-2b1c50f58ab8'


def get_map(id: str = MAP_ID):
    r = requests.get(URL_MAP_GET.format(id))
    data = json.loads(r.text)
    return data


def post_json(data):
    r = requests.post(URL_JSON_POST, json=data, headers={
        "Content-Type": "application/json",
        "X-API-Key": TEAM_SECRET_TOKEN
    })
    print(r.status_code, r.text)
