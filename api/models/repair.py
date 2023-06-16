from django.db import models
from django.contrib.auth.models import User

from api.models.house import House
from api.models.users import CustomUser


class Repair(models.Model):
    description = models.CharField(max_length=200)
    createdTime = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    contactName = models.CharField(max_length=50)
    contactNumber = models.CharField(max_length=20)
    staff = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True, blank=True)
    repairingTime = models.DateTimeField(null=True, blank=True)
    status_choices = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Open')
    plan = models.TextField(blank=True)
    completeTime = models.DateTimeField(null=True, blank=True)
    solver = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True, blank=True)