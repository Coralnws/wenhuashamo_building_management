import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, blank=True)
    real_name = models.CharField(max_length=150) #法人名称
    company = models.CharField(max_length=150, unique=True) #公司名称
    contactName = models.CharField(max_length=150)  # 联系人名称
    contactNumber = models.CharField(max_length=150, unique=True) #联系人联系电话
    email = models.EmailField(blank=True)

    # 默认属性
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

