import json

from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Tenant, RentalInfo, Payment
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
        real_name = request.POST.get('real_name')
        company = request.POST.get('company')
        contact_name = request.POST.get('contactName')
        contact_number = request.POST.get('contactNumber')
        # 创建新的客户对象并保存到数据库中
        tenant = Tenant(real_name=real_name, company=company,
                        contactName=contact_name,
                        contactNumber=contact_number)
        tenant.save()

        realname_exist = CustomUser.objects.filter(realname=real_name).count()
        username_exist = CustomUser.objects.filter(username=real_name).count()
        username = real_name
        if realname_exist > 0 or username_exist:
            if realname_exist == username_exist:
                username  = username+"_"+str(realname_exist)
            if username_exist < realname_exist:
                if username_exist != 0:
                    username  = username+"_" + str(realname_exist)

        new_user = CustomUser(tenant=tenant,username=username,realname=real_name,position='1',contactNumber=contact_number)
        new_user.set_password(DEFAULTPASS)
        new_user.save()

        data = {}
        data['username'] = new_user.username
        data['realname'] = new_user.realname
        data['position'] = new_user.position
        data['contact_number'] = new_user.contactNumber


        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant added successfully!','data':data})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def delete_tenant(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tenant = Tenant.objects.filter(id=user_id).first()
        tenant.delete()
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant deleted successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def update_tenant(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tenant = Tenant.objects.filter(id=user_id).first()
        # 更新客户信息
        tenant.real_name = request.POST.get('real_name')
        tenant.company = request.POST.get('company')
        tenant.contactName = request.POST.get('contactName')
        tenant.contactNumber = request.POST.get('contactNumber')

        # 保存客户对象到数据库中
        tenant.save()

        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant updated successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def search_tenant(request):
    if request.method == 'POST':
        search_word = request.POST.get('search_word')
        tenant = Tenant.objects.filter(
            Q(real_name__icontains=search_word) |
            Q(company__icontains=search_word) |
            Q(contactNumber__icontains=search_word) |
            Q(contactName__icontains=search_word) |
            Q(real_name__contains=search_word) |
            Q(company__contains=search_word) |
            Q(contactNumber__contains=search_word) |
            Q(contactName__contains=search_word)
        ).first()
        if tenant is None:
            return UTF8JsonResponse({'errno': 100001, 'msg': '不存在这样的用户'})

        tenantDetail = []
        user_level_rental_detail = {}
        user_level_rental_detail[REQUEST_USERNAME] = tenant.contactName
        user_level_rental_detail[REQUEST_LEGAL_NAME] = tenant.real_name
        user_level_rental_detail[REQUEST_COM_NAME] = tenant.company
        user_level_rental_detail[REQUEST_PHONE] = tenant.contactNumber

        rentalInfos = RentalInfo.objects.filter(tenant=tenant)

        rent_data_list = []
        for rent in rentalInfos:
            rent_data = {}
            rent_data[REQUEST_RENTAL_ID] = rent.id
            if rent.startTime:
                rent_data[REQUEST_DATE_BEGIN] = rent.startTime.strftime("%Y-%m-%d %H:%M:%S")
            if rent.endTime:
                rent_data[REQUEST_DATE_END] = rent.endTime.strftime("%Y-%m-%d %H:%M:%S")
            if rent.createdTime:
                rent_data[REQUEST_DATE_SIGN] = rent.createdTime.strftime("%Y-%m-%d %H:%M:%S")
            rent_data[REQUEST_IS_PAID_MANAGEMENT] = rent.ispaid_management
            if rent.paidManagementDate:
                rent_data[REQUEST_DATE_PAID_MANAGEMENT] = rent.paidManagementDate.strftime("%Y-%m-%d")
            rent_data[REQUEST_IS_PAID_RENTAL] = rent.ispaid_rental
            if rent.paidRentalDate:
                rent_data[REQUEST_DATE_PAID_RENTAL] = rent.paidRentalDate.strftime("%Y-%m-%d")
            rent_data[REQUEST_ROOM_ID] = rent.house.roomNumber
            rent_data_list.append(rent_data)

        user_level_rental_detail[REQUEST_RENT_DATA] = rent_data_list
        tenantDetail.append(user_level_rental_detail)
        return UTF8JsonResponse({'errno': 1001, 'msg': '查询客户成功', 'data': tenantDetail})

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
        return UTF8JsonResponse({'errno': 100001, 'msg': '请求格式有误'})

    # user_ID = request.GET.get('user_id')
    #
    # tenant_exist = Tenant.objects.filter(id=user_ID).first()
    #
    # if tenant_exist is None:
    #     return UTF8JsonResponse(99999, '客户不存在')
    page = request.POST.get('page')
    num = request.POST.get('num')
    page = int(page)
    num = int(num)
    left = (page - 1) * num
    right = page * num
    total = Tenant.objects.all().count()
    tenants = Tenant.objects.all()[left:right]

    tenantDetail = []
    for tenant in tenants:
        user_level_rental_detail = {}
        user_level_rental_detail[REQUEST_USER_ID] = tenant.id
        user_level_rental_detail[REQUEST_USERNAME] = tenant.contactName
        user_level_rental_detail[REQUEST_LEGAL_NAME] = tenant.real_name
        user_level_rental_detail[REQUEST_COM_NAME] = tenant.company
        user_level_rental_detail[REQUEST_PHONE] = tenant.contactNumber

        rentalInfos = RentalInfo.objects.filter(tenant=tenant)
        rent_data_list = []
        for rent in rentalInfos:
            rent_data = {}
            rent_data[REQUEST_RENTAL_ID] = rent.id
            if rent.startTime:
                rent_data[REQUEST_DATE_BEGIN] = rent.startTime.strftime("%Y-%m-%d")
            if rent.endTime:
                rent_data[REQUEST_DATE_END] = rent.endTime.strftime("%Y-%m-%d")
            if rent.createdTime:
                rent_data[REQUEST_DATE_SIGN] = rent.createdTime.strftime("%Y-%m-%d")
            rent_data[REQUEST_IS_PAID_MANAGEMENT] = rent.ispaid_management
            if rent.paidManagementDate:
                rent_data[REQUEST_DATE_PAID_MANAGEMENT] = rent.paidManagementDate.strftime("%Y-%m-%d")
            rent_data[REQUEST_IS_PAID_RENTAL] = rent.ispaid_rental
            if rent.paidRentalDate:
                rent_data[REQUEST_DATE_PAID_RENTAL] = rent.paidRentalDate.strftime("%Y-%m-%d")
            rent_data[REQUEST_ROOM_ID] = rent.house.roomNumber
            rent_data_list.append(rent_data)

        user_level_rental_detail[REQUEST_RENT_DATA] = rent_data_list

        paymentInfos = Payment.objects.filter(tenant=tenant)
        property_fees_list = []
        for pay in paymentInfos:
            pay_data = {}
            pay_data['year'] = pay.period
            pay_data['is_paid'] = pay.is_paid
            if pay.paymentTime:
                pay_data['date_pay'] = pay.paymentTime.strftime("%Y-%m-%d")
            pay_data['money'] = pay.amount
            property_fees_list.append(pay_data)
        user_level_rental_detail['property_fees_data'] = property_fees_list

        tenantDetail.append(user_level_rental_detail)

    return UTF8JsonResponse({'errno': 1001, 'msg': '返回客户列表成功', 'data': tenantDetail, 'total': total})
