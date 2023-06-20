from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from api.models import House, RentalInfo, Tenant
from api.utils import UTF8JsonResponse
from django.utils import timezone
import datetime
from django.db.models import Q


@csrf_exempt
def house_list_by_floor(request):
    if request.method == 'GET':
        floor = request.GET.get('floor','')
        if floor == '0':
            houses = House.objects.all().order_by('roomNumber')
        else:
            houses = House.objects.all().filter(floor=floor).order_by('roomNumber')

        houseList = []
        print(len(houses))

        for house in houses:
            house_data = {}
            house_data['id'] = house.id
            house_data['room_number'] = house.roomNumber
            # house_data['status'] = house.status
            house_data['floor'] = house.floor

            rentalInfos = RentalInfo.objects.filter(house=house).order_by('-endTime')
            
            if len(rentalInfos) > 0:
                house_data['status'] = True
            else:
                house_data['status'] = False

            rent_data_list = []

            first=True
            for rent in rentalInfos:
                #datetime_obj = datetime.datetime.strptime(rent.endTime, '%Y-%m-%d')
                if rent.endTime < timezone.now() and first:
                    house.status=False
                    house_data['status'] = house.status
                    house.save()  
                    first=False
                elif first:
                    house.status=True
                    house_data['status'] = house.status
                    house.save()  
                    first=False
                    
                rent_data = {}
                rent_data['start_time'] = rent.startTime
                rent_data['end_time'] = rent.endTime
                rentTenant = Tenant.objects.filter(id=rent.tenant.id).first()
                rent_data['company'] = rentTenant.company
                rent_data['real_name'] = rentTenant.real_name
                rent_data_list.append(rent_data)

            house_data['rent_data'] = rent_data_list
            houseList.append(house_data)

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
