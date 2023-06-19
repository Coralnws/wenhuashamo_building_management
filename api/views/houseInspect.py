from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from api.models import House, RentalInfo, Tenant
from api.utils import UTF8JsonResponse

@csrf_exempt
def house_list_by_floor(request):
    if request.method == 'POST':
        floor = request.POST.get('floor')
        if floor == '0':
            houses = House.objects.all()
        else:
            houses = House.objects.all().filter(floor=floor)

        print(len(houses))
        houseList = []
        for house in houses:
            houseData = {}
            houseData['id'] = house.id
            houseData['room_number'] = house.roomNumber
            houseData['status'] = house.status
            rentalInfos = RentalInfo.objects.filter(house=house)

            rent_data_list = []

            for rent in rentalInfos:
                rent_data = {}
                rent_data['start_time'] = rent.startTime
                rent_data['end_time'] = rent.endTime
                rentTenant = Tenant.objects.filter(id=rent.tenant.id).first()
                rent_data['company'] = rentTenant.company
                rent_data['real_name'] = rentTenant.real_name
                rent_data_list.append(rent_data)

            houseData['rent_data'] = rent_data_list
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