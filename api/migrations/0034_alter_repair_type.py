# Generated by Django 3.2 on 2023-06-24 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20230624_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='type',
            field=models.CharField(blank=True, choices=[('0', '无'), ('1', '水'), ('2', '电'), ('3', '机械')], default='0', max_length=10, null=True),
        ),
    ]
