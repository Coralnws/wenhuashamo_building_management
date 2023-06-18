import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse

from api.models import Tenant
from api.utils import UTF8JsonResponse


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


def delete_tenant(request):
    if request.method == 'POST':
        company = request.GET.get('company')
        tenant = Tenant.objects.get(company=company)
        tenant.delete()
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant deleted successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


def update_tenant(request):
    if request.method == 'POST':
        company = request.GET.get('former_company')
        tenant = Tenant.objects.get(company=company)
        # 更新客户信息
        tenant.real_name = request.GET.get('real_name')
        tenant.company = request.GET.get('company')
        tenant.contactName = request.GET.get('contactName')
        tenant.contactNumber = request.GET.get('contactNumber')

        # 保存客户对象到数据库中
        tenant.save()

        # 返回成功信息
        return UTF8JsonResponse({'errno': 1001, 'msg': 'Tenant updated successfully!'})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})


def view_tenant(request):
    if request.method == 'POST':
        company = request.GET.get('company')
        tenant = Tenant.objects.get(company=company)
        res = model_to_dict(tenant)
        return UTF8JsonResponse({'errno': 1001, 'msg': '返回员工列表成功', 'data': res})
    else:
        return UTF8JsonResponse({'errno': 4001, 'msg': 'Request Method Error'})
