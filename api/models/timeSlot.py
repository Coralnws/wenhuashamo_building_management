import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date

class Timeslot(models.Model):
    TIME_SLOT = (
        ('0','None'),
        ('1','9:00am-12:00pm'),
        ('2','12:00pm-3:00pm'),
        ('3','3:00pm-6:00pm'),
    )
    TYPE = (
        ('0','空闲'),
        ('1','已分派'),
        ('2','智能推荐')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now)
    slot  = models.CharField(max_length=1,choices=TIME_SLOT,default=TIME_SLOT[0][0])
    staff = models.ForeignKey("CustomUser",on_delete=models.SET_NULL, null=True,blank=True)
    type = models.CharField(max_length=1,choices=TYPE,default=TYPE[0][0])

    repair_info = models.ForeignKey("Repair",related_name='repair_info',on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)