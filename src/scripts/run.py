from src.services.points import create_cluster, get_children_addresses
from src.services.baskets import get_gift_baskets
from src.services.system import write_to_file, dict_to_json_str, RESULT_JSON_PATH
from src.services.net import get_map, post_json, MAP_ID


def main(map_id: str = MAP_ID):
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
    points = get_children_addresses(children)
    stack_of_bags = get_gift_baskets(gifts, selection='id')

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
    data = dict_to_json_str(request)
    write_to_file(data, RESULT_JSON_PATH)

    # Отправляем данные на сервер
    post_json(request)


if __name__ == '__main__':
    main()
