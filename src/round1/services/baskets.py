from typing import List, Dict, Literal


def get_gift_baskets(gifts: List[Dict[Literal['id', 'weight', 'volume'], int]],
                     max_weight: int = 200,
                     max_volume: int = 100,
                     selection: Literal['all', 'id', 'weight', 'volume'] = 'all',
                     reverse: bool = False) -> List[List]:
    # Сортируем список подарков по убыванию соотношения ценности (веса/объема)
    # gifts.sort(key=lambda x: x['weight'] / x['volume'], reverse=True)  -  deprecated!

    # Список мешков, которые будут возвращены из функции
    baskets = []

    # Текущий мешок, который мы заполняем:
    current_basket = []

    # Общий вес и объем текущего мешка
    current_weight = 0
    current_volume = 0

    # Проходим по всему списку подарков
    for gift in gifts:
        # Если добавление подарка не превышает лимиты веса и объема,
        # то добавляем его в текущий мешок
        if current_weight + gift['weight'] <= max_weight and \
                current_volume + gift['volume'] <= max_volume:
            current_basket.append(gift)
            current_weight += gift['weight']
            current_volume += gift['volume']
        # Иначе закрываем текущий мешок и начинаем новый
        else:
            baskets.append(current_basket)
            current_basket = [gift]
            current_weight = gift['weight']
            current_volume = gift['volume']

    # Добавляем текущий мешок в список, если он не заполнен
    if current_basket:
        baskets.append(current_basket)

    # Делаем выборку данных. По умолчанию берутся полные данные
    if selection in ['id', 'weight', 'volume']:
        baskets = [list(map(lambda x: x[selection], basket)) for basket in baskets]

    baskets.sort(key=len, reverse=reverse)

    return baskets


print('test commit')
