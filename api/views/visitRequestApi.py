
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
1. createRequest
2. delRequest
3. updateRequest
4. getRequest
    - customer(userId)
    - manager:order by company + time/search by company + room
'''
def gen_code(length=6):
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
        print(rand_str)
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

    inviter = CustomUser.objects.filter(id=user_id).first()

    code=gen_code()
    
    visit = VisitRequest(name=visitor_name,ic=visitor_ic,contact_number=visitor_contact,visit_time=visit_time,
                             otp=code,company=company,otp_sent=0,inviter=inviter)
        
    visit.save()
    data=model_to_dict(visit)

    return return_response(1001, '创建访客申请成功', data)        


        
    
        
#加个公司属性,otp_sent改成booleanfield

'''
为确保大厦安全，大厦访客必须经过预约登记进入。由客户公司邀请人在系统提出访客申请，包括访客人员姓名、身份证号码、
到访时间（具体到某日几点）、手机号码。
申请提交后，系统无需审核，只需要自动于预定到访时间前半小时给访客手机发送动态密码，便于访客密码方式进入大厦。

    name = models.CharField(max_length=100)
    ic = models.CharField(max_length=20)
    visit_time = models.DateTimeField()
    company = models.CharField(max_length=20,null=True,blank=True)
    inviter = models.ForeignKey(House, related_name='inviter',on_delete=models.CASCADE,null=True,blank=True)
    contact_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=8)
    otp_sent = models.IntegerField()
    house = models.ForeignKey(House, related_name='invite_house',on_delete=models.CASCADE,null=True,blank=True)
'''