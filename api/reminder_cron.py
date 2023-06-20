from datetime import datetime,timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from api.utils import *
from django.forms.models import model_to_dict
from django.db.models import Q
import operator


def schedule_reminder():
    start_date = datetime.strptime("2029-12-02", "%Y-%m-%d")
    target_date = start_date + timedelta(days=30)
    # target_date = timezone.now().date() + timedelta(days=30)
    # target_date = timezone.now().date() + timedelta(days=30)

    rental_infos = RentalInfo.objects.filter(endTime=target_date)

    print("do something")
    for rental_info in rental_infos:
        print("\n++++++++++")
        print("id: ", rental_info.id)
        print("start_date: ", rental_info.startTime)
        print("end_date: ", rental_info.endTime)
        print("sign_date: ", rental_info.createdTime)

    return return_response(1001, 'something', rental_infos)