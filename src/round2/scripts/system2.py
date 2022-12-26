from pathlib import Path
import json


BASE_DIR = Path.cwd()
MAP_FIXTURE_NAME_2 = 'map2.json'
MAP_FIXTURE_PATH = BASE_DIR.joinpath(MAP_FIXTURE_NAME_2)
RESULT_JSON_NAME_2 = 'result2.json'
RESULT_JSON_PATH = BASE_DIR.joinpath(RESULT_JSON_NAME_2)


def write_to_file(data, file_path):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


def dict_to_json_str(data):
    data = json.dumps(data, indent=4)
    return data

