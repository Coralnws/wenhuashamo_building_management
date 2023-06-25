import datetime
from django.utils import timezone
from api.models import RentalInfo, TenantRental
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def schedule_fee_email():

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
        print("start_date: ", rental_info.startTime)
        print("end_date: ", rental_info.endTime)
        print("sign_date: ", rental_info.createdTime)
        send_fee_reminder_smtp(rental_info)
        print("++++++++++")


def send_fee_reminder_smtp(rental_info):
    room_list = ', '.join([str(item.house.roomNumber) for item in TenantRental.objects.filter(rental=rental_info)])
    context = {
        'rental_id': rental_info.contract_id,
        'sign_time': rental_info.createdTime.date,
        'start_time': rental_info.startTime.date,
        'end_time': rental_info.endTime.date,
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
        # [rental_info.tenant.email],    #TO
        ["foueducation@gmail.com"],
    )

    email.send(fail_silently=False)
    print("Email sent successfully")
