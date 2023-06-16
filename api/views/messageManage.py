import json

from django.http import HttpResponse

from api.models import Tenant


def add_tenant(request):
    if request.method == 'POST':
        # 从请求中获取客户信息
        data = json.loads(request.body)
        real_name = data['real_name']
        company = data['company']
        contactName = data['contactName']
        contactNumber = data['contactNumber']
        # 创建新的客户对象并保存到数据库中
        tenant = Tenant(real_name=real_name, company=company,
                        contactName=contactName,
                        contactNumber=contactNumber)
        tenant.save()

        # 返回成功信息
        return HttpResponse('Tenant added successfully!')
    else:
        return HttpResponse('Tenant added failed!')


def delete_tenant(request, tenant_id):
    # 根据客户id获取客户对象
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.delete()
    return HttpResponse('Tenant deleted successfully!')


def update_tenant(request, tenant_id):
    if request.method == 'POST':
        # 根据客户id获取客户对象
        tenant = Tenant.objects.get(id=tenant_id)
        data = json.loads(request.body)
        # 更新客户信息
        tenant.real_name = data['real_name']
        tenant.company = data['company']
        tenant.contactName = data['contactName']
        tenant.contactNumber = data['contactNumber']

        # 保存客户对象到数据库中
        tenant.save()

        # 返回成功信息
        return HttpResponse('tenant updated successfully!')


def view_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    return tenant
