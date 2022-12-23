from pathlib import Path
import json

import requests


SRC = Path.cwd()
MAP_FIXTURE_NAME = 'map.json'
MAP_FIXTURE_PATH = SRC.joinpath(MAP_FIXTURE_NAME)

MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'


def get_map(id=MAP_ID):
    r = requests.get(URL_MAP_GET.format(id))
    data = json.loads(r.text)
    data = json.dumps(data, indent=4)
    return data


def write_to_file(data, file_path=SRC):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


write_to_file(get_map(), MAP_FIXTURE_PATH)
