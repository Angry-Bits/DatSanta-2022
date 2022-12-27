from pathlib import Path
import json


BASE_DIR = Path.cwd()
MAP_FIXTURE_NAME = 'map.json'
MAP_FIXTURE_PATH = BASE_DIR.joinpath(MAP_FIXTURE_NAME)
RESULT_JSON_NAME = 'result.json'
RESULT_JSON_PATH = BASE_DIR.joinpath(RESULT_JSON_NAME)


def write_to_file(data, file_path):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


def dict_to_str_like_json(data):
    data = json.dumps(data, indent=4)
    return data
