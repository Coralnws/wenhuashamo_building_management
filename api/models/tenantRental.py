import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date

class TenantRental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey("House",on_delete=models.CASCADE, null=False, blank=False)
    rental = models.ForeignKey("RentalInfo",on_delete=models.CASCADE, null=False, blank=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)