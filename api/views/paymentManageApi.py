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
            payment.hosue = house
        if rentalInfoId:
            rentalInfo = RentalInfo.objects.filter(id=rentalInfoId).first()
            payment.rentalInfo = rentalInfo
        if type:
            payment.type = type
        if date:
            payment.date = date
        if amount:
            payment.amount = amount

        payment.save()

        return UTF8JsonResponse({'errno':1001, 'msg': '成功添加缴费信息'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def deleteRecord(request):
    if request.method == 'POST':
        # userId=request.session.get('uid')
        # if userId is None:
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '当前cookie为空，未登录，请先登录'})
        # user = CustomUser.objects.filter(id=userId).first()
        # if user.position != 4 and user.position != 3:
        #     return UTF8JsonResponse({'errno': 3001, 'msg': '无权限'})

        recordId = request.POST.get('recordId')
        record = Payment.objects.filter(id=recordId).first()
        record.delete()
    
        return UTF8JsonResponse({'errno':1001, 'msg': '成功删除缴费信息'})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})

@csrf_exempt
def updateRecord(request):
    if request.method == 'POST':
        info = request.POST.dict()
        recordId = info.get('recordId')
        date = info.get('paymentTime')
        amount = info.get('amount')

        record = Payment.objects.filter(id=recordId).first()

        if date:
            record.createdTime = date
        if amount:
            record.amount = amount
        
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
                rental.unpaid_management = True
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    date = rental.nextManagementFeeDeadline
                    date.replace(year = date.year - 1)
                    rental.nextManagementFeeDeadline = date
                    #rental.nextManagementFeeDeadline -= datetime.timedelta(days=365)
                
            if status and status=='1':
                rental.unpaid_management = False
                if time:
                    rental.nextManagementFeeDeadline = time
                else:
                    date = rental.nextManagementFeeDeadline
                    date.replace(year = date.year + 1)
                    rental.nextManagementFeeDeadline = date
        
        if type == '0':
            if status and status=='0':
                rental.unpaid_rental = True
                if time:
                    rental.nextRentalDeadline = time
                else:
                    date = rental.nextRentalDeadline
                    date.replace(year = date.year - 1)
                    rental.nextRentalDeadline = date
            if status and status=='1':
                rental.unpaid_rental = False
                if time:
                    rental.nextRentalDeadline = time
                else:
                    date = rental.nextRentalDeadline
                    date.replace(year = date.year + 1)
                    rental.nextRentalDeadline = date
        rental.save()
        data = model_to_dict(rental)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功修改缴费信息','data': data})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   


@csrf_exempt
def getPaymentRecord(request):
    if request.method == 'GET':
        tenantId = request.GET.get('tenantId','')
        houseId = request.GET.get('houseId','')
        rentalId = request.GET.get('rentalId','')
        type = request.GET.get('type','') #1-租赁费   2-物业费
 
        tenant = None
        house = None
        PaymentRecord = None
        rentalInfo = None
       
        if tenantId:
            tenant = Tenant.objects.filter(id=tenantId).first()
            PaymentRecord = Payment.objects.filter(tenant=tenant,type=type).order_by('-createdTime')
        if houseId:
            house = House.objects.filter(id=houseId).first()
            PaymentRecord = Payment.objects.filter(house=house,type=type).order_by('-createdTime')
        if tenantId and houseId:
            PaymentRecord = Payment.objects.filter(tenant=tenant,house=house,type=type).order_by('-createdTime')
        if rentalId:
            rental = RentalInfo.objects.filter(id=rentalInfo).first()
            PaymentRecord = Payment.objects.filter(rentalInfo=rental,type=type).order_by('-createdTime')

        #这边找到rentalInfo

        paymentListData=[]
        year = rentalInfo.startTime.strftime("%Y")
        print("start at" + year)
        first = True 
                                                      
        for payment in PaymentRecord:
            paymentData={}
            if payment.createdTime.strftime("%Y") > year:
                year = payment.createdTime.strftime("%Y")
                paymentListData.append(paymentData) 
                first=True;
            
            if first:
                paymentData['year'] = year
                first=False;
            
            data = {}
            data['id']=payment.id
            data['paymentTime']=payment.createdTime
            data['amount']=payment.amount
            paymentData.append(paymentData) 

        
        return UTF8JsonResponse({'errno':1001, 'msg': '返回缴费记录成功', 'data': paymentListData})
    else:
        return UTF8JsonResponse({'errno':4001, 'msg': 'Request Method Error'})   
#.strftime("%Y-%m-%d %H:%M")
        