# Generated by Django 3.2.7 on 2022-03-19 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0010_alter_status_shipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wholeshipment',
            name='status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.status'),
        ),
    ]
