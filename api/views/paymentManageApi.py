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
from ..error_utils import *
from django.forms.models import model_to_dict
from django.db.models import Q
import operator


@csrf_exempt
def update_record(request):
    if request.method == 'POST':
        info = request.POST.dict()
        payment_id = info.get('payment_id')
        is_paid = info.get('is_paid')
        payment_time = info.get('payment_time')

        record = Payment.objects.filter(id=payment_id).first()

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

        return return_response(1001, '成功修改缴费信息', data)
    else:
        return not_post_method()