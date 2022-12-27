import math
from typing import List, Dict, Tuple


def create_cluster(points: List[Tuple[float, float]],
                   num_points: int) -> List[Tuple[float, float]]:
    cluster = []

    # Находим точку с минимальной дистанцией до начала координат
    closest_point = min(
        points, key=lambda point: math.sqrt(point[0] ** 2 + point[1] ** 2)
    )
    # Добавляем точку в кластер
    cluster.append(closest_point)

    # Удаляем точку из списка points
    points.remove(closest_point)

    # Продолжаем добавление точек в кластер, пока не добавим num_points точек
    while len(cluster) < num_points:
        # Находим точку с минимальной дистанцией до точек в кластере
        closest_point = min(
            points, key=lambda point: min(
                [math.sqrt((point[0] - c[0]) ** 2 +
                    (point[1] - c[1]) ** 2) for c in cluster]
            )
        )
        # Добавляем точку в кластер
        cluster.append(closest_point)

        # Удаляем точку из списка points
        points.remove(closest_point)

    return cluster


def sort_cluster(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    # Список результата, в который будем добавлять точки в нужном порядке
    result = []
    # Находим начальную точку - самую ближайшую к центру координат
    start = find_nearest_point(points)
    # Добавляем ее в список результата
    result.append(start)
    # Сет точек, которые еще не были посещены
    unvisited = set(points) - {start}

    # Пока есть непосещенные точки
    while unvisited:
        current = None
        # Находим точку с соседями из списка результата
        for point in result:
            # Соседи - точки, которые не в списке результата
            neighbors = set(points) - set(result)
            # Если у точки есть соседи, то выбираем эту точку
            if neighbors:
                current = point
                break

        # Если не нашли точки
        if not current:
            break

        nearest = min(
            neighbors, key=lambda neighbor:
                (current[0] - neighbor[0]) ** 2 +
                    (current[1] - neighbor[1]) ** 2
        )
        # Добавляем ближайшую точку и убираем ее их непосещенных
        result.append(nearest)
        unvisited.remove(nearest)

    return result


def find_nearest_point(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    # Функция, которая находит самую ближайшую точку к центру координат
    return min(points, key=lambda point: (point[0] - 0) ** 2 + (point[1] - 0) ** 2)


def get_children_addresses(children: List[Dict[str, float]]) -> List[Tuple[float, float]]:
    # Преобразует данные в списке вида {'x': float, 'y': float} в (float, float)
    return list(tuple(point.values()) for point in children)
