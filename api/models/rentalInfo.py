import uuid
from django.db import models
from django.utils import timezone


class RentalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey("House", on_delete=models.CASCADE, null=True, blank=True)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=False, blank=False)
    contract_id = models.CharField(max_length=20,null=True, blank=True)
    createdTime = models.DateTimeField(default=timezone.now)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    rental_fee = models.IntegerField(default=0)  #租赁费
    management_fee = models.IntegerField(default=0)  #物业费
    nextRentalDeadline = models.DateTimeField(null=True, blank=True)   #租赁费截止 每次付款更新截止日期，若截止日期 < 现在则欠费
    nextManagementFeeDeadline = models.DateTimeField(null=True, blank=True)   #物业费截止
    paidRentalDate = models.DateTimeField(null=True, blank=True)
    paidManagementDate = models.DateTimeField(null=True, blank=True)
    ispaid_rental = models.BooleanField(default=False)
    ispaid_management = models.BooleanField(default=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
