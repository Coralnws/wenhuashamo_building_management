from datetime import timedelta
from datetime import datetime
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from django.forms.models import model_to_dict
from django.db.models import Q
import operator
from api.utils import *
from api.error_utils import *

 #包括各个人姓名、电话、岗位。对于维修人员需要给出类型（水、电、机械）、是否可用状态。
 # listInfo - 0=管理人员 ,1=维修人员
 # managerManage : POST,PUT,DEL
 # servicemanManage : POST,PUT,DEL
 # searchStaff

@csrf_exempt
def create_user(request):
    if request.method != 'POST':  #创建 - 只有超级管理员，创建后添加user
        return not_post_method()

    tenant_id = request.POST.get('tenant_id')
    company = request.POST.get('company')
    name = request.POST.get('realname')
    contact = request.POST.get('contact')
    
    if tenant_id:
        tenant = Tenant.objects.filter(id=tenant_id).first()
    elif company:
        tenant = Tenant.objects.filter(company=company).first()
    realname_exist = CustomUser.objects.filter(realname=name).count()
    username_exist = CustomUser.objects.filter(username=name).count()
    username = name
    if realname_exist > 0 or username_exist:
        if realname_exist == username_exist:
            username  = username+"_"+str(realname_exist)
        if username_exist < realname_exist and username_exist != 0:
            username  = username+"_" + str(realname_exist)
    
    new_user = CustomUser(tenant=tenant,username=username,realname=name,position='1',contactNumber=contact)
    new_user.set_password(DEFAULTPASS)
    new_user.save()

    return return_response(1001,'成功添加用户')

@csrf_exempt
def create_staff(request):
    if request.method != 'POST':  #创建 - 只有超级管理员，创建后添加user
        return not_post_method()

    name = request.POST.get('name')
    contact = request.POST.get('contact')
    position = request.POST.get('position')  # 3 or 4
    #检查重名
    
    realname_exist = CustomUser.objects.filter(realname=name).count()
    username_exist = CustomUser.objects.filter(username=name).count()
    username = name
    if realname_exist > 0 or username_exist:
        if realname_exist == username_exist:
            username  = username+"_"+str(realname_exist)
        if username_exist < realname_exist and username_exist != 0:
            username  = username+"_" + str(realname_exist)
    #创建账号
    
    if position == '2':
        # check for superadmin or admin for permission
        type = request.POST.get('type')
        new_maintenance = CustomUser(username=username,realname=name,position=position,contactNumber=contact,m_type=type,m_status='1')
        new_maintenance.set_password(DEFAULTPASS)
        new_maintenance.save()
    
    else:
        # check for superadmin for permission
        new_manager = CustomUser(username=username,realname=name,position=position,contactNumber=contact)
        new_manager.set_password(DEFAULTPASS)
        new_manager.save()

    return return_response(1001,'成功添加人员')


@csrf_exempt
def update_staff(request):

    if request.method != 'POST':
        return not_post_method()

    info = request.POST.dict()
    user_id = info.get('staffId')
    name = info.get('name') 
    contact = info.get('contact')
    position = info.get('position')
    types = info.get('type')
    status = info.get('status')

    # only superadmin able to edit normal user info
    # admin and super admin can edit maintainer info

    user = CustomUser.objects.filter(id=user_id).first()
    if user is None:
        return UTF8JsonResponse({'errno': 3001, 'msg': '用户不存在'})
    try:
        if name:
            user.realname=name
            realname_exist = CustomUser.objects.filter(realname=name).count()
            username_exist = CustomUser.objects.filter(username=name).count()
            username = name
            if realname_exist > 0 or username_exist:
                if realname_exist == username_exist:
                    username  = username+"_"+str(realname_exist)
                if username_exist < realname_exist and username_exist != 0:
                    username  = username+"_"+str(realname_exist)
            user.username = username
        if contact:
            user.contactNumber = contact
        if position:
            if user.position == '2'and position != '2':
                user.m_type = '-'
                user.m_status = '-'
            user.position = position
            
        if types:
            user.m_type = types
        if status:
            user.m_status = status
        user.save()
    except Exception as e:
        return default_error(e)
    return return_response(1001,'修改信息成功')


@csrf_exempt
def delete_staff(request):
    if request.method != 'POST':
        return not_post_method()

    staff_id = request.POST.get('staffId')
    staff = CustomUser.objects.filter(id=staff_id).first()

    # only superadmin able to delete normal user info
    # admin and super admin can delete maintainer info

    staff.delete()

    return return_response(1001, '删除人员成功')


@csrf_exempt
def get_staff(request):
    if request.method != 'GET':
        return not_get_method()

    user_id = request.GET.get('staffId','')
    position = request.GET.get('position','')
    search = request.GET.get('search','') #名字和电话
    types = request.GET.get('type','')
    status = request.GET.get('status','')

    if user_id:
        staff = CustomUser.objects.filter(id=user_id).first()
        staff_data = {}
        staff_data['id']=str(staff.id)
        staff_data['name']=staff.realname
        staff_data['contact'] = staff.contactNumber
        staff_data['position']=staff.position
        staff_data['type'] = staff.m_type
        staff_data['status'] = staff.m_status

        return return_response(1001, '返回员工信息成功', staff_data)

    staff_list = None

    filters = get_staff_filters(position, status, types, search)

    staff_list = CustomUser.objects.filter(filters).order_by('-position')
    
    if len(position) == 0 and len(types) == 0 and len(search) == 0 and len(status) == 0:
        staff_list = CustomUser.objects.filter(Q(position='2') | Q(position='3') | Q(position='4')).order_by('-position')
    else:
        staff_list = CustomUser.objects.filter(filters).order_by('-position')
    
    staff_list_data=[]
    for staff in staff_list:
        staff_data={}
        staff_data['id']=staff.id
        staff_data['name']=staff.realname
        staff_data['contact'] = staff.contactNumber
        staff_data['position']=staff.position
        if staff.position != '2':
            staff_data['type'] = '-'
            staff_data['status'] = '-'
        else:
            staff_data['type'] = staff.m_type
            working = False
            timeslot_list = Timeslot.objects.filter(staff=staff)
            for time_slot in timeslot_list:
                #print(timezone.now().strftime("%Y-%m-%d"))
                if time_slot.date.strftime("%Y-%m-%d") == timezone.now().strftime("%Y-%m-%d"):
                    #print("working is true")
                    working = True
            if working:
                staff_data['status'] = '0'
            else:
                staff_data['status'] = '1'

        staff_list_data.append(staff_data)

    return return_response(1001, '返回员工列表成功', staff_list_data)


def get_staff_filters(position = None, status = None, types = None, search = None):
    filters = Q()
    if position:
        filters &= Q(position=position)
    if status:
        filters &= Q(m_status=status)
    if types:
        filters &= Q(m_type=types)
    if search:
        filters &= Q(realname__icontains=search) | Q(contactNumber__icontains=search)
    return filters

