import datetime
from django.utils import timezone
from api.models import RentalInfo


def schedule_fee_email():
    # set fixed date to testing
    # start_date = datetime.datetime.strptime("2029-12-02", "%Y-%m-%d")
    # target_date = start_date + datetime.timedelta(days=30)
    target_date = timezone.now().date() + datetime.timedelta(days=30)

    rental_infos = RentalInfo.objects.filter(endTime=target_date)

    print("+++++ START SENDING REMINDER EMAIL CRON ++++++")
    print("FOR target date:", target_date)
    for rental_info in rental_infos:
        print("\n++++++++++")
        print("id: ", rental_info.id)
        print("start_date: ", rental_info.startTime)
        print("end_date: ", rental_info.endTime)
        print("sign_date: ", rental_info.createdTime)
        #send_fee_reminder_smtp(rental_info)
        print("++++++++++")


def send_fee_reminder_smtp(rental_info):
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

    email = EmailMessage(
        "租赁信息提醒",
        render_to_string("reminder.txt", context),
        settings.EMAIL_FROM_USER, # FROM
        # [rental_info.tenant.email],    #TO
        ["foueducation@gmail.com"],
    )

    email.send(fail_silently=False)
    print("Email sent successfully")
