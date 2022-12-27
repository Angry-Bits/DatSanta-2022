from pathlib import Path
import json


BASE_DIR = Path.cwd()
MAP3_ID = 'dd6ed651-8ed6-4aeb-bcbc-d8a51c8383cc'
MAP_FIXTURE_NAME_3 = 'map3.json'
MAP_FIXTURE_PATH = BASE_DIR.joinpath(MAP_FIXTURE_NAME_3)
RESULT_JSON_NAME_3 = 'result.json'
RESULT_JSON_PATH = BASE_DIR.joinpath(RESULT_JSON_NAME_3)


def write_to_file(data, file_path):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


def dict_to_json_str(data):
    data = json.dumps(data, indent=4)
    return data


write_to_file(MAP3_ID, MAP_FIXTURE_PATH)
print(dict_to_json_str(MAP3_ID))
