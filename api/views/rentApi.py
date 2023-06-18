from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import *
from django.views.decorators.csrf import csrf_exempt
from ..utils import *


REQUEST_RENTAL_ID = 'rental_id'
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
def rentCreate(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
        
    info = request.POST.dict()
    
    user_ID = info.get(REQUEST_USER_ID)
    room_ID = info.get(REQUEST_ROOM_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)
    ispaid_management = info.get(REQUEST_IS_PAID_MANAGEMENT)
    date_paid_management = info.get(REQUEST_DATE_PAID_MANAGEMENT)


    room_exist = House.objects.filter(roomNumber=room_ID).first()
    tenant_exist = Tenant.objects.filter(id=user_ID).first()

    if room_exist is None or tenant_exist is None:
        return return_response(9999, '房间或者客户不存在')

    rentalInfo = RentalInfo()
    rentalInfo.house = room_exist
    rentalInfo.tenant = tenant_exist
    rentalInfo.createdTime = date_sign
    rentalInfo.startTime = date_begin
    rentalInfo.endTime = date_end
    rentalInfo.ispaid_management = ispaid_management
    rentalInfo.paidManagementDate = date_paid_management
    rentalInfo.save()

    return return_response(9999, '租赁信息新建成功', rentalInfo)


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
def rentDetailRead(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    rental_ID = request.GET.get(REQUEST_RENTAL_ID, '')

    rentalInfo = RentalInfo.objects.filter(id=rental_ID).first()

    if rentalInfo is None:
        return return_response(99999, '租赁信息不存在')

    rentalDetailInfo = {}
    rentalDetailInfo[REQUEST_RENTAL_ID] = rentalInfo.id
    rentalDetailInfo[REQUEST_DATE_BEGIN] = rentalInfo.startTime
    rentalDetailInfo[REQUEST_DATE_END] = rentalInfo.endTime
    rentalDetailInfo[REQUEST_DATE_SIGN] = rentalInfo.createdTime
    rentalDetailInfo[REQUEST_IS_PAID_MANAGEMENT] = rentalInfo.ispaid_management
    rentalDetailInfo[REQUEST_DATE_PAID_MANAGEMENT] = rentalInfo.paidManagementDate
    rentalDetailInfo[REQUEST_IS_PAID_RENTAL] = rentalInfo.ispaid_rental
    rentalDetailInfo[REQUEST_DATE_PAID_RENTAL] = rentalInfo.paidRentalDate
    rentalDetailInfo[REQUEST_ROOM_ID] = rentalInfo.house.roomNumber
    rentalDetailInfo[REQUEST_USERNAME] = rentalInfo.tenant.username
    rentalDetailInfo[REQUEST_LEGAL_NAME] = rentalInfo.tenant.real_name
    rentalDetailInfo[REQUEST_COM_NAME] = rentalInfo.tenant.company
    rentalDetailInfo[REQUEST_PHONE] = rentalInfo.tenant.contactNumber

    return return_response(9999, '租赁信息修改成功', rentalDetailInfo)



@csrf_exempt
def rentUserDetailRead(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    user_ID = request.GET.get(REQUEST_USER_ID, '')

    tenant_exist = Tenant.objects.filter(id=user_ID).first()
    
    if tenant_exist is None:
        return return_response(99999, '客户不存在')

    userLevelRentalDetail = {}
    userLevelRentalDetail[REQUEST_USERNAME] = tenant_exist.username
    userLevelRentalDetail[REQUEST_LEGAL_NAME] = tenant_exist.real_name
    userLevelRentalDetail[REQUEST_COM_NAME] = tenant_exist.company
    userLevelRentalDetail[REQUEST_PHONE] = tenant_exist.contactNumber

    rentalInfos = RentalInfo.objects.filter(tenant=tenant_exist)

    rent_data_list = []
    for rent in rentalInfos:
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

    userLevelRentalDetail[REQUEST_RENT_DATA] = rent_data_list

    return return_response(9999, '租赁信息修改成功', userLevelRentalDetail)


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
def rentUpdate(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')

    info = request.POST.dict()

    rental_ID = info.get(REQUEST_RENTAL_ID)
    user_ID = info.get(REQUEST_USER_ID)
    date_begin = info.get(REQUEST_DATE_BEGIN)
    date_end = info.get(REQUEST_DATE_END)
    date_sign = info.get(REQUEST_DATE_SIGN)
    ispaid_management = info.get(REQUEST_IS_PAID_MANAGEMENT)
    date_paid_management = info.get(REQUEST_DATE_PAID_MANAGEMENT)

    tenant_exist = Tenant.objects.filter(id=user_ID).first()


    rentalInfo = RentalInfo.objects.filter(id=rental_ID).first()

    if tenant_exist is None or rentalInfo is None:
        return return_response(9999, '客户或租赁信息不存在')


    rentalInfo.tenant = tenant_exist
    rentalInfo.createdTime = date_sign
    rentalInfo.startTime = date_begin
    rentalInfo.endTime = date_end
    rentalInfo.ispaid_management = ispaid_management
    rentalInfo.paidManagementDate = date_paid_management
    rentalInfo.save()

    return return_response(9999, '租赁信息修改成功', rentalInfo)


'''

{
    user_ID:'', //用户ID
    is_delete:'', //是否删除
    com_name:'', //公司名
    legal_person:'', // 法人名
    username:'', //联系人姓名
    phone:'', //联系人电话
    rent_data: [
        {
            room: '601',
            date_begin: '2021-5-5',
            date_end: '2024-5-5',
            date_sign: '2021-4-26',
            property_fees: '已缴纳',
            date_pay: '2023-6-3'
        },
        {
            room: '601',
            date_begin: '2021-5-5',
            date_end: '2024-5-5',
            date_sign: '2021-4-26',
            property_fees: '已缴纳',
            date_pay: '2023-6-3'
        },
        {
            room: '601',
            date_begin: '2021-5-5',
            date_end: '2024-5-5',
            date_sign: '2021-4-26',
            property_fees: '已缴纳',
            date_pay: '2023-6-3'
        },
        {
            room: '601',
            date_begin: '2021-5-5',
            date_end: '2024-5-5',
            date_sign: '2021-4-26',
            property_fees: '已缴纳',
            date_pay: '2023-6-3'
        }
    ]
}

'''