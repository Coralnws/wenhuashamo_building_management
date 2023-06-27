from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import *
from django.views.decorators.csrf import csrf_exempt
from ..utils import *
from django.utils import timezone
import datetime
from api.views.paymentManageApi import *

REQUEST_RENTAL_ID = 'rental_id'
REQUEST_TENANT_ID = 'tenant_id'
REQUEST_CONTRACT_ID = 'contract_id'
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
    contract_id = info.get(REQUEST_CONTRACT_ID)
    room_id = info.get(REQUEST_ROOM_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)

    room_list = room_id.split(",")
    print(room_list)

    tenant_exist = Tenant.objects.filter(id=tenant_id).first()

    rental_exist = RentalInfo.objects.filter(tenant=tenant_exist,contract_id=contract_id).first()
    if rental_exist:
        return return_response(4001, '合约编号已存在')

    if tenant_exist is None:
        return return_response(9999, '客户不存在')
    
    #添加合约
    rental_info = RentalInfo()
    rental_info.contract_id = contract_id
    rental_info.tenant = tenant_exist
    rental_info.createdTime = date_sign
    rental_info.startTime = date_begin
    rental_info.endTime = date_end
    rental_info.save()

    date_end_str = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    date_begin_str = datetime.datetime.strptime(date_begin, '%Y-%m-%d')
    status = None

    if date_begin_str <= timezone.now() and date_end_str >= timezone.now():
        status=True
    else:
        status=False
        
    #为每个房间建立TenantRental关系 - house + rental
    for room in room_list:
        house = House.objects.filter(roomNumber = room).first()
        if house is None:
            return return_response(3001, '房间不存在')
        
        #检查房屋在这个时间段是不是已经出租
        #拿这个房间的所有租赁信息
        rent_room_list = TenantRental.objects.filter(house=house)
        #检查这些租赁信息里面有没有重叠的
        for record in rent_room_list:
            if (record.rental.startTime >= date_begin_str and record.rental.startTime <= date_end_str) or (record.rental.endTime >= date_begin_str and record.rental.endTime <= date_end_str) or     (record.rental.startTime <= date_begin_str and record.rental.endTime >= date_end_str) or(date_begin_str <= record.rental.startTime and record.rental.endTime <= date_end_str):
                rental_info.delete()
                return return_response(2001, '该时间段房间已出租',room)

        house.status = status
        house.save()
        rent = TenantRental(house=house,rental=rental_info)
        rent.save()

    # populate contract duration and create payment records
    payments = []
    curr_start = date_begin_str
    while curr_start < date_end_str:
        curr_end = curr_start.replace(year=curr_start.year + 1)
        payment = Payment()
        payment.start_time = curr_start
        payment.end_time = curr_end
        payment.period = curr_start.strftime("%Y.%m") + "-" + curr_end.strftime("%Y.%m")
        payment.is_paid = False
        payment.amount = 0
        payment.rentalInfo = rental_info
        payment.tenant = tenant_exist
        payment.save()

        payment_item = {}
        payment_item['payment_id'] = payment.id
        payment_item[REQUEST_CONTRACT_ID] = payment.rentalInfo.contract_id
        payment_item['period'] = payment.period
        payment_item['paymentTime'] = payment.paymentTime
        payments.append(payment_item)

        curr_start = curr_end   # reassign the start year with end year

    data=model_to_dict(rental_info)
    data['id'] = rental_info.id
    room_list = TenantRental.objects.filter(rental = rental_info)
    room_data = []
    for room in room_list:
        room_data.append(room.house.roomNumber)
    data['room_data'] = room_data
    data['property_fees_data'] = payments

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息新建成功', 'data':data})

'''
    @param:
    - user_id:'1', //用户ID
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

    rental_id = request.GET.get(REQUEST_RENTAL_ID, '')

    rental_info = RentalInfo.objects.filter(id=rental_id).first()

    if rental_info is None:
        return return_response(99999, '租赁信息不存在')

    rental_detail_info = {}
    rental_detail_info[REQUEST_RENTAL_ID] = rental_info.id
    rental_detail_info[REQUEST_DATE_BEGIN] = rental_info.startTime
    rental_detail_info[REQUEST_DATE_END] = rental_info.endTime
    rental_detail_info[REQUEST_DATE_SIGN] = rental_info.createdTime
    rental_detail_info[REQUEST_IS_PAID_MANAGEMENT] = rental_info.ispaid_management
    rental_detail_info[REQUEST_DATE_PAID_MANAGEMENT] = rental_info.paidManagementDate
    rental_detail_info[REQUEST_IS_PAID_RENTAL] = rental_info.ispaid_rental
    rental_detail_info[REQUEST_DATE_PAID_RENTAL] = rental_info.paidRentalDate
    rental_detail_info[REQUEST_ROOM_ID] = rental_info.house.roomNumber
    rental_detail_info[REQUEST_USERNAME] = rental_info.tenant.username
    rental_detail_info[REQUEST_LEGAL_NAME] = rental_info.tenant.real_name
    rental_detail_info[REQUEST_COM_NAME] = rental_info.tenant.company
    rental_detail_info[REQUEST_PHONE] = rental_info.tenant.contactNumber

    return return_response(9999, '租赁信息修改成功', rental_detail_info)



@csrf_exempt
def rent_user_detail_read(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    user_id = request.GET.get(REQUEST_USER_ID, '')

    tenant_exist = Tenant.objects.filter(id=user_id).first()
    
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
    - user_id:'1', //用户ID
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

    tenant_id = info.get(REQUEST_TENANT_ID)
    contract_id = info.get(REQUEST_CONTRACT_ID)
    room_id = info.get(REQUEST_ROOM_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)

    tenant_exist = Tenant.objects.filter(id=tenant_id).first()
    rental_info = RentalInfo.objects.filter(tenant=tenant_exist,contract_id=contract_id).first()

    if tenant_exist is None or rental_info is None:
        return return_response(9999, '客户或租赁信息不存在')

    if date_sign:
        rental_info.createdTime = date_sign
    if date_begin:
        rental_info.startTime = date_begin
    if date_end:
        rental_info.endTime = date_end
    rental_info.save()

    if room_id is None:
        return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息修改成功'})

    date_end_str = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    date_begin_str = datetime.datetime.strptime(date_begin, '%Y-%m-%d')

    status = None
    if date_begin_str <= timezone.now() and date_end_str >= timezone.now():
        status=True
    else:
        status=False

    new_room_list = room_id.split(",")

    room_list_exist = TenantRental.objects.filter(rental = rental_info)

    for record in room_list_exist:
        if record.house.roomNumber in new_room_list:
            record.house.status = status
            record.house.save()
            new_room_list.remove(record.house.roomNumber)
        else:
            if record.rental.endTime >= timezone.now() and record.rental.startTime <= timezone.now():    
                record.house.status = not record.house.status
                record.house.save()
                record.delete()

    for room in new_room_list:
        house = House.objects.filter(roomNumber = room).first()
        if house is None:
            return return_response(3001, '房间不存在')
        
        #这边可以添加判断房屋在这个时间段是不是已经出租
        
        rent_room_list = TenantRental.objects.filter(house=house)

        for rent_room in rent_room_list:
            if (record.rental.startTime >= date_begin_str and record.rental.startTime <= date_end_str) or (record.rental.endTime >= date_begin_str and record.rental.endTime <= date_end_str) or     (record.rental.startTime <= date_begin_str and record.rental.endTime >= date_end_str) or(date_begin_str <= record.rental.startTime and record.rental.endTime <= date_end_str) and rent_room.rental != rental_info:
                return return_response(2001, '该时间段房间已出租',room)
#
        house.status = status
        house.save()
        rent = TenantRental(house=house,rental=rental_info)
        rent.save()
        
    data=model_to_dict(rental_info)
    
    room_list = TenantRental.objects.filter(rental = rental_info)
    room_data = []
    for room in room_list:
        room_data.append(room.house.roomNumber)
    data['room_data'] = room_data

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息修改成功', 'data':data})

@csrf_exempt
def rent_delete(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
    
    info = request.POST.dict()

    tenant_id = info.get(REQUEST_TENANT_ID)
    contract_id = info.get(REQUEST_CONTRACT_ID)

    tenant_exist = Tenant.objects.filter(id=tenant_id).first()
    rental_info = RentalInfo.objects.filter(tenant=tenant_exist,contract_id=contract_id).first()

    room_list_exist = TenantRental.objects.filter(rental = rental_info)
        
    for record in room_list_exist:
        if rental_info.startTime <= timezone.now() and rental_info.endTime >= timezone.now(): #当前仍在租赁
            record.house.status = False
            record.house.save()
        
        record.delete()
    
    rental_info.delete()

    return UTF8JsonResponse({'errno':1001, 'msg': '租赁信息删除成功'})