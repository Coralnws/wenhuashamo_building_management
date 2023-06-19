from datetime import timedelta
from datetime import datetime,timedelta
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

'''
派发维修任务
更新维修工单的最终状态
提交报修信息
发送提醒？

1.createRequest (报修工单包括：问题描述、报修时间、报修房间号、报修公司、报修联系人姓名和联系方式)
2.assignTask (对客户工单给出初步反馈意见（包括什么时间、谁负责维修，以及维修人联系电话） )
3.updateStatus 更新维修人员状态
4.closeTask 维修工单的最终状态，包括：问题解决办法，解决时间，解决人 + 维修人员状态更新为可用
5.buildLib 添加知识库记录?
6.alterRequest
7.delRequest
8.getRequest
'''

@csrf_exempt
def createRequest(request):
    if request.method == 'POST':
        #问题描述、报修时间、报修房间号、报修公司、报修联系人姓名和联系方式
        description = request.POST.get('description')
        time = request.POST.get('time')
        room = request.POST.get('room')
        company = request.POST.get('company')
        user_id = request.POST.get('user_id')
        contact_user = request.POST.get('contact_name')
        contact_number = request.POST.get('contact_number')

        house = House.objects.filter(roomNumber=room).first()
        submitter = CustomUser.objects.filter(id=user_id).first()

        repair = Repair(description=description,house=house,createdTime=time,
                        submitter=submitter,company=company,contactName=contact_user,contactNumber=contact_number)
        
        repair.save()
        data = model_to_dict(repair)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加报修信息','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def delRequest(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        record = Repair.objects.filter(id=request_id).first()
        record.delete()

        return UTF8JsonResponse({'errno':1001, 'msg':   '成功删除报修记录'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})  
     
@csrf_exempt
def updateRequest(request):
    if request.method == 'POST':
        info = request.POST.dict()
        request_id = info.get('request_id')
        description = info.get('description')
        createdTime = info.get('submitTime')
        room = info.get('room')
        company = info.get('company')
        contactName = info.get('submitterName')
        contactNumber = info.get('submitterContact')
        staffId = info.get('assignStaffId')
        staffContact = info.get('staffContact')
        managerId = info.get('managerIncharge')
        repairingTime = info.get('estimateRepairTime')
        status = info.get('status')
        plan = info.get('plan')
        complete_time = info.get('complete_time')
        solver_id = info.get('solverStaffId')        

        print(request_id)
        record = Repair.objects.filter(id=request_id).first()
        if description:
            print("here")
            record.description = description
        if createdTime:    
            record.createdTime = createdTime
        if room:
            house = House.objects.filter(roomNumber=room)
            record.house=house
        if company:
            record.company = company
        if contactName:
            record.contactName = contactName
        if contactNumber:
            record.contactNumber = contactNumber
        if staffId:
            staff=CustomUser.objects.filter(id=staffId)
            record.staff=staff
        if staffContact:
            record.staffContact = staffContact
        if managerId:
            manager = CustomUser.objects.filter(id=managerId)
            record.manager = manager
        if repairingTime:
            record.repairingTime = repairingTime
        if status:
            record.status = status
        if plan:
            print("has plan")
            record.plan = plan
        if complete_time:
            record.complete_time = complete_time
        if solver_id:
            solver = CustomUser.objects.filter(id= solver_id)
            record.solver = solver

        record.save()

        data = model_to_dict(record)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改报修记录','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def getRequest(request):
    if request.method == 'GET':
        status = request.GET.get('status','')
        user_id = request.GET.get('user_id','')

        request_list = None
        
        filter = Q()

        if status:
            filter &= Q(status=status)
        if user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            filter &= Q(submitter=user)
        

        request_list = Repair.objects.filter(filter).order_by('createdTime')
    
        requestData=[]

        for request in request_list:
            
            
            data=model_to_dict(request)
            data['house'] = request.house.roomNumber

            if request.manager:
                data['manager'] = request.manager.realname
            if request.staff:
                data['staff'] = request.staff.realname
            if request.solver:
                data['solver'] = request.staff.realname
            
            requestData.append(data)
        
        return UTF8JsonResponse({'errno':1001, 'msg': '成功获取报修列表','data':requestData})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def assignTask(request):
    #对客户工单给出初步反馈意见（包括什么时间、谁负责维修，以及维修人联系电话）
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        staff_id =  request.POST.get('staff_id')
        repair_time = request.POST.get('repair_time')
        staff_contact = request.POST.get('staff_contact')

        request = Repair.objects.filter(id=request_id).first()
        staff = CustomUser.objects.filter(id=staff_id).first()
        request.staff = staff
        request.repairingTime = repair_time
        request.staffContact = staff_contact
        request.status = 'In Progress'


        request.save()

        data = model_to_dict(request)
        staff.m_status=0
        staff.save()


        return UTF8JsonResponse({'errno':1001, 'msg': '成功分派任务','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def closeTask(request):
    #维修工单的最终状态，包括：问题解决办法，解决时间，解决人 + 维修人员状态更新为可用
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        plan = request.POST.get('plan')
        complete_time = request.POST.get('complete_time')
        solver_id = request.POST.get('solver_id')
        #solver = request.POST.get('solver_username')

        request = Repair.objects.filter(id=request_id).first()
        solver = CustomUser.objects.filter(id=solver_id).first()
        #solver = CustomUser.objects.filter(username=solver).first()

        request.plan = plan
        request.completeTime = complete_time
        request.solver = solver
        request.status = 'Complete'

        staff = request.staff
        staff.m_status = 1
        staff.save()

        request.save()
        data = model_to_dict(request)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功结束报修任务','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

'''
    description = models.CharField(max_length=200)
    createdTime = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    contactName = models.CharField(max_length=50)
    contactNumber = models.CharField(max_length=20)
    staff = models.ForeignKey(CustomUser, related_name="repair_staff",on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(CustomUser,related_name="repair_manager",  on_delete=models.CASCADE, null=True, blank=True)
    repairingTime = models.DateTimeField(null=True, blank=True)
    status_choices = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Open')
    plan = models.TextField(blank=True)
    complete_time = models.DateTimeField(null=True, blank=True)
    solver = models.ForeignKey(CustomUser, related_name="repair_solver", on_delete=models.CASCADE, null=True, blank=True)
'''




    