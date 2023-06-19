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
def createRecord(request):
    if request.method == 'POST':
        tenant_id = request.POST.get("tenant_id")
        period = request.POST.get('year')
        is_paid = request.POST.get('is_paid')
        payment_time = request.POST.get('payment_time')
        amount = request.POST.get('money')

        if is_paid == '0':
            is_paid = False
        elif is_paid == '1':
            is_paid = True

        tenant = Tenant.objects.filter(id=tenant_id).first()
        record = Payment(tenant=tenant,period=period,is_paid=is_paid,paymentTime=payment_time,
                         amount=amount,type=2)
        record.save()
        data=model_to_dict(record)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加物业费缴纳信息','data':data})    
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

"""
@csrf_exempt
def createRecord(request):
    if request.method == 'POST':
        info = request.POST.dict()
        tenantId = info.get('tenantId') #针对租客
        houseId = info.get('houseId')  #针对房屋
        rentalInfoId = info.get('rentalId')  #针对租赁合约

        type = info.get('paymentType')
        date = info.get('paymentTime')
        amount = info.get('amount')
    
        payment = Payment()

        if tenantId:
            tenant = Tenant.objects.filter(id=tenantId).first()
            payment.tenant = tenant
        if houseId:
            house = House.objects.filter(id=houseId).first()
            payment.house = house
        if rentalInfoId:
            rentalInfo = RentalInfo.objects.filter(id=rentalInfoId).first()
            payment.rentalInfo = rentalInfo
        if type:
            payment.type = type
        if date:
            payment.createdTime = date
        if amount:
            payment.amount = amount

        payment.save()
        data = model_to_dict(payment)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加缴费信息','data':data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})
"""

@csrf_exempt
def deleteRecord(request):
    if request.method == 'POST':
        # userId=request.session.get('uid')
        # if userId is None:
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
        # user = CustomUser.objects.filter(id=userId).first()
        # if user.position != 4 and user.position != 3:
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '无权限'})

        record_id = request.POST.get('record_id')
        record = Payment.objects.filter(id=record_id).first()
        record.delete()
    
        return UTF8JsonResponse({'errno':1001, 'msg': '成功删除物业费缴纳信息'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def updateRecord(request):
    if request.method == 'POST':
        info = request.POST.dict()
        record_id = info.get('record_id')
        period = info.get('year')
        is_paid = info.get('is_paid')
        payment_time = info.get('payment_time')
        amount = info.get('money')

        record = Payment.objects.filter(id=record_id).first()

        if period:
            record.period = period
        if amount:
            record.amount = amount
        if is_paid:
            record.is_paid = is_paid
        if payment_time:
            record.paymentTime = payment_time
        
        record.save()
        data = model_to_dict(record)

        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改缴费信息','data': data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})    

@csrf_exempt
def updatePaymentStatus(request):
    if request.method == 'POST':
        info = request.POST.dict()
        rentalInfoId = info.get('rentalId')  #针对租赁合约
        type = info.get('type') #0-修改租赁费状态 1-修改物业费状态 
        status = info.get('status') #0=未缴费 1=已缴费
        time  = info.get('paymentTime') #修改的时间

        rental = RentalInfo.objects.filter(id = rentalInfoId).first()
        
        if type == '1': #修改物业费
            if status and status=='0':
                rental.ispaid_management = False
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    #date = rental.nextManagementFeeDeadline
                    rental.nextManagementFeeDeadline -= datetime.timedelta(days=365)
                    # date.replace(year = date.year - 1)
                    # print(date)
                    # rental.nextManagementFeeDeadline = date
                
                
            if status and status=='1':
                rental.ispaid_management = True
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    rental.nextManagementFeeDeadline += datetime.timedelta(days=365)
                    # date = rental.nextManagementFeeDeadline
                    # date.replace(year = date.year + 1)
                    # rental.nextManagementFeeDeadline = date
        
        if type == '0':
            if status and status=='0':
                rental.ispaid_rental = False
                if time:
                    rental.nextRentalDeadline = time
                else:
                    rental.nextRentalDeadline -= datetime.timedelta(days=365)
                    # date = rental.nextRentalDeadline
                    # date.replace(year = date.year - 1)
                    # rental.nextRentalDeadline = date
            if status and status=='1':
                rental.ispaid_rental = True
                if time:
                    rental.nextRentalDeadline = time
                else:
                    rental.nextRentalDeadline += datetime.timedelta(days=365)
                    # date = rental.nextRentalDeadline
                    # date.replace(year = date.year + 1)
                    # rental.nextRentalDeadline = date
        rental.save()
        data = model_to_dict(rental)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改缴费信息','data': data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   


@csrf_exempt
def getPaymentDetail(request):
    if request.method == 'GET':
        tenantId = request.GET.get('tenantId','')
        houseId = request.GET.get('houseId','')
        rentalId = request.GET.get('rentalId','')
        type = request.GET.get('type','') #1-租赁费   2-物业费
 
        tenant = None
        house = None
        PaymentRecord = None
        rental = None
       
        if tenantId:
            tenant = Tenant.objects.filter(id=tenantId).first()
            PaymentRecord = Payment.objects.filter(tenant=tenant,type=type).order_by('-paymentTime')
        if houseId:
            house = House.objects.filter(id=houseId).first()
            PaymentRecord = Payment.objects.filter(house=house,type=type).order_by('-paymentTime')
        if tenantId and houseId:
            PaymentRecord = Payment.objects.filter(tenant=tenant,house=house,type=type).order_by('-paymentTime')
        
        if rentalId:
            rental = RentalInfo.objects.filter(id=rentalId).first()

            paymentListData=[]
            #year = rental.startTime.strftime("%Y")
            year=None
            startyear = rental.startTime.strftime("%Y")
            first=1
        
            paymentData=[]    
            index = len(PaymentRecord)
            for payment in PaymentRecord:
                if first:
                    year = payment.paymentTime.strftime("%Y")
                    first=0

                if payment.paymentTime.strftime("%Y") < year:
                    paymentListData.append(paymentData) 
                    paymentData=[]
                    
                    if int(payment.paymentTime.strftime("%Y")) != int(year)-1:
                        while int(payment.paymentTime.strftime("%Y")) != int(year)-1:
                            paymentListData.append(paymentData) 
                            paymentData=[]
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
                paymentData.append(data) 

                index -= 1

                if index == 0 :
                    year = payment.paymentTime.strftime("%Y")
                    paymentListData.append(paymentData) 
                    paymentData=[]

            return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': paymentListData})

        paymentListData=[]
                                            
        for payment in PaymentRecord:            
            data = {}
            data['id']=payment.id
            data['paymentTime']=payment.paymentTime
            data['amount']=payment.amount
            paymentListData.append(data) 
                
        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': paymentListData})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   
#.strftime("%Y-%m-%d %H:%M")


@csrf_exempt
def getPaymentRecord(request):
    if request.method == 'GET':
        tenantId = request.GET.get('tenantId','')
        tenant = Tenant.objects.filter(id=tenantId).first()
        PaymentRecord = Payment.objects.filter(tenant=tenant,type=2).order_by('-paymentTime')
    
        paymentListData=[]

                                            
        for payment in PaymentRecord:            
            data = {}
            data['id']=payment.id
            data['paymentTime']=payment.paymentTime
            data['amount']=payment.amount
            paymentListData.append(data) 

        
        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': paymentListData})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   
#.strftime("%Y-%m-%d %H:%M")

@csrf_exempt
def getRecord(request):
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