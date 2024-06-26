# Generated by Django 3.2 on 2023-06-17 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_customuser_m_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_pay', to='api.house'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='rentalInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rentalinfo_pay', to='api.rentalinfo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_pay', to='api.tenant'),
        ),
    ]
