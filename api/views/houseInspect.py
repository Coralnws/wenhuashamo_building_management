from django.shortcuts import render, get_object_or_404

from api.models import House


def house_list(request):
    houses = House.objects.all()

    floors = {}
    for house in houses:
        if house.floor not in floors:
            floors[house.floor] = {
                'rooms': [],
                'vacant_count': 0,
                'rented_count': 0,
            }
        if house.status:
            floors[house.floor]['rented_count'] += 1
        else:
            floors[house.floor]['vacant_count'] += 1
        floors[house.floor]['rooms'].append(house)

    # 计算每层房间状态的总占比
    total_count = len(houses)
    for floor in floors.values():
        floor['vacant_ratio'] = floor['vacant_count'] / total_count * 100
        floor['rented_ratio'] = floor['rented_count'] / total_count * 100

    return render(request, 'house_list.html', {'houses': houses, 'floors': floors})


