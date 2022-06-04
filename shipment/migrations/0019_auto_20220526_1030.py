# Generated by Django 3.2.7 on 2022-05-26 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_company_vehicles_vehicle_busy'),
        ('shipment', '0018_auto_20220416_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholeshipment',
            name='real_vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Vehicle_to_Ship', to='accounts.company_vehicles'),
        ),
        migrations.AlterField(
            model_name='senderreceiver',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]