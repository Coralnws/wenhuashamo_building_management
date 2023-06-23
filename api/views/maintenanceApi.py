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
from api.utils import *
from api.error_utils import *

'''
派发维修任务
更新维修工单的最终状态
提交报修信息
发送提醒？
 
1.createRequest (报修工单包括：问题描述、报修时间、报修房间号、报修公司、报修联系人姓名和联系方式)
2.assignTask (对客户工单给出初步反馈意见（包括什么时间、谁负责维修，以及维修人联系电话)
3.closeTask 维修工单的最终状态，包括：问题解决办法，解决时间，解决人 + 维修人员状态更新为可用
4.udpateRequest
5.delRequest
6.getRequest
7.getTimeslot
8.changeTimeslot
'''

@csrf_exempt
def create_request(request):
    if request.method == 'POST':
        #问题描述、报修时间、报修房间号、报修公司、报修联系人姓名和联系方式
        description = request.POST.get('description')
        time = request.POST.get('time')
        room = request.POST.get('room')
        company = request.POST.get('company')
        user_id = request.POST.get('user_id')
        contact_user = request.POST.get('contact_name')
        contact_number = request.POST.get('contact_number')
        expect_date = request.POST.get('expect_date')
        expect_timeslot = request.POST.get('expect_timeslot')

        house = House.objects.filter(roomNumber=room).first()
        if house is None:
            return UTF8JsonResponse({'errno':7001, 'msg': '房间不存在'})
        submitter = CustomUser.objects.filter(id=user_id).first()

        repair = Repair(description=description,house=house,createdTime=time,
                        submitter=submitter,company=company,contactName=contact_user,
                        contactNumber=contact_number,expect_date=expect_date,
                        expect_time_slot=expect_timeslot)
        
        repair.save()
        data = model_to_dict(repair)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加报修信息','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def del_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        record = Repair.objects.filter(id=request_id).first()
        record.delete()

        return UTF8JsonResponse({'errno':1001, 'msg':   '成功删除报修记录'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})  
     
@csrf_exempt
def update_request(request):
    if request.method == 'POST':
        info = request.POST.dict()
        request_id = info.get('request_id')
        description = info.get('description')
        created_time = info.get('submitTime')
        room = info.get('room')
        company = info.get('company')
        contact_name = info.get('submitterName')
        contact_number = info.get('submitterContact')
        staff_id = info.get('assignStaffId')
        staff_contact = info.get('staffContact')
        manager_id = info.get('managerIncharge')
        #repairing_time = info.get('estimateRepairTimeSlot')
        status = info.get('status')
        plan = info.get('plan')
        complete_time = info.get('complete_time')
        solver_id = info.get('solverStaffId')
        expect_date = info.get('expect_date')
        expect_timeslot = info.get('expect_timeslot')   

        print(request_id)
        record = Repair.objects.filter(id=request_id).first()
        if description:
            print("here")
            record.description = description
        if created_time:    
            record.createdTime = created_time
        if room:
            house = House.objects.filter(roomNumber=room)
            record.house=house
        if company:
            record.company = company
        if contact_name:
            record.contactName = contact_name
        if contact_number:
            record.contactNumber = contact_number
        if staff_id:
            staff=CustomUser.objects.filter(id=staff_id)
            record.staff=staff
        if staff_contact:
            record.staffContact = staff_contact
        if manager_id:
            manager = CustomUser.objects.filter(id=manager_id)
            record.manager = manager
        # if repairing_time:
        #     record.repairingTime = repairing_time
        if status:
            record.status = status
        if plan:
            record.plan = plan
        if complete_time:
            record.complete_time = complete_time
        if solver_id:
            solver = CustomUser.objects.filter(id= solver_id)
            record.solver = solver
        if expect_date:
            record.expect_date = expect_date
        if expect_timeslot:
            record.expect_time_slot = expect_timeslot

        record.save()

        data = model_to_dict(record)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改报修记录','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def get_request(request):
    if request.method == 'GET':
        status = request.GET.get('status','')
        user_id = request.GET.get('user_id','')
    
        request_list = None
        
        filter = Q()
    
        if status:
            filter &= Q(status=status)
        if user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            
            if user.position == '2':
                filter &= Q(staff=user)
            elif user.position == '1':
                filter &= Q(submitter=user)
                if user.tenant:
                    company = user.tenant.company
                    filter &= Q(company=company)        

        request_list = Repair.objects.filter(filter).order_by('createdTime')
    
        request_data=[]

        for record in request_list:
            
            
            data=model_to_dict(record)
            data['house'] = record.house.roomNumber

            if record.manager:
                data['manager'] = record.manager.realname
            if record.staff:
                data['repair_staff'] = record.staff.realname
                data['staff_contact'] = record.staff.contactNumber
            if record.solver:
                data['solver'] = record.solver.realname

            data['createdTime'] = record.createdTime.strftime("%Y-%m-%d %H:%M:%S")
            if record.repairingTime:
                data['repairingTime'] = record.repairingTime.strftime("%Y-%m-%d %H:%M:%S")
            if record.completeTime:
                data['completeTime'] = record.completeTime.strftime("%Y-%m-%d %H:%M:%S")
            if record.expect_date:
                data['expect_date'] = record.expect_date.strftime("%Y-%m-%d")
            if record.expect_time_start:   
                data['expect_time_start'] = record.expect_time_start.strftime("%H:%M:%S")
            if record.expect_time_start:   
                data['expect_time_end'] = record.expect_time_end.strftime("%H:%M:%S")

            
            request_data.append(data)
        
        return UTF8JsonResponse({'errno':1001, 'msg': '成功获取报修列表','data':request_data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def assign_task(request):
    #对客户工单给出初步反馈意见（包括什么时间、谁负责维修，以及维修人联系电话）
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        staff_id =  request.POST.get('staff_id')
        repair_date = request.POST.get('repair_date')
        repair_slot = request.POST.get('repair_slot')
        staff_contact = request.POST.get('staff_contact')

        repair_exist = Repair.objects.filter(id=request_id).first()
        staff = CustomUser.objects.filter(id=staff_id).first()

        #由管理员分派，type=1
        time_slot = Timeslot(staff=staff,date=repair_date,slot=repair_slot,type='1',repair_info=repair_exist)
        time_slot.save()

        repair_exist.staff = staff
        repair_exist.time_slot = time_slot
        repair_exist.staffContact = staff_contact
        repair_exist.status = 'In Progress'
        repair_exist.save()

        data = model_to_dict(repair_exist)
        
        #
        staff.m_status=0
        staff.save()


        return UTF8JsonResponse({'errno':1001, 'msg': '成功分派任务','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def close_task(request):
    #维修工单的最终状态，包括：问题解决办法，解决时间，解决人 + 维修人员状态更新为可用
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        plan = request.POST.get('plan')
        complete_time = request.POST.get('complete_time')
        solver_id = request.POST.get('solver_id')
        #solver = request.POST.get('solver_username')

        repair_exist = Repair.objects.filter(id=request_id).first()
        solver = CustomUser.objects.filter(id=solver_id).first()
        #solver = CustomUser.objects.filter(username=solver).first()

        repair_exist.plan = plan
        repair_exist.completeTime = complete_time
        repair_exist.solver = solver
        repair_exist.status = 'Complete'

        staff = repair_exist.staff
        staff.m_status = 1
        staff.save()

        repair_exist.save()
        data = model_to_dict(repair_exist)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功结束报修任务','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})


@csrf_exempt
def get_timeslot(request):
    if request.method != GETMETHOD:
        return not_get_method()
    
    start_date = request.GET.get('start_date','')
    period = request.GET.get('period','')
    
    staff_id = request.GET.get('staff_id','')

    filter = Q()
    staff_filter = Q(position='2')
    if staff_id:
        staff = CustomUser.objects.filter(id=staff_id).first()
        filter &= Q(staff=staff)
        staff_filter &= Q(id=staff_id)
    if period == '1':
        filter &= Q(date=start_date)
    else:
        filter &= Q(date__gte=start_date)

    
    timeslot_list = Timeslot.objects.filter(filter).order_by('date')
    staff_list = CustomUser.objects.filter(staff_filter).order_by('realname')
    return_data = {}

    for staff in staff_list:
        return_data[staff.realname] = {}
    
    for i in range(int(period)):
        search_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=i)
        search_date = search_date.strftime("%Y-%m-%d")
        timeslot_list_accurate = timeslot_list.filter(date__startswith=search_date).order_by('slot')
        print(len(timeslot_list_accurate))
        for timeslot in timeslot_list_accurate:
            if return_data[staff.realname].get(search_date) is None:
                return_data[staff.realname][search_date] = []
            return_data[staff.realname][search_date].append(timeslot.slot)


    return return_response(1001, '返回排班信息',return_data)

    

        

# + datetime.timedelta(days=1)).strftime("%Y-%m-%d)