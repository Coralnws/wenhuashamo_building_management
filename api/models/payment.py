import uuid
from django.db import models
from django.utils import timezone

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=False, blank=False)
    createdTime = models.DateTimeField(default=timezone.now)
    rentalInfo = models.ForeignKey("RentalInfo", on_delete=models.CASCADE, null=False, blank=False)
    amount = models.IntegerField()

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
