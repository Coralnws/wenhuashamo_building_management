# Generated by Django 3.2.5 on 2023-06-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20230625_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='library_status',
            field=models.BooleanField(default=False),
        ),
    ]
