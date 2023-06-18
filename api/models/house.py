import uuid
from django.db import models
from django.utils import timezone
import os
import random


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roomNumber = models.IntegerField(unique=False)
    floor = models.IntegerField(blank=False)
    status = models.BooleanField(default=False)  # 租赁状态
    rentalInfo = models.ForeignKey("RentalInfo", related_name="rentalInfo", on_delete=models.CASCADE, null=True,
                                   blank=True)
    # tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=True, blank=True)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
