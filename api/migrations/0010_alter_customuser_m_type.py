# Generated by Django 3.2.5 on 2023-06-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20230618_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='m_type',
            field=models.CharField(max_length=10),
        ),
    ]