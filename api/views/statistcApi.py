
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

"""
separate by year -> category by month -> recognize different type in each month
"""

@csrf_exempt
def repair_statistic(request):
    if request.method != GETMETHOD:
        return not_get_method()

    year = request.GET.get('year','')



    if tenant_id:
        tenant = Tenant.objects.filter(id=tenant_id).first()
        payment_record = Payment.objects.filter(tenant=tenant,type=type).order_by('-paymentTime')
    if house_id:
        house = House.objects.filter(id=house_id).first()
        payment_record = Payment.objects.filter(house=house,type=type).order_by('-paymentTime')
    if tenant_id and house_id:
        payment_record = Payment.objects.filter(tenant=tenant,house=house,type=type).order_by('-paymentTime')
    
    if rental_id:
        rental = RentalInfo.objects.filter(id=rental_id).first()

        payment_list_data=[]
        year=None
        startyear = rental.startTime.strftime("%Y")
        first=1
    
        payment_data=[]    
        index = len(payment_record)

        time_prefix = ""
        #time_prefix set which year, and ascending order,start with jan
        record_list = Repair.objects.filter(createdTime__startswith=time_prefix).order_by('createdTime')
        
        first=1 
        record_list_data=[]
        record_data=[]
        index = len(record_list)
        month =None
        for record in record_list:
            if first:
                month = record.createdTime.strftime("%M")
                first=0

            if record.createdTime.strftime("%M") < month:
                record_list_data.append(record_data) 
                record_data=[]
                
                if int(record.createdTime.strftime("%M")) != int(month)-1:
                    while int(record.createdTime.strftime("%M")) != int(month)-1:
                        record_list_data.append(record_data) 
                        record_data=[]
                        year = str(int(month)-1)
                    year = record.createdTime.strftime("%M")   
                else:       
                    year = record.createdTime.strftime("%M")    

            data = {}
            data['month'] = month
            data['id'] = record.id
            data['paymentTime']=payment.paymentTime
            data['amount']=payment.amount
            print(data)
            payment_data.append(data) 

            index -= 1

            if index == 0 :
                year = payment.paymentTime.strftime("%Y")
                payment_list_data.append(payment_data) 
                payment_data=[]

        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': payment_list_data})

    payment_list_data=[]

    for payment in payment_record:
        data = {}
        data['id']=payment.id
        data['paymentTime']=payment.paymentTime
        data['amount']=payment.amount
        payment_list_data.append(data) 
            
    return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': payment_list_data})
    
    
    
