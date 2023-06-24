import datetime
from django.utils import timezone
from api.views import sms

def schedule_otp_sms():
    # Query visit request with duration 30minutes earlier and not yet sent otp
    # generate code
    # send sms
    pass