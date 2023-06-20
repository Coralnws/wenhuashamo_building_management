from django.db import models

from api.models.house import House


class VisitRequest(models.Model):
    name = models.CharField(max_length=100)
    ic = models.CharField(max_length=20)
    visit_time = models.DateTimeField()
    inviter = models.ForeignKey(House, related_name='inviter',on_delete=models.CASCADE,null=True,blank=True)
    contact_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=8)
    otp_sent = models.IntegerField()
    house = models.ForeignKey(House, related_name='invite_house',on_delete=models.CASCADE,null=True,blank=True)



