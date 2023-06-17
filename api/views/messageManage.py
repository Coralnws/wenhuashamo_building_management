import json

from django.http import HttpResponse

from api.models import Tenant


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
        return HttpResponse('Tenant added successfully!')
    else:
        return HttpResponse('Tenant added failed!')


def delete_tenant(request):
    # 根据客户id获取客户对象
    company = request.GET.get('company')
    tenant = Tenant.objects.get(company=company)
    tenant.delete()
    return HttpResponse('Tenant deleted successfully!')


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
        return HttpResponse('tenant updated successfully!')


def view_tenant(request):
    company = request.GET.get('company')
    tenant = Tenant.objects.get(company=company)
    return tenant
