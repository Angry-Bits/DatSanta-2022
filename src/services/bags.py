import json
from os.path import abspath


def delete_id(array, numbers):
    for item in array:
        if isinstance(item, dict):
            if item['id'] in numbers:
                array[array.index(item)] = 'shipped'
    new_massive = list(filter(lambda a: a != 'shipped', array))
    return new_massive


path = 'Hackathon-DatSanta-2022/'
map = open(abspath(path + 'map2.json'), 'r')
json_map = json.loads(map.read())
gifts = json_map['gifts']
bags = []


def get_bags(newlist):
    check = list(filter(lambda item: isinstance(item, dict), newlist))
    if len(check) != 0:
        weight = 0
        volume = 0
        bag = []
        for i, item in enumerate(newlist):
            weight += item.get('weight')
            volume += item.get('volume')
            bag.append(item.get('id'))
            if weight > 200 or volume > 100:
                print(f"{weight - item.get('weight')} вес \
                        {volume - item.get('volume')} объем")
                bags.append(bag[:-1])
                new_massive = delete_id(newlist, bag[:-1])
                return get_bags(new_massive)
            if len(newlist) == i + 1:
                bags.append(bag)


print(get_bags(gifts))
print(bags)
print(len(bags))
n = 0
for bag in bags:
  n += len(bag)
print(f'всего подарков нафасовано: {n}')

n2 = 0
for bag in bags:
  n2 += len(set(bag))
print(f'всего уникальных подарков нафасовано: {n2}')
