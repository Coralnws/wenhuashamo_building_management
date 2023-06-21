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


@csrf_exempt
def create_record(request):
    if request.method == 'POST':
        tenant_id = request.POST.get("tenant_id")
        period = request.POST.get('year')
        is_paid = request.POST.get('is_paid')
        payment_time = request.POST.get('payment_time') or None
        amount = request.POST.get('money')

        if is_paid == '未缴费' or is_paid == '0': 
            is_paid = False
        elif is_paid == '已缴费' or is_paid == '1':
            is_paid = True

        tenant = Tenant.objects.filter(id=tenant_id).first()
        record = Payment(tenant=tenant,period=period,is_paid=is_paid,paymentTime=payment_time,
                         amount=amount,type=2)
        record.save()
        data=model_to_dict(record)

        return return_response(1001, '成功添加物业费缴纳信息', data)
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})


@csrf_exempt
def delete_record(request):
    if request.method == 'POST':

        tenant_id = request.POST.get('tenant_id')
        year = request.POST.get('year')
        tenant = Tenant.objects.filter(id=tenant_id).first()
        record = Payment.objects.filter(tenant=tenant,period=year).first()
        record.delete()
    
        return UTF8JsonResponse({'errno':1001, 'msg': '成功删除物业费缴纳信息'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def update_record(request):
    if request.method == 'POST':
        info = request.POST.dict()
        tenant_id = info.get('tenant_id')
        period = info.get('year')
        new_period = info.get('new_year')
        is_paid = info.get('is_paid')
        payment_time = info.get('payment_time')
        amount = info.get('money')

        tenant = Tenant.objects.filter(id=tenant_id).first()
        record = Payment.objects.filter(tenant=tenant,period=period).first()

        if new_period:
            record.period = new_period
        if amount:
            record.amount = amount
        if is_paid:
            if is_paid == '未缴费' or is_paid == '0': 
                is_paid = False
            elif is_paid == '已缴费' or is_paid == '1':
                is_paid = True
            record.is_paid = is_paid
        if payment_time:
            record.paymentTime = payment_time
        
        record.save()
        data = model_to_dict(record)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改缴费信息','data': data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})    

@csrf_exempt
def update_payment_status(request):
    if request.method == 'POST':
        info = request.POST.dict()
        rental_info_id = info.get('rentalId')  #针对租赁合约
        type = info.get('type') #0-修改租赁费状态 1-修改物业费状态 
        status = info.get('status') #0=未缴费 1=已缴费
        time  = info.get('paymentTime') #修改的时间

        rental = RentalInfo.objects.filter(id=rental_info_id).first()
        
        if type == '1': #修改物业费
            if status and status=='0':
                rental.ispaid_management = False
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    rental.nextManagementFeeDeadline -= datetime.timedelta(days=365)

            if status and status=='1':
                rental.ispaid_management = True
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    rental.nextManagementFeeDeadline += datetime.timedelta(days=365)
        
        if type == '0':
            if status and status=='0':
                rental.ispaid_rental = False
                if time:
                    rental.nextRentalDeadline = time
                else:
                    rental.nextRentalDeadline -= datetime.timedelta(days=365)
            if status and status=='1':
                rental.ispaid_rental = True
                if time:
                    rental.nextRentalDeadline = time
                else:
                    rental.nextRentalDeadline += datetime.timedelta(days=365)
        rental.save()
        data = model_to_dict(rental)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改缴费信息','data': data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   


@csrf_exempt
def get_payment_detail(request):
    if request.method == 'GET':
        tenant_id = request.GET.get('tenantId','')
        house_id = request.GET.get('houseId','')
        rental_id = request.GET.get('rentalId','')
        type = request.GET.get('type','') #1-租赁费   2-物业费

        #必填：tenantId,rentalId,type=2
 
        tenant = None
        house = None
        payment_record = None
        rental = None
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
            for payment in payment_record:
                if first:
                    year = payment.paymentTime.strftime("%Y")
                    first=0

                if payment.paymentTime.strftime("%Y") < year:
                    payment_list_data.append(payment_data) 
                    payment_data=[]
                    
                    if int(payment.paymentTime.strftime("%Y")) != int(year)-1:
                        while int(payment.paymentTime.strftime("%Y")) != int(year)-1:
                            payment_list_data.append(payment_data) 
                            payment_data=[]
                            year = str(int(year)-1)
                        year = payment.paymentTime.strftime("%Y")   
                    else:       
                        year = payment.paymentTime.strftime("%Y")    

                if payment.paymentTime.strftime("%Y") < startyear:
                    break                  

                data = {}
                data['year'] = year
                data['id']=payment.id
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
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   


@csrf_exempt
def get_payment_record(request):
    if request.method == 'GET':
        tenant_id = request.GET.get('tenantId','')
        tenant = Tenant.objects.filter(id=tenant_id).first()
        payment_record = Payment.objects.filter(tenant=tenant,type=2).order_by('-paymentTime')
    
        payment_list_data=[]

        for payment in payment_record:
            data = {}
            data['id']=payment.id
            data['paymentTime']=payment.paymentTime
            data['amount']=payment.amount
            payment_list_data.append(data) 

        
        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': payment_list_data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def get_record(request):
    if request.method == 'GET':
        tenant_id = request.GET.get('tenant_id','')
        period = request.GET.get('year','')
        tenant = Tenant.objects.filter(id=tenant_id).first()
        record_list = Payment.objects.filter(tenant=tenant,type=2,period=period).order_by('-period')

        record_list_data=[]

        for record in record_list:
            data = {}
            data['id']=record.id
            data['year']=record.period
            data['is_paid']=record.is_paid
            data['payment_time']=record.paymentTime
            data['money']=record.amount
            record_list_data.append(data) 
        
        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': record_list_data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   