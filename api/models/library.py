from django.db import models


class Library(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    solution = models.TextField()
    staff_name = models.CharField(max_length=50,null=True,blank=True)
    staff_contact = models.CharField(max_length=50,null=True,blank=True)

