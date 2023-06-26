# Generated by Django 3.2.5 on 2023-06-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_repair_library_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='staff_contact',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='library',
            name='staff_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='library',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='library',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]