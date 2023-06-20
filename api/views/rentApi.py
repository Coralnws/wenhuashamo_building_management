from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import *
from django.views.decorators.csrf import csrf_exempt
from ..utils import *
from django.utils import timezone
import datetime

REQUEST_RENTAL_ID = 'rental_id'
REQUEST_TENANT_ID = 'tenant_id'
REQUEST_USER_ID = 'user_id'
REQUEST_IS_DELETE = 'is_delete'
REQUEST_COM_NAME = 'com_name'
REQUEST_LEGAL_NAME = 'legal_name'
REQUEST_USERNAME = 'username'
REQUEST_PHONE = 'phone'
REQUEST_RENT_DATA = 'rent_data'
REQUEST_ROOM_ID = 'room_id'
REQUEST_DATE_BEGIN = 'date_begin'
REQUEST_DATE_END = 'date_end'
REQUEST_DATE_SIGN = 'date_sign'
REQUEST_IS_PAID_MANAGEMENT = 'is_paid_management'
REQUEST_DATE_PAID_MANAGEMENT = 'date_paid_management'
REQUEST_IS_PAID_RENTAL = 'is_paid_rental'
REQUEST_DATE_PAID_RENTAL = 'date_paid_rental'


@csrf_exempt
def rent_create(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
        
    info = request.POST.dict()
    
    tenant_id = info.get(REQUEST_TENANT_ID)
    room_id = info.get(REQUEST_ROOM_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)

    #ispaid_management = info.get(REQUEST_IS_PAID_MANAGEMENT)
    #date_paid_management = info.get(REQUEST_DATE_PAID_MANAGEMENT)

    room_exist = House.objects.filter(roomNumber=room_id).first()

    datetime_obj = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    if datetime_obj < timezone.now():
        room_exist.status=False
        room_exist.save()
    else:
        room_exist.status=True
        room_exist.save()


    tenant_exist = Tenant.objects.filter(id=tenant_id).first()

    if room_exist is None or tenant_exist is None:
        return return_response(9999, '房间或者客户不存在')
    print(room_exist)
    rental_info = RentalInfo()
    rental_info.house = room_exist
    rental_info.tenant = tenant_exist
    rental_info.createdTime = date_sign
    rental_info.startTime = date_begin
    rental_info.endTime = date_end
    #rental_info.ispaid_management = ispaid_management
    #rental_info.paidManagementDate = date_paid_management
    rental_info.save()
    data=model_to_dict(rental_info)

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息新建成功', 'data':data})

'''s
    @param:
    - user_ID:'1', //用户ID
    - date_begin:'', //租赁开始时间
    - date_end:'', //租赁结束时间
    - date_sign:'', // 签约时间
    - if_pay:'', //是否缴纳物业费
    - pay_time:'' //物业费缴纳时间
'''
@csrf_exempt
def rent_detail_read(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    rental_ID = request.GET.get(REQUEST_RENTAL_ID, '')

    rental_info = RentalInfo.objects.filter(id=rental_ID).first()

    if rental_info is None:
        return return_response(99999, '租赁信息不存在')

    rentalDetailInfo = {}
    rentalDetailInfo[REQUEST_RENTAL_ID] = rental_info.id
    rentalDetailInfo[REQUEST_DATE_BEGIN] = rental_info.startTime
    rentalDetailInfo[REQUEST_DATE_END] = rental_info.endTime
    rentalDetailInfo[REQUEST_DATE_SIGN] = rental_info.createdTime
    rentalDetailInfo[REQUEST_IS_PAID_MANAGEMENT] = rental_info.ispaid_management
    rentalDetailInfo[REQUEST_DATE_PAID_MANAGEMENT] = rental_info.paidManagementDate
    rentalDetailInfo[REQUEST_IS_PAID_RENTAL] = rental_info.ispaid_rental
    rentalDetailInfo[REQUEST_DATE_PAID_RENTAL] = rental_info.paidRentalDate
    rentalDetailInfo[REQUEST_ROOM_ID] = rental_info.house.roomNumber
    rentalDetailInfo[REQUEST_USERNAME] = rental_info.tenant.username
    rentalDetailInfo[REQUEST_LEGAL_NAME] = rental_info.tenant.real_name
    rentalDetailInfo[REQUEST_COM_NAME] = rental_info.tenant.company
    rentalDetailInfo[REQUEST_PHONE] = rental_info.tenant.contactNumber

    return return_response(9999, '租赁信息修改成功', rentalDetailInfo)



@csrf_exempt
def rent_user_detail_read(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    user_ID = request.GET.get(REQUEST_USER_ID, '')

    tenant_exist = Tenant.objects.filter(id=user_ID).first()
    
    if tenant_exist is None:
        return return_response(99999, '客户不存在')

    user_level_rental_detail = {}
    user_level_rental_detail[REQUEST_USERNAME] = tenant_exist.username
    user_level_rental_detail[REQUEST_LEGAL_NAME] = tenant_exist.real_name
    user_level_rental_detail[REQUEST_COM_NAME] = tenant_exist.company
    user_level_rental_detail[REQUEST_PHONE] = tenant_exist.contactNumber

    rental_infos = RentalInfo.objects.filter(tenant=tenant_exist)

    rent_data_list = []
    for rent in rental_infos:
        rent_data = {}
        rent_data[REQUEST_RENTAL_ID] = rent.id
        rent_data[REQUEST_DATE_BEGIN] = rent.startTime
        rent_data[REQUEST_DATE_END] = rent.endTime
        rent_data[REQUEST_DATE_SIGN] = rent.createdTime
        rent_data[REQUEST_IS_PAID_MANAGEMENT] = rent.ispaid_management
        rent_data[REQUEST_DATE_PAID_MANAGEMENT] = rent.paidManagementDate
        rent_data[REQUEST_IS_PAID_RENTAL] = rent.ispaid_rental
        rent_data[REQUEST_DATE_PAID_RENTAL] = rent.paidRentalDate
        rent_data[REQUEST_ROOM_ID] = rent.house.roomNumber
        rent_data_list.append(rent_data)

    user_level_rental_detail[REQUEST_RENT_DATA] = rent_data_list

    return return_response(9999, '租赁信息修改成功', user_level_rental_detail)


'''s
    @param:
    - user_ID:'1', //用户ID
    - date_begin:'', //租赁开始时间
    - date_end:'', //租赁结束时间
    - date_sign:'', // 签约时间
    - if_pay:'', //是否缴纳物业费
    - pay_time:'' //物业费缴纳时间
'''
@csrf_exempt
def rent_update(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')

    info = request.POST.dict()

    tenant_ID = info.get(REQUEST_TENANT_ID)
    room_ID = info.get(REQUEST_ROOM_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)
    # ispaid_management = info.get(REQUEST_IS_PAID_MANAGEMENT)
    # date_paid_management = info.get(REQUEST_DATE_PAID_MANAGEMENT)

    tenant_exist = Tenant.objects.filter(id=tenant_ID).first()
    house = House.objects.filter(roomNumber=room_ID).first()

    rental_info = RentalInfo.objects.filter(tenant=tenant_exist,house=house).first()

    if tenant_exist is None or rental_info is None:
        return return_response(9999, '客户或租赁信息不存在')


    #rental_info.tenant = tenant_exist
    rental_info.createdTime = date_sign
    rental_info.startTime = date_begin
    rental_info.endTime = date_end

    datetime_obj = datetime.datetime.strptime(
    rental_info.endTime, '%Y-%m-%d')

    if datetime_obj < timezone.now():
        house.status=False
        house.save()
    else:
        house.status=True
        house.save()
    # rental_info.ispaid_management = ispaid_management
    # rental_info.paidManagementDate = date_paid_management
    rental_info.save()

    data=model_to_dict(rental_info)

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息修改成功', 'data':data})

@csrf_exempt
def rent_delete(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
    
    info = request.POST.dict()

    tenant_ID = info.get(REQUEST_TENANT_ID)
    room_ID = info.get(REQUEST_ROOM_ID)

    tenant_exist = Tenant.objects.filter(id=tenant_ID).first()
    house_exist = House.objects.filter(roomNumber=room_ID).first()
    rental_info = RentalInfo.objects.filter(tenant=tenant_exist,house=house_exist).first()

    #datetime_obj = datetime.datetime.strptime(rental_info.endTime, '%Y-%m-%d')

    if rental_info.endTime > timezone.now():
        house_exist.status=False
        house_exist.save()

    rental_info.delete()

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息删除成功'})