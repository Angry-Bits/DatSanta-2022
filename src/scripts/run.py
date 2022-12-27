#!/usr/bin/env python

import re
from pathlib import Path

from src.services.presents import get_gift_baskets
from src.services.children import create_cluster, get_children_addresses
from src.services.system import write_to_file, dict_to_str_like_json
from src.services.net import get_map, post_json, get_result
from src.logger import logger


MAP3_ID = 'dd6ed651-8ed6-4aeb-bcbc-d8a51c8383cc'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'
URL_JSON_GET = 'https://datsanta.dats.team/api/round3/{}'
URL_JSON_POST = 'https://datsanta.dats.team/api/round'
TEAM_SECRET_TOKEN = 'bf31be91-70a6-476e-ae99-2b1c50f58ab8'


def main(map_id: str = MAP3_ID):
    # Формируем словарь, который в итоге отправится на сервер как JSON
    request = {
        "mapID": map_id,
        "moves": [],
        "stackOfBags": []
    }
    # Скачиваем карту, берем оттуда информацию о подарках и детях
    data = get_map(map_id)
    gifts = data.get('gifts')
    children = data.get('children')

    # Обрабатываем данные
    males = list(filter(lambda x: x['gender'] == 'male', children))
    girls = list(filter(lambda x: x['gender'] == 'female', children))
    # girls_younger5 = list(filter(lambda x: x['age'] <= 3, girls))
    # males_younger5 = list(filter(lambda x: x['age'] <= 3, males))
    # males_older = list(filter(lambda x: x['age'] > 3, males))
    # girls_older = list(filter(lambda x: x['age'] > 3, girls))

    educational_games = list(filter(lambda x: x['type'] == 'educational_games', gifts))
    music_games = list(filter(lambda x: x['type'] == 'music_games', gifts))
    bath_toys = list(filter(lambda x: x['type'] == 'bath_toys', gifts))
    bike = list(filter(lambda x: x['type'] == 'bike', gifts))
    paints = list(filter(lambda x: x['type'] == 'paints', gifts))
    casket = list(filter(lambda x: x['type'] == 'casket', gifts))
    soccer_ball = list(filter(lambda x: x['type'] == 'soccer_ball', gifts))
    toy_kitchen = list(filter(lambda x: x['type'] == 'toy_kitchen', gifts))

    sorted_educational_games = sorted(educational_games, key=lambda x: x['price'])[:200]
    sorted_music_games = sorted(music_games, key=lambda x: x['price'])[:200]
    sorted_bath_toys = sorted(bath_toys, key=lambda x: x['price'])[:200]
    sorted_bike = sorted(bike, key=lambda x: x['price'])
    sorted_paints = sorted(paints, key=lambda x: x['price'])
    sorted_casket = sorted(casket, key=lambda x: x['price'])[:200]
    sorted_soccer_ball = sorted(soccer_ball, key=lambda x: x['price'], reverse=True)[:200]
    sorted_toy_kitchen = sorted(toy_kitchen, key=lambda x: x['price'])
    gifts_qw = [sorted_bath_toys, sorted_educational_games, sorted_casket, sorted_soccer_ball, sorted_music_games]

    gifts_rt = []
    for gifts in gifts_qw:
        for gift in gifts:
            gifts_rt.append(gift)

    points = get_children_addresses(children)
    stack_of_bags = get_gift_baskets(gifts_rt)

    # Для каждого мешка определяем размер кластера и создаем его с ближайшими точками
    for bag in stack_of_bags:
        cluster_len = len(bag)
        cluster = create_cluster(points, cluster_len)

        # Добавляем готовые данные в наш будущий JSON
        request["moves"].extend({"x": _[0], "y": _[1]} for _ in cluster)
        request["stackOfBags"].insert(0, bag)

        # После обхода детей в кластере возвращаемся на базу
        request["moves"].append({"x": 0, "y": 0})

    # Делаем запись в файл
    file_path = Path(__file__).parent.parent.joinpath('result.json')
    write_to_file(dict_to_str_like_json(request), file_path)

    # Отправляем данные на сервер и получаем результат
    r = post_json(request)

    # Получаем результат
    round_id = re.search(r'"roundId":"(.*)"', r.text).group(1)
    logger.debug("Round ID = {}".format(round_id))
    if round_id:
        get_result(round_id)


if __name__ == '__main__':
    main()
