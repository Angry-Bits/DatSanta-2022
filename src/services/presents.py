from typing import List, Dict, Any, Optional, Literal


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


##############################################################################################
# Приведенный ниже отбор подарков использовали во втором раунде, но не использовали в финале #
##############################################################################################


gift_for_male = [
    'constructors', 'radio_controlled_toys', 'toy_vehicles', 'board_games',
    'outdoor_games', 'playground', 'computer_games', 'sweets'
]
gift_for_female = [
    'dolls', 'board_games', 'outdoor_games', 'playground', 'soft_toys',
    'sweets', 'books', 'pet', 'clothes'
]

gift_younger_5 = [
    'constructors', 'dolls', 'radio_controlled_toys', 'toy_vehicles',
    'board_games', 'outdoor_games', 'playground', 'soft_toys', 'sweets',
    'books', 'pet', 'clothes'
]
gift_older_5 = [
    'constructors', 'radio_controlled_toys', 'toy_vehicles', 'board_games',
    'outdoor_games', 'playground', 'computer_games', 'sweets'
]

MAX_BUDGET = 50000


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
