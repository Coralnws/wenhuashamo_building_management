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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now)
    slot  = models.CharField(max_length=1,choices=TIME_SLOT,default=TIME_SLOT[0][0])
    staff = models.ForeignKey("CustomUser",on_delete=models.CASCADE, null=False, blank=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)