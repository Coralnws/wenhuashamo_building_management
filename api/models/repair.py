from django.db import models
from django.contrib.auth.models import User
import os,random
from api.models.house import House
from api.models.users import CustomUser
from api.models.timeSlot import Timeslot
from backend.settings import MEDIA_URL

def repair_photo_to(instance, filename):
    return os.path.join('repair', instance.username, str(random.uniform(1000, 9999)) + 'repair.png')
    
class Repair(models.Model):
    TIME_SLOT = (
        ('0','None'),
        ('1','9:00am-12:00pm'),
        ('2','12:00pm-3:00pm'),
        ('3','3:00pm-6:00pm'),
    )
    
    TYPE = (
        ('0','未分类'),
        ('1','水'),
        ('2','电'),
        ('3','机械'),
    )

    description = models.CharField(max_length=200)
    title = models.CharField(max_length=200,null=True, blank=True)
    createdTime = models.DateTimeField(null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.SET_NULL,null=True,blank=True)
    company = models.CharField(max_length=50,null=True,blank=True)
    submitter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True)
    contactName = models.CharField(max_length=50,null=True,blank=True)
    contactNumber = models.CharField(max_length=20,null=True,blank=True)
    staff = models.ForeignKey(CustomUser, related_name="repair_staff",on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(CustomUser,related_name="repair_manager",  on_delete=models.SET_NULL, null=True, blank=True)
    repairingTime = models.DateTimeField(null=True, blank=True)
    time_slot = models.ForeignKey(Timeslot,related_name="repair_time",  on_delete=models.SET_NULL, null=True, blank=True)
    staffContact = models.CharField(max_length=20,null=True,blank=True)
    expect_date = models.DateTimeField(null=True, blank=True)
    expect_time_slot = models.CharField(max_length=1,choices=TIME_SLOT,default=TIME_SLOT[0][0],null=True, blank=True)
    type = models.CharField(max_length=10,choices=TYPE,default=TYPE[0][0],null=True, blank=True)

    status_choices = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
    ]
    
    status = models.CharField(max_length=20, choices=status_choices, default='Open')
    plan = models.TextField(null=True,blank=True)
    completeTime = models.DateTimeField(null=True, blank=True)
    solver = models.ForeignKey(CustomUser, related_name="repair_solver", on_delete=models.CASCADE, null=True, blank=True)


    def get_photo_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return os.path.join(MEDIA_URL, str(self.thumbnail))
        return os.path.join(MEDIA_URL, 'default', 'thumbnail.png')