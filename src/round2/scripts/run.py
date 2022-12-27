from typing import List, Dict, Tuple
import json
import requests
from src.logger import logger
from pathlib import Path

MAP_ID = 'faf7ef78-41b3-4a36-8423-688a61929c08'
MAP2_ID = 'a8e01288-28f8-45ee-9db4-f74fc4ff02c8'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'
URL_JSON_GET = 'https://datsanta.dats.team/api/round/{}'
URL_JSON_POST = 'https://datsanta.dats.team/api/round2'
TEAM_SECRET_TOKEN = 'bf31be91-70a6-476e-ae99-2b1c50f58ab8'
BASE_DIR = Path.cwd()
MAP_FIXTURE_NAME = 'map.json'
MAP_FIXTURE_PATH = BASE_DIR.joinpath(MAP_FIXTURE_NAME)
RESULT_JSON_NAME = 'result2.json'
RESULT_JSON_PATH = BASE_DIR.joinpath(RESULT_JSON_NAME)

g = requests.get('https://datsanta.dats.team/json/map/a8e01288-28f8-45ee-9db4-f74fc4ff02c8.json')
f = json.loads(g.text)
gifts = f['gifts']
children = f['children']
def post_json(data):
    r = requests.post(URL_JSON_POST, json=data, headers={
        "Content-Type": "application/json",
        "X-API-Key": TEAM_SECRET_TOKEN
    })
    logger.info("Отправлены данные на сервер.\n" +
        "Код ответа: {}.\nСообщение: {}".format(r.status_code, r.text)
    )
    return r

def write_to_file(data, file_path):
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)


def dict_to_json_str(data):
    data = json.dumps(data, indent=4)
    return data

def get_map(id):
    r = requests.get(URL_MAP_GET.format(id))
    data = json.loads(r.text)
    logger.info("Получена карта с ID {}".format(id))
    return data

data = get_map(MAP2_ID)

# g = requests.get('https://datsanta.dats.team/json/map/a8e01288-28f8-45ee-9db4-f74fc4ff02c8.json')
# f = json.loads(g.text)
# gifts = f['gifts']
# children = f['children']


def select_gifts(gifts, children):
    # отсортируем список подарков по цене в порядке убывания
    gifts.sort(key=lambda x: -x['price'])

    # отсортируем список детей по возрасту в порядке возрастания
    # children.sort(key=lambda x: x['age'])

    # иницилизируем общую стоимость подарков и список выбранных подарков
    total_price = 0
    selected_gifts = []
    selected_cildren = []
    result = []
    gift_girls_0_3 = []
    gift_girls_4_6 = []
    gift_girls_6_10 = []
    gift_males_0_3 = []
    gift_males_4_6 = []
    gift_males_6_10 = []

    for lit in gifts:
        if lit['type'] == 'soft_toys':
            gift_girls_0_3.append(lit)
        # if lit['type'] == 'pet':
        #     gift_girls_0_3.append(lit)
        if lit['type'] == 'dolls':
            gift_girls_4_6.append(lit)
        # if lit['type'] == 'sweets':
        #     gift_girls_4_6.append(lit)
        # if lit['type'] == 'outdoor_games':
        #     gift_girls_4_6.append(lit)
        if lit['type'] == 'clothes':
            gift_girls_6_10.append(lit)
        # if lit['type'] == 'board_games':
        #     gift_girls_6_10.append(lit)
        if lit['type'] == 'toy_vehicles':
            gift_males_0_3.append(lit)
        # if lit['type'] == 'books':
        #     gift_males_0_3.append(lit)
        if lit['type'] == 'constructors':
            gift_males_4_6.append(lit)
        # if lit['type'] == 'playground':
        #     gift_males_4_6.append(lit)
        if lit['type'] == 'computer_games':
            gift_males_6_10.append(lit)
        # if lit['type'] == 'radio_controlled_toys':
        #     gift_males_6_10.append(lit)

    # для каждого ребенка в списке детей
    for child in children:
        # пройдемся по подаркам в порядке убывания цены
        for g in gifts:
            # если подарок подходит ребенку по возрасту и общая стоимость подарков не превышает бюджет
            if ((child['age'] <= 3 and child['gender'] == 'female' and g['type'] in gift_girls_0_3) or (
                    child['age'] <= 3 and child['gender'] == 'male' and g['type'] in gift_males_0_3) or (
                        child['age'] >= 4 or child['age'] <= 6 and child['gender'] == 'female' and g['type']
                        in gift_girls_4_6)) or (
                    child['age'] >= 4 or child['age'] <= 6 and child['gender'] == 'male' and g['type']
                    in gift_males_4_6) or (
                    child['age'] > 6 and child['gender'] == 'female' and g['type'] in gift_girls_6_10) or (
                    child['age'] > 6 and child['gender'] == 'male' and g['type'] in gift_males_6_10) and \
                    total_price + g['price'] <= 100000:
                # добавляем подарок в список выбранных подарков
                selected_gifts.append(g)
                selected_cildren.append(child)

                # обновляем общую стоимость подарков
                total_price += g['price']
                # удаляем подарок из общего списка подарков, чтобы он больше не выбирался
                gifts.remove(g)
                children.remove(child)

                # order = {"giftID": selected_gifts.get('id'),
                #          "childID": selected_cildren.get('id')}
                # result.append(order)
                # прекращаем разбирать подарки для этого ребенка
                break
    for gif, chil in zip(selected_gifts, selected_cildren):
        order = {"giftID": gif.get('id'),
                 "childID": chil.get('id')}
        result.append(order)

    return result



result = select_gifts(gifts, children)
# print(a)
json_file = {"mapID": "a8e01288-28f8-45ee-9db4-f74fc4ff02c8",
             "presentingGifts": result}

data = dict_to_json_str(json_file)
write_to_file(data, RESULT_JSON_PATH)

# Отправляем данные на сервер и получаем результат
# r = post_json(json_file)


def get_result(round_id):
    logger.info("Запрос подтверждения решения...")
    r = requests.get('https://datsanta.dats.team/api/round2/01GN7QJQA0R5GHJ4V2EHRV5Y93', headers={
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

get_result('01GN7QJQA0R5GHJ4V2EHRV5Y93')

