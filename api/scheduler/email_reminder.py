import datetime
from django.utils import timezone
from api.models import RentalInfo, TenantRental, Payment
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


# based on payment instead of rental Info
def schedule_fee_email():
    one_month_later = timezone.now().date() + datetime.timedelta(days=30)
    payment_infos = Payment.objects.filter(end_time=one_month_later, is_paid=False)

    print("+++++ START SENDING REMINDER EMAIL CRON ++++++")
    print("FOR target date:", one_month_later)
    for payment_info in payment_infos:
        print("\n++++++++++")
        print("contact id: ", payment_info.rentalInfo.contract_id)
        print("period: ", payment_info.period)
        print("start_date: ", payment_info.rentalInfo.startTime.strftime("%Y年 %m月 %d日"))
        print("end_date: ", payment_info.rentalInfo.endTime.strftime("%Y年 %m月 %d日"))
        send_fee_reminder_smtp(payment_info)
        print("++++++++++")


def send_fee_reminder_smtp(payment_info):
    room_list = ', '.join([str(item.house.roomNumber) for item in TenantRental.objects.filter(rental=payment_info.rentalInfo)])
    context = {
        'rental_id': payment_info.rentalInfo.contract_id,
        'period': payment_info.period,
        'sign_time': payment_info.rentalInfo.createdTime.strftime("%Y年 %m月 %d日"),
        'start_time': payment_info.rentalInfo.startTime.strftime("%Y年 %m月 %d日"),
        'end_time': payment_info.rentalInfo.endTime.strftime("%Y年 %m月 %d日"),
        'company_name': payment_info.tenant.company,
        'legal_name': payment_info.tenant.real_name,
        'contact_name': payment_info.tenant.contactName,
        'email': payment_info.tenant.email,
        'rooms': room_list,
    }

    print("sending email to:", payment_info.rentalInfo.tenant.email)
    email = EmailMessage(
        "租赁缴费提醒",
        render_to_string("reminder_payment.txt", context),
        settings.EMAIL_FROM_USER, # FROM
        [payment_info.rentalInfo.tenant.email, "legendofunique@hotmail.com"],    #TO
    )

    email.send(fail_silently=False)
    print("Email sent successfully")



def schedule_fee_based_on_rental_info_email():

    one_month_later = timezone.now().date() + datetime.timedelta(days=30)

    rental_infos = RentalInfo.objects.filter(
        startTime__year__lt=one_month_later.year,
        endTime__year__gte=one_month_later.year,
        endTime__month=one_month_later.month,
        endTime__day=one_month_later.day,
    )

    print("+++++ START SENDING REMINDER EMAIL CRON ++++++")
    print("FOR target date:", one_month_later)
    for rental_info in rental_infos:
        print("\n++++++++++")
        print("contact id: ", rental_info.contract_id)
        print("start_date: ", rental_info.startTime.strftime("%Y年 %m月 %d日"))
        print("end_date: ", rental_info.endTime.strftime("%Y年 %m月 %d日"))
        print("sign_date: ", rental_info.createdTime.strftime("%Y年 %m月 %d日"))
        send_fee_reminder_smtp(rental_info)
        print("++++++++++")


def send_fee_reminder_based_on_rental_info_smtp(rental_info):
    room_list = ', '.join([str(item.house.roomNumber) for item in TenantRental.objects.filter(rental=rental_info)])
    context = {
        'rental_id': rental_info.contract_id,
        'sign_time': rental_info.createdTime.strftime("%Y年 %m月 %d日"),
        'start_time': rental_info.startTime.strftime("%Y年 %m月 %d日"),
        'end_time': rental_info.endTime.strftime("%Y年 %m月 %d日"),
        'company_name': rental_info.tenant.company,
        'legal_name': rental_info.tenant.real_name,
        'contact_name': rental_info.tenant.contactName,
        'email': rental_info.tenant.email,
        'rooms': room_list,
    }

    email = EmailMessage(
        "租赁信息提醒",
        render_to_string("reminder.txt", context),
        settings.EMAIL_FROM_USER, # FROM
        [rental_info.tenant.email, "legendofunique@hotmail.com"],    #TO
    )

    email.send(fail_silently=False)
    print("Email sent successfully")
