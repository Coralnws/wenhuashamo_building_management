from django.db import models

from api.models.house import House


class VisitRequest(models.Model):
    name = models.CharField(max_length=100)
    ic = models.CharField(max_length=20)
    visitTime = models.DateTimeField()
    contactNumber = models.CharField(max_length=20)

    house = models.ForeignKey(House, on_delete=models.CASCADE)


