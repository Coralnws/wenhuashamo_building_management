from django.db import models
from django.utils import timezone
from api.models.house import House
from api.models.users import CustomUser


class VisitRequest(models.Model):
    name = models.CharField(max_length=100)
    ic = models.CharField(max_length=20)
    visit_time = models.DateTimeField()
    company = models.CharField(max_length=20,null=True,blank=True)
    inviter = models.ForeignKey(CustomUser, related_name='inviter',on_delete=models.CASCADE,null=True,blank=True)
    contact_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=8)
    otp_sent = models.IntegerField()
    house = models.ForeignKey(House, related_name='invite_house',on_delete=models.CASCADE,null=True,blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


