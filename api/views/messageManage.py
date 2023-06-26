from datetime import date
import json

from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Tenant, RentalInfo, Payment,TenantRental
from api.utils import UTF8JsonResponse
from ..utils import *

REQUEST_RENTAL_ID = 'rental_id'
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

def check_name_repeat(real_name):
    realname_exist = CustomUser.objects.filter(realname=real_name).count()
    username_exist = CustomUser.objects.filter(username=real_name).count()
    username = real_name
    if realname_exist > 0 or username_exist:
        if realname_exist == username_exist:
            username  = username+"_"+str(realname_exist)
        if username_exist < realname_exist and username_exist != 0:
            username  = username+"_" + str(realname_exist)
    return username

@csrf_exempt
def add_tenant(request):
    if request.method == 'POST':
        # 从请求中获取客户信息
        real_name = request.POST.get('real_name')
        company = request.POST.get('company')
        contact_name = request.POST.get('contactName')
        contact_number = request.POST.get('contactNumber')
        email = request.POST.get('email') or None
        # 创建新的客户对象并保存到数据库中

        tenant = Tenant(real_name=real_name, company=company,
                        contactName=contact_name,
                        contactNumber=contact_number,email=email)
        try:
            tenant.save()
        except Exception as e:
            return UTF8JsonResponse({'errno': 2001, 'msg': '请重新检查所填信息'})

        username = check_name_repeat(real_name)

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
        current_date = date.today()

        rental = RentalInfo.objects.filter(tenant=tenant,endTime__gte=current_date).count()
        payment = Payment.objects.filter(tenant=tenant,is_paid=False).count()

        if rental > 0:
            return UTF8JsonResponse({'errno': 3001, 'msg': '合同未到期，无法删除客户'})
        
        if payment > 0:
            return UTF8JsonResponse({'errno': 4001, 'msg': '客户仍有欠费记录，无法删除客户'})
        
        user_exist = CustomUser.objects.filter(tenant=tenant).first()
        if user_exist:
            user_exist.delete()
        tenant.delete()
    
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant deleted successfully!'})
    else:
        return UTF8JsonResponse({'errno': 9001, 'msg': 'Request Method Error'})


@csrf_exempt
def update_tenant(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tenant = Tenant.objects.filter(id=user_id).first()
        user = CustomUser.objects.filter(tenant=tenant).first()
        # 更新客户信息
        
        real_name = request.POST.get('real_name')
        if real_name != tenant.real_name:
            tenant.real_name = real_name
            username = check_name_repeat(real_name)
            user.username = username
        

        tenant.company = request.POST.get('company')
        try:
            tenant.save()
        except Exception as e:
            return UTF8JsonResponse({'errno': 2001, 'msg': '公司名已存在，请重新填写'})

        tenant.contactName = request.POST.get('contactName')
        tenant.email = request.POST.get('email')

        contact_number = request.POST.get('contactNumber')
        user.contactNumber = contact_number
        tenant.contactNumber = request.POST.get('contactNumber')
        try:
            tenant.save()
        except Exception as e:
            return UTF8JsonResponse({'errno': 2001, 'msg': '联系人电话已被使用，请重新填写'})
        # 保存客户对象到数据库中

        user.save()

        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant updated successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


@csrf_exempt
def search_tenant(request):
    if request.method == 'POST':
        search_word = request.POST.get('search_word')
        try:
            tenant = Tenant.objects.filter(
                Q(real_name__icontains=search_word) |
                Q(company__icontains=search_word) |
                Q(contactNumber__icontains=search_word) |
                Q(contactName__icontains=search_word) |
                Q(real_name__contains=search_word)
            ).first()
        except Exception as e:
            return UTF8JsonResponse({'errno': 10001, 'msg': '客户查询失败：{}'.format(str(e))})
        if not tenant:
            return UTF8JsonResponse({'errno': 100001, 'msg': '不存在这样的用户'})

        tenant_detail = []

        user_level_rental_detail = {}
        user_level_rental_detail[REQUEST_USERNAME] = tenant.contactName
        user_level_rental_detail[REQUEST_LEGAL_NAME] = tenant.real_name
        user_level_rental_detail[REQUEST_COM_NAME] = tenant.company
        user_level_rental_detail[REQUEST_PHONE] = tenant.contactNumber
        user_level_rental_detail['email'] = tenant.email

        rental_infos = RentalInfo.objects.filter(tenant=tenant)

        rent_data_list = []
        if rental_infos:
            for rent in rental_infos:
                rent_data = {}
                rent_data[REQUEST_RENTAL_ID] = rent.id
                rent_data[REQUEST_CONTRACT_ID] = rent.contract_id
                room_list = TenantRental.objects.filter(rental = rent)
                room_data = []
                for room in room_list:
                    room_data.append(room.house.roomNumber)
                room_data.sort()
                rent_data['room_data'] = room_data
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
                rent_data_list.append(rent_data)

        user_level_rental_detail[REQUEST_RENT_DATA] = rent_data_list
        tenant_detail.append(user_level_rental_detail)
        return UTF8JsonResponse({'errno': 1001, 'msg': '查询客户成功', 'data': tenant_detail})

@csrf_exempt
def view_tenant(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 100001, 'msg': '请求格式有误'})

    page = request.POST.get('page')
    num = request.POST.get('num')
    page = int(page)
    num = int(num)
    left = (page - 1) * num
    right = page * num
    total = Tenant.objects.all().count()
    tenants = Tenant.objects.all()[left:right]

    tenant_detail = []
    for tenant in tenants:
        user_level_rental_detail = {}
        user_level_rental_detail[REQUEST_USER_ID] = tenant.id
        user_level_rental_detail[REQUEST_USERNAME] = tenant.contactName
        user_level_rental_detail[REQUEST_LEGAL_NAME] = tenant.real_name
        user_level_rental_detail[REQUEST_COM_NAME] = tenant.company
        user_level_rental_detail[REQUEST_PHONE] = tenant.contactNumber
        user_level_rental_detail['email'] = tenant.email

        rental_infos = RentalInfo.objects.filter(tenant=tenant).order_by('contract_id')
        rent_data_list = []
        for rent in rental_infos:
            rent_data = {}
            rent_data[REQUEST_RENTAL_ID] = rent.id
            rent_data[REQUEST_CONTRACT_ID] = rent.contract_id
            room_list = TenantRental.objects.filter(rental = rent)
            room_data = []
            for room in room_list:
                room_data.append(room.house.roomNumber)
            room_data.sort()
            rent_data['room_data'] = room_data
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
            rent_data_list.append(rent_data)

        user_level_rental_detail[REQUEST_RENT_DATA] = rent_data_list

        payment_infos = Payment.objects.filter(tenant=tenant).order_by('rentalInfo__contract_id', 'start_time')
        property_fees_list = []
        for pay in payment_infos:
            pay_data = {}
            pay_data['contract_id'] = pay.rentalInfo.contract_id
            pay_data['payment_id'] = pay.id
            pay_data['year'] = pay.period
            pay_data['is_paid'] = pay.is_paid
            if pay.paymentTime:
                pay_data['date_pay'] = pay.paymentTime.strftime("%Y-%m-%d")
            property_fees_list.append(pay_data)
        user_level_rental_detail['property_fees_data'] = property_fees_list

        tenant_detail.append(user_level_rental_detail)

    return UTF8JsonResponse({'errno': 1001, 'msg': '返回客户列表成功', 'data': tenant_detail, 'total': total})
