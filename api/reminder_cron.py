import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from api.utils import *
from django.forms.models import model_to_dict
from django.db.models import Q
import operator
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


scheduler = BackgroundScheduler()

scheduler.add_jobstore(DjangoJobStore(), 'default')


def test(s):
    print("_____TESTING____EXE_____")
    pass

# 注册定时任务并开始
register_events(scheduler)
scheduler.start()



def schedule_reminder():
    print("____EXE_____")
    print("____EXE_____")

def schedule_reminder1(request):
    # start_date = datetime.datetime.strptime("2029-12-02", "%Y-%m-%d")
    # target_date = start_date + datetime.timedelta(days=30)
    # target_date = timezone.now().date() + timedelta(days=30)
    target_date = timezone.now().date() + datetime.timedelta(days=30)

    rental_infos = RentalInfo.objects.filter(endTime=target_date)

    print("+++++ START CRONJOB ++++++")
    print("target date:", target_date)
    # for rental_info in rental_infos:
    #     print("\n++++++++++")
    #     print("id: ", rental_info.id)
    #     print("start_date: ", rental_info.startTime)
    #     print("end_date: ", rental_info.endTime)
    #     print("sign_date: ", rental_info.createdTime)
    #     send_reminder_smtp(rental_info)

    return return_response(1001, 'something')


#send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
def send_reminder_smtp(rental_info):
    room_list = ', '.join([str(item.house.roomNumber) for item in TenantRental.objects.filter(rental=rental_info)])
    context = {
        'rental_id': rental_info.id,
        'sign_time': rental_info.createdTime.date,
        'start_time': rental_info.startTime.date,
        'end_time': rental_info.endTime.date,
        'company_name': rental_info.tenant.company,
        'legal_name': rental_info.tenant.real_name,
        'contact_name': rental_info.tenant.contactName,
        'email': rental_info.tenant.email,
        'rooms': room_list,
    }


    print(settings.EMAIL_FROM_USER)
    email = EmailMessage(
        "租赁信息提醒",
        render_to_string("reminder.txt", context),
        settings.EMAIL_FROM_USER, # FROM
        # [rental_info.tenant.email],    #TO
        ["foueducation@gmail.com"],
    )

    email.send(fail_silently=False)
    return return_response(1001, "邮件已发送")
