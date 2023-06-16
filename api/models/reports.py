import uuid
from django.db import models
from django.utils import timezone

#申诉
class Report(models.Model):
    CATEGORY = (
        (0, '-'),
        (1, '学者申诉'),
        (2, '学术成果申诉'),
    )

    STATUS = (
        (0, 'Pending'),
        (1, 'Reject'),
        (2, 'Accept')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    reportArticle_id = models.CharField(max_length=40 ,blank=True,null=True)
    reportScholar_id = models.CharField(max_length=40 ,blank=True,null=True)
    category = models.IntegerField(choices=CATEGORY,default=0)
    result = models.IntegerField(choices=STATUS, default=0)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

class ReviewReport(models.Model):
    CATEGORY = (
        (1, '垃圾内容'),
        (2, '色情内容'),
        (3, '非法活动'),
        (4, '侵犯版权'),
        (5, '骚扰、欺凌和威胁'),
        (6, '仇恨言论'),
        (7, '暴力内容'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    reportReview = models.ForeignKey("Review", on_delete=models.CASCADE, null=True, blank=True)
    category = models.IntegerField(choices=CATEGORY,default = 0)
    result = models.BooleanField(default=False)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)