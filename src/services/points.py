import math
from typing import List, Tuple


def create_cluster(points: List[Tuple[float, float]],
                   num_points: int) -> List[Tuple[float, float]]:
    cluster = []

    # Находим точку с минимальной дистанцией до начала координат
    closest_point = min(
        points, key=lambda point: math.sqrt(point[0]**2 + point[1]**2)
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
                [math.sqrt((point[0] - c[0]) ** 2 + \
                    (point[1]-c[1]) ** 2) for c in cluster]
            )
        )
        # Добавляем точку в кластер
        cluster.append(closest_point)

        # Удаляем точку из списка points
        points.remove(closest_point)

    return cluster
