import uuid
from django.db import models
from django.utils import timezone


class RentalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=False, blank=False)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=False, blank=False)
    createdTime = models.DateTimeField(default=timezone.now)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    fee = models.IntegerField()  #租赁费
    nextRentalDeadline = models.DateTimeField(null=True)   #租赁费截止 每次付款更新截止日期，若截止日期 < 现在则欠费
    nextManagementFeeDeadline = models.DateTimeField(null=True)   #物业费截止
    lastPay = models.DateTimeField()
    ispaid_rental = models.BooleanField(default=False)
    ispaid_management = models.BooleanField(default=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
