import json
import time

import requests

from src.logger import logger


MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
MAP2_ID = 'a8e01288-28f8-45ee-9db4-f74fc4ff02c8'
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
