import uuid
from django.utils import timezone
from django.db import models


class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.CharField(max_length=150,null=True, blank=True)
    articleName=models.CharField(max_length=150,null=True, blank=True)
    belongTo = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

