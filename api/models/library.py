from django.db import models


class Library(models.Model):
    TYPES = (
        ('0','未分类'),
        ('1','水'),
        ('2','电'),
        ('3','机械'),
    )

    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    solution = models.TextField()
    staff_name = models.CharField(max_length=50,null=True,blank=True)
    staff_contact = models.CharField(max_length=50,null=True,blank=True)
    type = models.CharField(max_length=10,choices=TYPES,default=TYPES[0][0],null=True, blank=True)
