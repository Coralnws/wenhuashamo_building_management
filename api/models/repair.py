from django.db import models
from django.contrib.auth.models import User
import os,random
from api.models.house import House
from api.models.users import CustomUser
from backend.settings import MEDIA_URL

def repairPhoto_to(instance, filename):
    return os.path.join('repair', instance.username, str(random.uniform(1000, 9999)) + 'repair.png')
    
class Repair(models.Model):
    description = models.CharField(max_length=200)
    createdTime = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    company = models.CharField(max_length=50,null=True,blank=True)
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    contactName = models.CharField(max_length=50,null=True,blank=True)
    contactNumber = models.CharField(max_length=20,null=True,blank=True)
    staff = models.ForeignKey(CustomUser, related_name="repair_staff",on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(CustomUser,related_name="repair_manager",  on_delete=models.CASCADE, null=True, blank=True)
    repairingTime = models.DateTimeField(null=True, blank=True)

    staffContact = models.CharField(max_length=20,null=True,blank=True)
    status_choices = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Open')
    plan = models.TextField(null=True,blank=True)
    completeTime = models.DateTimeField(null=True, blank=True)
    solver = models.ForeignKey(CustomUser, related_name="repair_solver", on_delete=models.CASCADE, null=True, blank=True)
    #photo = models.ImageField(upload_to=repairPhoto_to, blank=True)


    def get_photo_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return os.path.join(MEDIA_URL, str(self.thumbnail))
        return os.path.join(MEDIA_URL, 'default', 'thumbnail.png')