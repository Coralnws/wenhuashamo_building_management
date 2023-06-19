import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Tenant, RentalInfo
from api.utils import UTF8JsonResponse
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
def add_tenant(request):
    if request.method == 'POST':
        # 从请求中获取客户信息
        real_name = request.GET.get('real_name')
        company = request.GET.get('company')
        contactName = request.GET.get('contactName')
        contactNumber = request.GET.get('contactNumber')
        # 创建新的客户对象并保存到数据库中
        tenant = Tenant(real_name=real_name, company=company,
                        contactName=contactName,
                        contactNumber=contactNumber)
        tenant.save()

        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant added successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def delete_tenant(request):
    if request.method == 'POST':
        company = request.GET.get('company')
        tenant = Tenant.objects.get(company=company)
        tenant.delete()
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant deleted successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def update_tenant(request):
    if request.method == 'POST':
        id = request.GET.get(REQUEST_USER_ID)
        tenant = Tenant.objects.get(id=id)
        # 更新客户信息
        tenant.real_name = request.GET.get(REQUEST_LEGAL_NAME)
        tenant.company = request.GET.get(REQUEST_COM_NAME)
        tenant.contactName = request.GET.get(REQUEST_USERNAME)
        tenant.contactNumber = request.GET.get(REQUEST_PHONE)

        # 保存客户对象到数据库中
        tenant.save()

        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant updated successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def search_tenant(request):
    if request.method == 'POST':
        search_word = request.GET.get('search_word')
        tenant = (
                Tenant.objects.filter(real_name=search_word).first() or
                Tenant.objects.filter(company=search_word).first() or
                Tenant.objects.filter(contactNumber=search_word).first() or
                Tenant.objects.filter(contactName=search_word).first()
        )
        if tenant is None:
            return UTF8JsonResponse(100001, '不存在这样的客户')

        userLevelRentalDetail = {}
        userLevelRentalDetail[REQUEST_USERNAME] = tenant.contactName
        userLevelRentalDetail[REQUEST_LEGAL_NAME] = tenant.real_name
        userLevelRentalDetail[REQUEST_COM_NAME] = tenant.company
        userLevelRentalDetail[REQUEST_PHONE] = tenant.contactNumber

        rentalInfos = RentalInfo.objects.filter(tenant=tenant)

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

        return UTF8JsonResponse({'errno': 1001, 'msg': '查询客户成功', 'data': userLevelRentalDetail})

@csrf_exempt
def view_tenant(request):
    # if request.method == 'POST':
    #     company = request.GET.get('company')
    #     tenant = Tenant.objects.get(company=company)
    #     # tenantRental = Payment.objects.all().filter(tenant)
    #     res = model_to_dict(tenant)
    #     return UTF8JsonResponse({'errno': 1001, 'msg': '返回员工列表成功', 'data': res})
    # else:
    #     return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})
    if request.method != 'POST':
        return UTF8JsonResponse(100001, '请求格式有误，不是GET')

    # user_ID = request.GET.get('user_id')
    #
    # tenant_exist = Tenant.objects.filter(id=user_ID).first()
    #
    # if tenant_exist is None:
    #     return UTF8JsonResponse(99999, '客户不存在')
    page = request.GET.get('page')
    num = request.GET.get('num')
    page = int(page)
    num = int(num)
    left = (page - 1) * num
    right = page * num - 1
    total = Tenant.objects.all().count()
    tenants = Tenant.objects.all()[left:right]

    tenantDetail = []
    for tenant in tenants:
        userLevelRentalDetail = {}
        userLevelRentalDetail[REQUEST_USERNAME] = tenant.contactName
        userLevelRentalDetail[REQUEST_LEGAL_NAME] = tenant.real_name
        userLevelRentalDetail[REQUEST_COM_NAME] = tenant.company
        userLevelRentalDetail[REQUEST_PHONE] = tenant.contactNumber

        rentalInfos = RentalInfo.objects.filter(tenant=tenant)

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

        tenantDetail.append(userLevelRentalDetail)

    return UTF8JsonResponse({'errno': 1001, 'msg': '返回客户列表成功', 'data': tenantDetail, 'total': total})
