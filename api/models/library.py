from django.db import models


class Library(models.Model):
    description = models.CharField(max_length=200)
    solution = models.TextField()
