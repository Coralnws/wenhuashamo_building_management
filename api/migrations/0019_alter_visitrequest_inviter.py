# Generated by Django 3.2 on 2023-06-20 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_visitrequest_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitrequest',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inviter', to=settings.AUTH_USER_MODEL),
        ),
    ]
