# Generated by Django 3.2.5 on 2023-06-26 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_library_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='contactName',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='real_name',
            field=models.CharField(max_length=150),
        ),
    ]