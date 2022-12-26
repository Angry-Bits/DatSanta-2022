""" from typing import List, Tuple


def get_nearest_cluster(points: List[Tuple[float, float]],
                        k: int) -> List[Tuple[float, float]]:
    clusters = []
    while points:
        point = points.pop(0)
        # Найти ближайшую точку
        nearest_point = min(points, key=lambda p: ((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) ** 0.5)
        # Найти ближайший кластер
        nearest_cluster = None
        min_distance = float('inf')
        for cluster in clusters:
            for p in cluster:
                d = ((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) ** 0.5
                if d < min_distance:
                    min_distance = d
                    nearest_cluster = cluster
        # Если расстояние до ближайшего кластера меньше расстояния до ближайшей точки,
        # то добавить точку и ближайшую точку в кластер
        if min_distance < ((point[0] - nearest_point[0]) ** 2 + (point[1] - nearest_point[1]) ** 2) ** 0.5:
            nearest_cluster.extend([point, nearest_point])
            points.remove(nearest_point)
        # Иначе создать новый кластер
        else:
            clusters.append([point, nearest_point])
            points.remove(nearest_point)
    return clusters """


""" import math
from typing import List, Tuple


X_CENTER = 0
Y_CENTER = 0


def get_nearest_cluster(points: List[Tuple[float, float]],
                        k: int) -> List[Tuple[float, float]]:    
    # Сортируем точки по расстоянию до центра координат
    sorted_points = sorted(
        points, key=lambda point: math.sqrt(
            (point[0] - X_CENTER) ** 2 + (point[1] - Y_CENTER) ** 2
        )
    )
    # Возвращаем первые k точек из отсортированного списка
    return sorted_points[:k] """


""" def get_density_based_clustering(points, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(points)
    claster_labels = kmeans.predict(points)
    claster_centers = kmeans.cluster_centers_
    sorted_centers = sorted(claster_centers, key=lambda x: np.linalg.norm(x))
    nearest_cluster = sorted_centers[0]
    nearest_cluster_indices = [i for i, label in enumerate(claster_labels) if label == nearest_cluster]
    return [points[i] for i in nearest_cluster_indices] """

""" # Сортируем список подарков по убыванию соотношения ценности (веса/объема)
    gifts.sort(key=lambda x: x['weight'] / x['volume'], reverse=True)

    # Список мешков
    baskets = []

    # Проходим по всему списку подарков
    for gift in gifts:
        gift_added = False
        # Проходим по всем мешкам
        for basket in baskets:
            basket['stack'] = []
            # Если подарок вмещается в мешок по весу и объему, то добавляем его туда
            if basket['weight'] + gift['weight'] <= max_weight and \
                    basket['volume'] + gift['volume'] <= max_volume:
                basket['weight'] += gift['weight']
                basket['volume'] += gift['volume']
                basket['stack'].append(gift['id'])
                gift_added = True
        # Если подарок не добавили ни в один мешок, то создаем новый мешок и добавляем подарок туда
        if not gift_added:
            baskets.append(
                {
                    'weight': gift['weight'],
                    'volume': gift['volume'],
                    'stack': gift['id']
                }
            ) """


""" def extract_from_baskets(baskets: List[List[Dict[Literal['id', 'weight', 'volume'], int]]],
                         entity: Literal['id', 'weight', 'volume'] = 'id') -> List[List[int]]:
    '''
    Вытаскакивает из массива подарков заданные свойства (ID, вес, объем).
    По умолчанию берутся по ID.
    '''
    return [list(map(lambda x: x[entity], basket)) for basket in baskets] """


""" data = get_map(map_id)
    gifts2 = data.get('gifts')[:10]
    get_bags(gifts2)
    return bags """
