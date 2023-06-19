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
def create_staff(request):
    # user_id=request.session.get('uid')
    # if user_id is None:
    #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
    # user = CustomUser.objects.filter(id=user_id).first()
    
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
        if username_exist < realname_exist:
            if username_exist != 0:
                username  = username+"_" + str(realname_exist)
    #创建账号
    
    if position == '2':
        # if(user.position != '4' and user.position != '3'):
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '无权限添加维修人员'})
        type = request.POST.get('type')
        new_maintenance = CustomUser(username=username,realname=name,position=position,contactNumber=contact,m_type=type,m_status='1')
        new_maintenance.set_password(DEFAULTPASS)
        new_maintenance.save()
    
    else:
        # if(user.position != '4'):
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '无权限添加人员'})
        new_manager = CustomUser(username=username,realname=name,position=position,contactNumber=contact)
        new_manager.set_password(DEFAULTPASS)
        new_manager.save()

    return return_response(1001,'成功添加人员')


@csrf_exempt
def update_staff(request):
    # user_id=request.session.get('uid')
    # if user_id is None:
    #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
    # user = CustomUser.objects.filter(id=user_id).first()

    if requset.method != 'POST':
        return not_post_method()

    info = request.POST.dict()
    user_id = info.get('staffId')
    name = info.get('name') 
    contact = info.get('contact')
    position = info.get('position')
    types = info.get('type')
    status = info.get('status')

    # if position and position == '2':
    #     if(user.position != '4' and user.position != '3'):
    #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'}) 
    # elif position:
    #     if(user.position != '4'):
    #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'})

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
                if username_exist < realname_exist:
                    if username_exist != 0:
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

    # user = get_user_from_redis(request.POST.get('session_id'))
    # if user is None:
    #     return not_login()

    staff_id = request.POST.get('staffId')
    staff = CustomUser.objects.filter(id=staff_id).first()

    # if staff.position == '2':
    #     if(user.position != '4' and user.position != '3'):
    #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'}) 
    # elif:
    #     if(user.position != '4'):
    #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'})

    staff.delete()

    return return_response(1001, '删除人员成功')


@csrf_exempt
def get_staff(request):
    if request.method != 'GET':
        return not_get_method()

    # check user from redis 
    # user = get_user_from_redis(request.POST.get('session_id'))
    # if user is None:
    #     return not_login()

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
    
    if position and types and search is None:
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
            staff_data['status'] = staff.m_status

        staff_list_data.append(staff_data)

    return return_response(1001, '返回员工列表成功', staff_list_data)


def get_staff_filters(position = None, status = None, types = None, search = None):
    filters = Q()
    if position:
        filters &= Q(position=position)
        #staff_list = CustomUser.objects.filter(position=position)
    if status:
        filters &= Q(m_status=status)
    if type:
        filters &= Q(m_type=types)
    if search:
        filters &= Q(realname__icontains=search) | Q(contactNumber__icontains=search)
    return filters
