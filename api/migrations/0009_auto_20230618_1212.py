# Generated by Django 3.2.5 on 2023-06-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20230618_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalinfo',
            old_name='lastPay',
            new_name='paidManagementDate',
        ),
        migrations.RemoveField(
            model_name='house',
            name='rentalInfo',
        ),
        migrations.RemoveField(
            model_name='rentalinfo',
            name='fee',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_change_password',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rentalinfo',
            name='management_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rentalinfo',
            name='paidRentalDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='rentalinfo',
            name='rental_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='house',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
