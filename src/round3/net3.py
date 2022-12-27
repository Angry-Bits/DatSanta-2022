import json
import time
from pathlib import Path

import requests

from src.logger import logger

MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
MAP2_ID = 'a8e01288-28f8-45ee-9db4-f74fc4ff02c8'
MAP3_ID = 'dd6ed651-8ed6-4aeb-bcbc-d8a51c8383cc'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'
URL_JSON_GET = 'https://datsanta.dats.team/api/round/{}'
URL_JSON_POST = 'https://datsanta.dats.team/api/round'
TEAM_SECRET_TOKEN = 'bf31be91-70a6-476e-ae99-2b1c50f58ab8'


def get_map(id):
    r = requests.get(URL_MAP_GET.format(id))
    data = json.loads(r.text)
    logger.info("Получена карта с ID {}".format(id))
    return data


def post_json(data):
    r = requests.post(URL_JSON_POST, json=data, headers={
        "Content-Type": "application/json",
        "X-API-Key": TEAM_SECRET_TOKEN
    })
    logger.info("Отправлены данные на сервер.\n" +
                "Код ответа: {}.\nСообщение: {}".format(r.status_code, r.text)
                )
    return r


def get_result(round_id):
    logger.info("Запрос подтверждения решения...")
    r = requests.get(URL_JSON_GET.format(round_id), headers={
        "Content-Type": "application/json",
        "X-API-Key": TEAM_SECRET_TOKEN
    })
    if '"status":"pending"' in r.text:
        logger.info("Решение находится в обработке...")
        time.sleep(120)
        get_result(round_id)
    elif '"status":"processed"' in r.text:
        logger.info("Получены данные с сервера.\n" +
                    "Код ответа: {}.\nСообщение: {}".format(r.status_code, r.text)
                    )
    else:
        logger.info("Возникла ошибка.\n" +
                    "Код ответа: {}.\nСообщение: {}".format(r.status_code, r.text)
                    )


BASE_DIR = Path.cwd()
MAP_FIXTURE_NAME_3 = 'map.json'
MAP_FIXTURE_PATH_3 = BASE_DIR.joinpath(MAP_FIXTURE_NAME_3)
RESULT_JSON_NAME_3 = 'result.json'
RESULT_JSON_PATH = BASE_DIR.joinpath(RESULT_JSON_NAME_3)


def write_to_file(data, file_path):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


def dict_to_json_str(data):
    data = json.dumps(data, indent=4)
    return data


write_to_file(dict_to_json_str(get_map(MAP3_ID)), MAP_FIXTURE_PATH_3)
