from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from api.models import House, RentalInfo, Tenant,TenantRental
from api.utils import UTF8JsonResponse
from django.utils import timezone
import datetime
from django.db.models import Q
from api.utils import *
from api.error_utils import *


@csrf_exempt
def house_list_by_floor(request):
    if request.method == 'GET':
        floor = request.GET.get('floor','')
        if floor == '0':
            houses = House.objects.all().order_by('roomNumber')
        else:
            houses = House.objects.all().filter(floor=floor).order_by('roomNumber')

        house_list = []
        print(len(houses))

        for house in houses:
            house_data = {}
            house_data['id'] = house.id
            house_data['room_number'] = house.roomNumber
            house_data['floor'] = house.floor

            rent_record = TenantRental.objects.filter(house=house)

            rent_data_list = []

            renting = False
            for rent in rent_record:
                rent_data = {}
                if rent.rental.startTime <= timezone.now() and rent.rental.endTime >= timezone.now():  #
                    house.status=True
                    house.save()  
                    renting = True
                    
                    rent_data['start_time'] = rent.rental.startTime
                    rent_data['end_time'] = rent.rental.endTime
                    rent_tenant = Tenant.objects.filter(id=rent.rental.tenant.id).first()
                    rent_data['company'] = rent_tenant.company
                    rent_data['real_name'] = rent_tenant.real_name
                    rent_data_list.append(rent_data)
            
            house_data['status'] = renting
            house_data['rent_data'] = rent_data_list
            house_list.append(house_data)

        return UTF8JsonResponse({'errno': 1001, 'msg': '返回房间列表成功', 'data': house_list})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})

@csrf_exempt
def get_company_house(request):
    if request.method != 'GET':
        return not_get_method()
    
    user_id = request.GET.get('user_id','')
    user = CustomUser.objects.filter(id=user_id).first()
    rental_list = None
    if user.tenant is None:
        return return_response(3001, '该用户不属于任何公司')
    
    rental_list = RentalInfo.objects.filter(tenant = user.tenant)

    house_arr = []
    for rental in rental_list:
        rental_info_list = None
        if rental.startTime <= timezone.now() and rental.endTime > timezone.now():
            rental_info_list = TenantRental.objects.filter(rental = rental)
            
            for record in rental_info_list:
                house_arr.append(record.house.roomNumber)

    
    house_arr = list(set(house_arr))
    house_arr = sorted(house_arr)
    
    return return_response(1001, '返回用户所属公司的所有房间',house_arr)


        
        
    
