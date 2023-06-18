from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import *
from django.views.decorators.csrf import csrf_exempt
from ..utils import *



REQUEST_USER_ID = 'user_ID'
REQUEST_IS_DELETE = 'is_delete'
REQUEST_COM_NAME = 'com_name'
REQUEST_LEGAL_PERSON = 'legal_name'
REQUEST_USERNAME = 'username'
REQUEST_PHONE = 'phone'
REQUEST_RENT_DATA = 'rent_data'

REQUEST_ROOM = 'room'
REQUEST_DATE_BEGIN = 'date_begin'
REQUEST_DATE_END = 'date_end'
REQUEST_DATE_SIGN = 'date_sign'
REQUEST_IS_PAID_MANAGEMENT = 'is_paid_management'
REQUEST_DATE_PAID_MANAGEMENT = 'date_paid_management'




@csrf_exempt
def rentCreate(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
        
    info = request.POST.dict()
    
    user_ID = info.get(REQUEST_USER_ID)
    room_ID = info.get(REQUEST_ROOM)
    rent_start_time = info.get(REQUEST_DATE_BEGIN)
    rent_end_time = info.get(REQUEST_DATE_END)
    signing_time = info.get(REQUEST_DATE_SIGN)
    ispaid_management = info.get(REQUEST_IS_PAID_MANAGEMENT)
    date_paid_management = info.get(REQUEST_DATE_PAID_MANAGEMENT)


    room_exist = House.objects.filter(roomNumber=room_ID).first()
    tenant_exist = Tenant.objects.filter(id=user_ID).first()

    if room_exist is None or tenant_exist is None:
        return return_response(9999, '房间或者客户不存在')

    rentalInfo = RentalInfo()
    rentalInfo.house = room_exist
    rentalInfo.tenant = tenant_exist
    rentalInfo.createdTime = signing_time
    rentalInfo.startTime = rent_start_time
    rentalInfo.endTime = rent_end_time
    rentalInfo.lastPay = pay_time
    rentalInfo.ispaid_rental = if_pay
    rentalInfo.save()

    return return_response(9999, '租赁信息新建成功', rentalInfo)


'''s
    @param:
    - user_ID:'1', //用户ID
    - rent_start_time:'', //租赁开始时间
    - rent_end_time:'', //租赁结束时间
    - signing_time:'', // 签约时间
    - if_pay:'', //是否缴纳物业费
    - pay_time:'' //物业费缴纳时间
'''
@csrf_exempt
def rentDetailRead(request):
    if request.method != GETMETHOD:
        return return_response(100001, '请求格式有误，不是GET')

    rental_ID = request.GET.get('rental_ID', '')

    rentalInfo = RentalInfo.objects.filter(id=rental_ID).first()

    if rentalInfo is None:
        return return_response(99999, '租赁信息不存在')

    rentalDetailInfo = {}
    rentalDetailInfo['rental_ID'] = rentalInfo.id
    rentalDetailInfo['rent_start_time'] = rentalInfo.startTime
    rentalDetailInfo['rent_end_time'] = rentalInfo.endTime
    rentalDetailInfo['']


    info = request.POST.dict()

    rental_ID = info.get('rental_ID')
    user_ID = info.get('user_ID')
    rent_start_time = info.get('rent_start_time')
    rent_end_time = info.get('rent_end_time')
    signing_time = info.get('signing_time')
    if_pay = info.get('if_pay')
    pay_time = info.get('pay_time')

    tenant_exist = Tenant.objects.filter(id=user_ID).first()


    rentalInfo = RentalInfo.objects.filter(id=rental_ID).first()

    if tenant_exist is None or rentalInfo is None:
        return return_response(9999, '客户或租赁信息不存在')


    rentalInfo.tenant = tenant_exist
    rentalInfo.startTime = rent_start_time
    rentalInfo.endTime = rent_end_time
    rentalInfo.createdTime = signing_time
    rentalInfo.ispaid_rental = if_pay
    rentalInfo.lastPay = pay_time
    rentalInfo.save()

    return return_response(9999, '租赁信息修改成功', rentalInfo)


'''s
    @param:
    - user_ID:'1', //用户ID
    - rent_start_time:'', //租赁开始时间
    - rent_end_time:'', //租赁结束时间
    - signing_time:'', // 签约时间
    - if_pay:'', //是否缴纳物业费
    - pay_time:'' //物业费缴纳时间
'''
@csrf_exempt
def rentUpdate(request):
    if request.method != POSTMETHOD:
        return return_response(100001, '请求格式有误，不是POST')
        
    info = request.POST.dict()

    rental_ID = info.get('rental_ID')
    user_ID = info.get('user_ID')
    rent_start_time = info.get('rent_start_time')
    rent_end_time = info.get('rent_end_time')
    signing_time = info.get('signing_time')
    if_pay = info.get('if_pay')
    pay_time = info.get('pay_time')

    tenant_exist = Tenant.objects.filter(id=user_ID).first()


    rentalInfo = RentalInfo.objects.filter(id=rental_ID).first()

    if tenant_exist is None or rentalInfo is None:
        return return_response(9999, '客户或租赁信息不存在')


    rentalInfo.tenant = tenant_exist
    rentalInfo.startTime = rent_start_time
    rentalInfo.endTime = rent_end_time
    rentalInfo.createdTime = signing_time
    rentalInfo.ispaid_rental = if_pay
    rentalInfo.lastPay = pay_time
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