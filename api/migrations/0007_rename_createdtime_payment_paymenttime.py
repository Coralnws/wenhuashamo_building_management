# Generated by Django 3.2 on 2023-06-18 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20230618_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='createdTime',
            new_name='paymentTime',
        ),
    ]
