# Generated by Django 3.2 on 2023-06-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_createdtime_payment_paymenttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='m_status',
            field=models.CharField(choices=[('1', '可用'), ('0', '不可用')], default='1', max_length=10),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='company',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='contactName',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='contactNumber',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='real_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
