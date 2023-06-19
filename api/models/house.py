import uuid
from django.db import models
from django.utils import timezone
import os
import random


class House(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    roomNumber = models.IntegerField(unique=False)
    floor = models.IntegerField(blank=False)
    status = models.BooleanField(default=False)  # 租赁状态
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
