# Generated by Django 3.2.5 on 2023-06-16 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentalinfo',
            old_name='nextDeadline',
            new_name='nextManagementFeeDeadline',
        ),
        migrations.RenameField(
            model_name='rentalinfo',
            old_name='unpaid',
            new_name='unpaid_management',
        ),
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('0', '暂无'), ('1', '租赁费'), ('2', '物业费')], default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='rentalinfo',
            name='nextRentalDeadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='rentalinfo',
            name='unpaid_rental',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='repair',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repair_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='repair',
            name='solver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repair_solver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='repair',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repair_staff', to=settings.AUTH_USER_MODEL),
        ),
    ]