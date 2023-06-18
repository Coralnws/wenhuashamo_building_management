import uuid
from django.db import models
from django.utils import timezone

class Payment(models.Model):
    TYPE = (
        ('0','暂无'),
        ('1','租赁费'),
        ('2','物业费'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=True, blank=True)
    createdTime = models.DateTimeField(default=timezone.now)
    tenant = models.ForeignKey("Tenant", related_name="tenant_pay",on_delete=models.CASCADE, null=True, blank=True)
    rentalInfo = models.ForeignKey("RentalInfo", related_name="rentalinfo_pay",on_delete=models.CASCADE, null=True, blank=True)
    house =  models.ForeignKey("House",  related_name="house_pay",on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE,default='0')
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
