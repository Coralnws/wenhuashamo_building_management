
from django.core import serializers

from api.models import House
from api.utils import UTF8JsonResponse


def house_list_by_floor(request):
    if request.method == 'POST':
        floor = request.GET.get('floor')
        if floor == 0:
            houses = House.objects.all()
        else:
            houses = House.objects.all().filter(floor=floor)

        houseList = []
        for house in houses:
            houseData = {}
            houseData['id'] = house.id
            houseData['room_number'] = house.roomNumber
            houseData['status'] = house.status
            houseData['rental_info'] = house.rentalInfo

            houseList.append(houseData)

        return UTF8JsonResponse({'errno': 1001, 'msg': '返回房间列表成功', 'data': houseList})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})
    # for house in houses:
    #     if house.floor not in floors:
    #         floors[house.floor] = {
    #             'rooms': [],
    #             'vacant_count': 0,
    #             'rented_count': 0,
    #         }
    #     if house.status:
    #         floors[house.floor]['rented_count'] += 1
    #     else:
    #         floors[house.floor]['vacant_count'] += 1
    #     floors[house.floor]['rooms'].append(house)
    #
    # # 计算每层房间状态的总占比
    # total_count = len(houses)
    # for floor in floors.values():
    #     floor['vacant_ratio'] = floor['vacant_count'] / total_count * 100
    #     floor['rented_ratio'] = floor['rented_count'] / total_count * 100
