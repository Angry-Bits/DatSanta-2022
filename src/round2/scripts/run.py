#!/usr/bin/env python

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import requests

from src.logger import logger


MAP2_ID = 'a8e01288-28f8-45ee-9db4-f74fc4ff02c8'
URL_MAP_GET = 'https://datsanta.dats.team/json/map/{}.json'
URL_JSON_GET = 'https://datsanta.dats.team/api/round2/{}'
URL_JSON_POST = 'https://datsanta.dats.team/api/round2'
TEAM_SECRET_TOKEN = 'bf31be91-70a6-476e-ae99-2b1c50f58ab8'


gift_for_male = ['constructors', 'radio_controlled_toys', 'toy_vehicles', 'board_games', 'outdoor_games', 'playground', 'computer_games', 'sweets']
gift_for_female = ['dolls', 'board_games', 'outdoor_games', 'playground', 'soft_toys', 'sweets', 'books', 'pet', 'clothes']

gift_younger_5 = ['constructors', 'dolls', 'radio_controlled_toys', 'toy_vehicles', 'board_games', 'outdoor_games', 'playground', 'soft_toys', 'sweets', 'books', 'pet', 'clothes']
gift_older_5 = ['constructors', 'radio_controlled_toys', 'toy_vehicles', 'board_games', 'outdoor_games', 'playground', 'computer_games', 'sweets']

MAX_BUDGET = 100000


def select_gifts(gifts: List[Dict[str, Any]], children: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Количество детей, каждому из которых нужно подобрать подарок
    CHILDREN_COUNT = len(children)

    # Сортируем список детей по возрасту в порядке возрастания
    children.sort(key=lambda x: x['age'])

    # Сортируем список подарков по цене в порядке возрастания
    gifts.sort(key=lambda x: x['price'])

    # Общая стоимость подарков и список выбранных подарков
    total_price = 0
    selected_gifts = []

    # Пока количество выбранных подарков меньше CHILDREN_COUNT
    while len(selected_gifts) < CHILDREN_COUNT:
        # Для каждого ребенка в списке детей
        for child in children:
            # Получаем наилучший подарок для ребенка из списка подарков
            best_gift = find_best_gift(gifts, child)
            # Если был найден подходящий подарок
            if best_gift is not None:
                # Добавляем подарок в список выбранных подарков
                selected_gifts.append({'child': child, 'gift': best_gift})
                # Обновляем общую стоимость подарков
                total_price += best_gift['price']
                # Удаляем подарок из списка подарков, чтобы он больше не выбирался
                gifts.remove(best_gift)
        # Если не нашлось подходящего подарка или общая стоимость подарков превышает бюджет
        if best_gift is None or total_price > MAX_BUDGET:
            break

    # Заменяем дешевые подарки на более дорогие
    for presenting in selected_gifts:
        # Получаем наилучший подарок для ребенка из списка подарков
        best_gift = find_best_gift(gifts, presenting['child'])
        # Если подходящий подарок найден и его цена больше, чем цена текущего подарка
        if total_price + best_gift['price'] > MAX_BUDGET:
            return selected_gifts
        if best_gift is not None and best_gift['price'] > presenting['gift']['price']:
            # Обновляем общую стоимость подарков
            total_price -= presenting['gift']['price']
            total_price += best_gift['price']
            # Обновляем подарок в списке выбранных подарков
            presenting['gift'] = best_gift
            # Удаляем подарок из списка подарков, чтобы он больше не выбирался
            gifts.remove(best_gift)
        # Если не нашлось подходящего подарка или общая стоимость подарков превышает бюджет
        if best_gift is None or total_price > MAX_BUDGET:
            break

    return selected_gifts


def find_best_gift(gifts: List[Dict[str, Any]],
                   child: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    best_gift = None

    # Исходя из пола и возраста ребенка формируем
    # наилучшие и предпочтительные варианты подарка
    if child['gender'] == 'female' and child['age'] < 5:
        best_type = 'soft_toys'
        preferred_type = set(gift_for_female) & set(gift_younger_5)
        best_gift = find_by_type(gifts, best_type, preferred_type)

    elif child['gender'] == 'female' and child['age'] >= 5:
        best_type = 'clothes'
        preferred_type = set(gift_for_female) & set(gift_older_5)
        best_gift = find_by_type(gifts, best_type, preferred_type)

    elif child['gender'] == 'male' and child['age'] < 5:
        best_type = 'toy_vehicles'
        preferred_type = set(gift_for_male) & set(gift_younger_5)
        best_gift = find_by_type(gifts, best_type, preferred_type)

    elif child['gender'] == 'male' and child['age'] >= 5:
        best_type = 'computer_games'
        preferred_type = set(gift_for_male) & set(gift_older_5)
        best_gift = find_by_type(gifts, best_type, preferred_type)

    # Если не нашлось подходящего подарка вернуть None
    return best_gift if best_gift else None


def find_by_type(gifts: List[Dict[str, Any]],
                 best_type: str,
                 preferred_type: set) -> Optional[Dict[str, Any]]:
    best_gift = None
    for gift in gifts:
        # Проверяем, есть ли наилучший подарок для ребенка
        if gift['type'] == best_type:
            best_gift = gift
    # Если наилучшего варианта нет, смотрим предпочтительный
    if best_gift is None:
        for gift in gifts:
            # Проверяем, есть ли предпочтительный подарок для ребенка
            if gift['type'] in preferred_type:
                best_gift = gift

    # Если не нашлось подходящего подарка вернуть None
    return best_gift if best_gift else None


def main(map_id: str = MAP2_ID):
    # Формируем словарь, который в итоге отправится на сервер как JSON
    request = {
        "mapID": map_id,
        "presentingGifts": []
    }
    # Скачиваем карту, берем оттуда информацию о подарках и детях
    r = requests.get(URL_MAP_GET.format(map_id))
    data = json.loads(r.text)
    logger.info("Получена карта с ID {}".format(map_id))

    gifts = data.get('gifts')
    children = data.get('children')

    # Обрабатываем данные
    selected_gifts = select_gifts(gifts, children)

    for gift in selected_gifts:
        request['presentingGifts'].append(
            {
                "giftID": gift['gift']['id'],
                "childID": gift['child']['id']
            }
        )
    # Делаем запись в файл
    data = json.dumps(data, indent=4)
    file_path = Path(__file__).parent.parent.joinpath('result.json')
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)

    # Отправляем данные на сервер и получаем результат
    r = requests.post(URL_JSON_POST, json=request, headers={
        "Content-Type": "application/json",
        "X-API-Key": TEAM_SECRET_TOKEN
    })
    logger.info("Отправлены данные на сервер.\n" +  # noqa: W504
                "Код ответа: {}.\nСообщение: {}".format(r.status_code, r.text))


if __name__ == '__main__':
    print(main())
