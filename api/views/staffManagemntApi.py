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

 #包括各个人姓名、电话、岗位。对于维修人员需要给出类型（水、电、机械）、是否可用状态。
 # listInfo - 0=管理人员 ,1=维修人员
 # managerManage : POST,PUT,DEL
 # servicemanManage : POST,PUT,DEL
 # searchStaff


@csrf_exempt
def createStaff(request):
    # userId=request.session.get('uid')
    # if userId is None:
    #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
    # user = CustomUser.objects.filter(id=userId).first()
    
    if request.method == 'POST':  #创建 - 只有超级管理员，创建后添加user
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
            NewMaintenance = CustomUser(username=username,realname=name,position=position,contactNumber=contact,m_type=type,m_status='1')
            NewMaintenance.set_password("wenhuashamo123.")
            NewMaintenance.save()
        
        else:
            # if(user.position != '4'):
            #     return UTF8JsonResponse({'errno': 3001, 'msg': '无权限添加人员'})
            NewManager = CustomUser(username=username,realname=name,position=position,contactNumber=contact)
            NewManager.set_password("wenhuashamo123.")
            NewManager.save()

        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加人员'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})
    
@csrf_exempt
def updateStaff(request):
    # userId=request.session.get('uid')
    # if userId is None:
    #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
    # user = CustomUser.objects.filter(id=userId).first()

    
    if request.method == 'POST':
        info = request.POST.dict()
        userId = info.get('staffId')
        name = info.get('name') 
        contact = info.get('contact')
        position = info.get('position')
        type = info.get('type')
        status = info.get('status')

        # if position and position == '2':
        #     if(user.position != '4' and user.position != '3'):
        #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'}) 
        # elif position:
        #     if(user.position != '4'):
        #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'})
        

        user = CustomUser.objects.filter(id=userId).first()
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
                    user.m_type = '0'
                    user.m_status = '1'
                user.position = position
                
            if type:
                user.m_type = type
            if status:
                user.m_status = status
            user.save()
        except Exception as e:
            return UTF8JsonResponse({'errno': 3004, 'msg': '数据库存储错误'+str(e.args)})
        return UTF8JsonResponse({'errno': 1001, 'msg': '修改信息成功'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})
    
@csrf_exempt
def deleteStaff(request):
    # userId=request.session.get('uid')
    # if userId is None:
    #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
    # user = CustomUser.objects.filter(id=userId).first()

    if request.method == 'POST':
        staffId = request.POST.get('staffId')
        staff = CustomUser.objects.filter(id=staffId).first()
        

        # if staff.position == '2':
        #     if(user.position != '4' and user.position != '3'):
        #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'}) 
        # elif:
        #     if(user.position != '4'):
        #         return UTF8JsonResponse({'errno': 3001, 'msg': '无权限修改信息'})
        

        staff.delete()
        return UTF8JsonResponse({'errno':1001, 'msg': '删除人员成功'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def getStaff(request):
    if request.method == 'GET':
        userId = request.GET.get('staffId','')
        if userId:
            staff = CustomUser.objects.filter(id=userId).first()
            staffData = {}
            staffData['id']=staff.id
            staffData['name']=staff.realname
            staffData['contact'] = staff.contactNumber
            staffData['position']=staff.position
            staffData['type'] = staff.m_type
            staffData['status'] = staff.m_status
            return UTF8JsonResponse({'errno':1001, 'msg': '返回员工信息成功', 'data': staffData})

        staffList = CustomUser.objects.filter(Q(position='2') | Q(position='3') | Q(position='4')).order_by('-position')
        #ordered = sorted(staffList, key=operator.attrgetter('position'),reverse=False)

        staffListData=[]
        for staff in staffList:
            staffData={}
            staffData['id']=staff.id
            staffData['name']=staff.realname
            staffData['contact'] = staff.contactNumber
            staffData['position']=staff.position
            staffData['type'] = staff.m_type
            staffData['status'] = staff.m_status

            staffListData.append(staffData)

            
        return UTF8JsonResponse({'errno':1001, 'msg': '返回员工列表成功', 'data': staffListData})

