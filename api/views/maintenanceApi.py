from datetime import timedelta
from datetime import datetime,timedelta
import time
import jieba
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
from api.keywords import water_keywords,electric_keyword,mechanical_keyword,stopwords

def auto_assign(text):
    tokens = jieba.cut(text)  # 使用jieba分词器对文本进行分词
    #filtered_tokens = [token for token in tokens if token not in stopwords]

    data={}
    data['1'] = 0
    data['2'] = 0
    data['3'] = 0

    for token in tokens:
        if token not in stopwords:
            if token in water_keywords:
                data['1'] += 1
            if token in electric_keyword:
                data['2'] += 1
            if token in mechanical_keyword:
                data['3'] += 1

    type_list = sorted(data.items(),  key=lambda x: x[1], reverse=True)
    print(type_list)



@csrf_exempt
def create_request(request):
    if request.method == 'POST':
        #问题描述、报修时间、报修房间号、报修公司、报修联系人姓名和联系方式
        title = request.POST.get('title')
        description = request.POST.get('description')
        time = request.POST.get('time')
        room = request.POST.get('room')
        company = request.POST.get('company')
        user_id = request.POST.get('user_id')
        contact_user = request.POST.get('contact_name')
        contact_number = request.POST.get('contact_number')
        expect_date = request.POST.get('expect_date')
        expect_timeslot = request.POST.get('expect_timeslot')
        repair_type = request.POST.get('type')

        house = House.objects.filter(roomNumber=room).first()
        if house is None:
            return UTF8JsonResponse({'errno':7001, 'msg': '房间不存在'})
        submitter = CustomUser.objects.filter(id=user_id).first()

        #智能派单
        if repair_type is None:
            repair_type = auto_assign(description)
        
        #筛选出类型匹配的维修人员
        staff_list = CustomUser.objects.filter(position='2',m_type__startswith='1')

        #第一轮先查看有没有完全一致的排班时间
        #第一轮没有的话就从当前开始往后看，直到有一个符合的（前面没有也一定会遇到后面最早可以的时间）
        assign = False
        accurate = 1
        next_date = expect_date
        next_slot = expect_timeslot
        while not assign:
            for staff in staff_list:
                #每个员工查看他的空档，如果有空档直接派单,检查存不存在这个时间，存在就代表没空
                unavailable_timeslot = Timeslot.objects.filter(staff=staff,date=next_date,slot=next_slot).first()
                if unavailable_timeslot is None:
                    assign_timeslot = Timeslot(date=next_date,slot=next_slot,staff=staff,type=2)
                    assign = True
                    break
            
            accurate += 1
            date.strftime("%Y-%m-%d")+ datetime.timedelta(days=i)

        
        #for staff in staff_list:
        #print(staff_list)
        #print(type(free_staff_list))
        #available_staff_list = None

        repair = Repair(title=title,description=description,house=house,createdTime=time,
                        submitter=submitter,company=company,contactName=contact_user,
                        contactNumber=contact_number,expect_date=expect_date,
                        expect_time_slot=expect_timeslot,type=repair_type)
        
        #repair.save()

    

        data = model_to_dict(repair)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加报修信息','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def del_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        record = Repair.objects.filter(id=request_id).first()
        if record.status == 'In Progress':
            time_slot = record.time_slot
            time_slot.delete()

        record.delete()

        return UTF8JsonResponse({'errno':1001, 'msg':   '成功删除报修记录'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})  
     
@csrf_exempt
def update_request(request):
    if request.method == 'POST':
        info = request.POST.dict()
        request_id = info.get('request_id')
        title = info.get('title')
        description = info.get('description')
        created_time = info.get('submitTime')
        room = info.get('room')
        company = info.get('company')
        contact_name = info.get('submitterName')
        contact_number = info.get('submitterContact')
        #staff_id = info.get('assignStaffId')
        staff_contact = info.get('staffContact')
        manager_id = info.get('managerIncharge')
        #repairing_time = info.get('estimateRepairTimeSlot')
        status = info.get('status')
        plan = info.get('plan')
        complete_time = info.get('complete_time')
        solver_id = info.get('solverStaffId')
        expect_date = info.get('expect_date')
        expect_timeslot = info.get('expect_timeslot')   

        record = Repair.objects.filter(id=request_id).first()
        if title:
            record.title = title
        if description:
            record.description = description
        if created_time:    
            record.createdTime = created_time
        if room:
            house = House.objects.filter(roomNumber=room).first()
            record.house=house
        if company:
            record.company = company
        if contact_name:
            record.contactName = contact_name
        if contact_number:
            record.contactNumber = contact_number
        # if staff_id:
        #     staff=CustomUser.objects.filter(id=staff_id).first()
        #   record.staff=staff
        if staff_contact:
            record.staffContact = staff_contact
        if manager_id:
            manager = CustomUser.objects.filter(id=manager_id).first()
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
            solver = CustomUser.objects.filter(id= solver_id).first()
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
            if record.time_slot:
                data['repairing_date'] = record.time_slot.date.strftime("%Y-%m-%d")
                data['repairing_slot'] = record.time_slot.slot
            if record.completeTime:
                data['completeTime'] = record.completeTime.strftime("%Y-%m-%d %H:%M:%S")
            if record.expect_date:
                data['expect_date'] = record.expect_date.strftime("%Y-%m-%d")
            data['expect_timeslot'] = record.expect_time_slot

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
        

        repair_exist = Repair.objects.filter(id=request_id).first()
        staff = CustomUser.objects.filter(id=staff_id).first()

        if repair_exist.time_slot is not None:
            ori_timeslot = repair_exist.time_slot
            ori_timeslot.delete()

        #由管理员分派，type=1
        time_slot = Timeslot(staff=staff,date=repair_date,slot=repair_slot,type='1',repair_info=repair_exist)
        time_slot.save()

        repair_exist.staff = staff
        repair_exist.time_slot = time_slot
        repair_exist.staffContact = staff.contactNumber
        repair_exist.status = 'In Progress'
        repair_exist.save()

        data = model_to_dict(repair_exist)        
        #
        # staff.m_status=0
        # staff.save()


        return UTF8JsonResponse({'errno':1001, 'msg': '成功分派任务/修改上门时段','data':data})
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
    return_data = []
    str_date = ""
    for staff in staff_list:
        data={}
        data['id'] = staff.id
        data['name'] = staff.realname
        data['type'] = staff.m_type
        for i in range(1,(int(period)*3 + 1)):
            str_date = "time" + str(i)
            data[str_date] = '0'
            
        print("here")
        for j in range(int(period)):
            search_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=j)
            search_date = search_date.strftime("%Y-%m-%d")
            timeslot_list_accurate = timeslot_list.filter(date__startswith=search_date).order_by('slot')

            for timeslot in timeslot_list_accurate:
                if timeslot.staff == staff:
                    str_date = "time" + str(3 * int(j) + int(timeslot.slot))
                    print(timeslot.staff.realname + " - str_date:" + str_date)
                    data[str_date] = timeslot.type

        return_data.append(data)

    return return_response(1001, '返回排班信息',return_data)

    


    

