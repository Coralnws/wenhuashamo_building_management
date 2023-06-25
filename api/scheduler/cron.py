import datetime
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from backend import settings
from api.models import *
from api.utils import *
from api.scheduler.email_reminder import *
from api.scheduler.sms_reminder import *


def start():
    print("JOB STARTING")
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    scheduler.add_job(
        schedule_fee_email,
        "cron",
        hour= 0,
        minute= 0,
        second= 0,
        id= "schedule_fee_email",
        replace_existing= True
    )

    scheduler.add_job(
        schedule_otp_sms,
        "interval",
        seconds= 60,
        id= "schedule_otp_sms",
        replace_existing= True
    )

    scheduler.start()
    print("SCHEDULING STARTINGGGG")


