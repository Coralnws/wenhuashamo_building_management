import datetime
from django.utils import timezone
from api.views import sms
from api.models import VisitRequest
from django.db.models import Q
from api.utils import *

def schedule_otp_sms(request):
    target_time = timezone.now() + datetime.timedelta(hours=0.5)
    print("target_time", target_time)

    visit_requests = VisitRequest.objects.filter(Q(otp_sent=0) & Q(visit_time__lte=target_time) & Q(visit_time__gte=timezone.now()))

    for v in visit_requests:
        code = get_random_codes()
        res = sms.phone_send("19568729194", code)
        # check if res successfull, then update the otp_sent and code, otherwise fail silently
        if res.data.Code == 'OK':
            v.otp = code
            v.otp_sent += 1
            v.save()
    
    return return_response(1000001, 'Done Sending SMS')


def get_random_codes():
    code = ''
    str1 = '0123456789'
    for i in range(0, 6):
        code += str1[random.randrange(0, len(str1))]
    return code