# Generated by Django 3.2 on 2023-06-23 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_alter_repair_expect_time_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='repair_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repair_info', to='api.repair'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='type',
            field=models.CharField(choices=[('0', '智能推荐'), ('1', '已分派')], default='0', max_length=1),
        ),
    ]
