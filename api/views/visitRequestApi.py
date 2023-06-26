
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


def gen_code(length=6):
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
    return rand_str

@csrf_exempt
def create_request(request):
    if request.method != 'POST':
        return not_post_method()
    
    user_id = request.POST.get('user_id')
    visitor_name = request.POST.get('visitor_name')
    visitor_ic = request.POST.get('visitor_ic')
    visit_time = request.POST.get('visit_time')
    visitor_contact = request.POST.get('visitor_contact')
    company = request.POST.get('company')
    room = request.POST.get('room')

    inviter = CustomUser.objects.filter(id=user_id).first()
    house = House.objects.filter(roomNumber=room).first()

    code=gen_code()

    visit_time_obj = datetime.datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S")
    otp_send = 0 if visit_time_obj > timezone.now() else 1

    visit = VisitRequest(name=visitor_name,ic=visitor_ic,contact_number=visitor_contact,visit_time=visit_time,
                             otp=code,company=company,otp_sent=otp_send,inviter=inviter,house=house)
        
    visit.save()
    data=model_to_dict(visit)
    data['id']=visit.id

    return return_response(1001, '创建访客申请成功', data)        

@csrf_exempt
def del_request(request):
    if request.method != 'POST':
        return not_post_method()

    visit_id = request.POST.get('visit_id')
    visit = VisitRequest.objects.filter(id=visit_id).first()
    visit.delete()

    return return_response(1001, '删除访客申请成功')        


@csrf_exempt
def update_request(request):
    if request.method != 'POST':
        return not_post_method()
    
    info = request.POST.dict()
    visit_id = info.get('visit_id')
    visitor_name = info.get('visitor_name')
    visitor_ic = info.get('visitor_ic')
    visit_time = info.get('visit_time')
    visitor_contact = info.get('visitor_contact')
    company = info.get('company')
    resend = info.get('resend')
    room = info.get('room')

    visit = VisitRequest.objects.filter(id=visit_id).first()
    if visitor_name:
        visit.name = visitor_name
    if visitor_ic:
        visit.ic = visitor_ic
    if visit_time:
        visit.visit_time = visit_time
    if visitor_contact:
        visit.contact_number = visitor_contact
    if company:
        visit.company = company
    if resend:
        code = gen_code()
        visit.otp = code
    if room:
        house = House.objects.filter(roomNumber=room).first()
        visit.house=house
    
    visit.save()
    data=model_to_dict(visit)
    
    return return_response(1001, '更新访客申请成功',data)

@csrf_exempt
def get_request(request):
    if request.method != 'GET':
        return not_get_method()
    
    user_id = request.GET.get('user_id','')
    company = request.GET.get('company','')

    user = CustomUser.objects.filter(id=user_id).first()
    position = user.position


    if position == '1':
        print("普通用户")
        user_company = user.tenant.company
        visit_list = VisitRequest.objects.filter(company=user_company).order_by('-updated_at')
    elif position == '3' or position == '4':
        print("管理人员")
        if company:
            visit_list = VisitRequest.objects.filter(company=company).order_by('-updated_at')
        else:
            visit_list = VisitRequest.objects.all().order_by('-updated_at')


    visit_list_data=[]

    for visit in visit_list:
        visit_data = {}
        visit_data['id']=visit.id
        visit_data['visitor_name']=visit.name
        visit_data['visitor_ic']=visit.ic
        visit_data['visitor_time'] = visit.visit_time
        visit_data['contact_number']=visit.contact_number
        visit_data['company'] = visit.company
        visit_data['room'] = str(visit.house.roomNumber) or None
        visit_data['inviter_name']=visit.inviter.realname

        if position == '3' or position == '4':
            visit_data['otp_sent'] = visit.otp_sent
            visit_data['otp'] = visit.otp

        

        visit_list_data.append(visit_data)

    return return_response(1001, '获取访客申请列表成功',visit_list_data)

@csrf_exempt
def reset_request(request):
    if request.method != 'GET':
        return not_get_method()
    current_date = date.today()
    visit_list = VisitRequest.objects.filter(visit_time__gt=current_date)

    for visit in visit_list:
        print(visit.visit_time)
        visit.otp_sent = 0
        visit.save()
