from datetime import datetime,timedelta
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
from api.keywords import water_keywords,electric_keyword,mechanical_keyword,stopwords,water_main_keywords,electric_main_keyword,mechanical_main_keyword,non_type_keywords

def auto_assign(text):

    data={}
    data['0'] = 0
    data['1'] = 0
    data['2'] = 0
    data['3'] = 0

    if any(item in text for item in non_type_keywords):
        return '0'

    for item in water_main_keywords:
        if item in text:
            data['1'] += 2
            print("水主关键词出现")
    for item in water_keywords:
        if item in text:
            data['1'] += 1
            print("水关键词出现")
    for item in electric_main_keyword:
        if item in text:
            data['2'] += 2
            print("电主关键词出现")
    for item in electric_keyword:
        if item in text:
            data['2'] += 1
            print("电关键词出现")
    for item in mechanical_main_keyword:
        if item in text:
            data['3'] += 3
            print("机械主关键词出现")
    for item in mechanical_keyword:
        if item in text:
            data['3'] += 1
            print("机械关键词出现")

    type_list = sorted(data.items(), key=lambda x: (-x[1], -ord(x[0][0])))
    print(type_list)

    return type_list[0][0]


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
        if repair_type is None or repair_type == '0':
            repair_type = auto_assign(title+description)
        
        repair = Repair(title=title,description=description,house=house,createdTime=time,
                        submitter=submitter,company=company,contactName=contact_user,
                        contactNumber=contact_number,expect_date=expect_date,
                        expect_time_slot=expect_timeslot,type=repair_type)

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
        if record.status == 'In Progress' and record.time_slot:
            time_slot = record.time_slot
            time_slot.delete()

        record.delete()
        
        return UTF8JsonResponse({'errno':1001, 'msg':   '成功删除报修记录'})
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


        repair_exist = Repair.objects.filter(id=request_id).first()
        solver = CustomUser.objects.filter(id=solver_id).first()


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
    repair_id = request.GET.get('repair_id','')
    staff_id = request.GET.get('staff_id','')

    repair_type = None

    if len(repair_id) > 0:
        repair = Repair.objects.filter(id=repair_id).first()
        repair_type = repair.type
        expect_date = repair.expect_date
        expect_timeslot = repair.expect_time_slot
    
    target_staff = []
    target_date = []
    target_slot = []


    if repair_type is not None and repair_type != '0':
        if repair_type == '1':
            staff_list = CustomUser.objects.filter(position='2',m_type__startswith='1').order_by('?')
        elif repair_type == '2':
            staff_list = CustomUser.objects.filter(position='2',m_type__regex=r'\w1\w').order_by('?')
        elif repair_type == '3':
            staff_list = CustomUser.objects.filter(position='2',m_type__endswith='1').order_by('?')
        

        expect_date = repair.expect_date

        interval = 0
        check_slot = [1,0,0,0]
        assign = 0
        search_date = expect_date
        search_slot = expect_timeslot
        forward = False
        stop_backward = False
        while assign < 2:  #循环天
        #从0开始，每一次拿expect日期往前-period和+period，然后查看同一slot有没有，没有的话就查其它slot
        #筛出那天的某一员工的timeslot 
            if forward and interval > 0:
                search_date = (expect_date - timedelta(days=interval)).strftime("%Y-%m-%d")
                if search_date <= timezone.now().strftime("%Y-%m-%d"):
                    if search_date < timezone.now().strftime("%Y-%m-%d"):
                        search_date = (expect_date + timedelta(days=interval)).strftime("%Y-%m-%d")
                        stop_backward = True
                    else:
                        stop_backward = True
                        if timezone.now().strftime("%H:%M:%S") < "09:00:00":
                            search_slot = '1'
                        elif timezone.now().strftime("%H:%M:%S") < "12:00:00":
                            search_slot = '2'
                        elif timezone.now().strftime("%H:%M:%S") < "15:00:00":
                            search_slot = '3'
                        else:
                            search_date = (expect_date + timedelta(days=interval)).strftime("%Y-%m-%d")
                            forward = not forward
                
                        stop_backward = True   
            elif not forward and interval > 0:
                print("forward and interval > 0")
                search_date = (expect_date + timedelta(days=interval)).strftime("%Y-%m-%d")
                interval += 1
            elif interval == 0:
                search_date = expect_date.strftime("%Y-%m-%d")
                interval += 1
            
            while True:  #一天内循环找slot
                print("search_date = " + str(search_date))
                print("search_slot = " + str(search_slot))
                for staff in staff_list:
                    #先看准准的时间有没有空
                    unavailable_timeslot = Timeslot.objects.filter(staff=staff,date__startswith=search_date,slot=search_slot).first()
                    if unavailable_timeslot is None: #有空
                        target_date.append(search_date)
                        target_slot.append(search_slot)
                        target_staff.append(staff)
                        # assign_timeslot = Timeslot(date=search_date,slot=search_slot,staff=staff,type=2) #智能推荐
                        print("找到时间 - " + staff.realname)
                        assign += 1
                        if assign < 2:
                            continue 
                        else:
                            break
                    else:
                        print("没有空档 - " + staff.realname)

                check_slot[int(search_slot)] = 1
                if 0 in check_slot:
                    search_slot = check_slot.index(0)
                if 0 not in check_slot or assign >= 2:
                    break
                
            check_slot = [1,0,0,0]
            search_slot = expect_timeslot
            if not stop_backward:
                forward = not forward
            

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

        #这边把推荐的时间段设成2
        if repair_type != '0' and staff in target_staff:
            index = target_staff.index(staff)
            interval = datetime.datetime.strptime(target_date[index], "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")
            str_date = "time" + str(3 * int(interval.days) + int(target_slot[index]))
            data[str_date] = '2'
            
        for j in range(int(period)):
            search_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=j)
            search_date = search_date.strftime("%Y-%m-%d")
            timeslot_list_accurate = timeslot_list.filter(date__startswith=search_date).order_by('slot')

            for timeslot in timeslot_list_accurate:
                if timeslot.staff == staff:
                    str_date = "time" + str(3 * int(j) + int(timeslot.slot))
                    data[str_date] = timeslot.type

        return_data.append(data)

    return return_response(1001, '返回排班信息',return_data)

@csrf_exempt
def save_library(request):
    if request.method != 'POST':
        return not_post_method()

    repair_id = request.POST.get('repair_id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    solution = request.POST.get('solution')

    repair = Repair.objects.filter(id=repair_id).first()
    repair.library_status=True
    repair.save()

    library = Library(title=title,description=description,staff_name=repair.staff.realname,
                      staff_contact=repair.staff.contactNumber,solution=solution,type=repair.type)

    library.save()

    return_data=model_to_dict(library)
    return_data['id'] = library.id

    return return_response(1001, '成功录入知识库',return_data)


