# Generated by Django 3.2 on 2023-06-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20230622_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalinfo',
            name='contract_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
