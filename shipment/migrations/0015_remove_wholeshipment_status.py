# Generated by Django 3.2.7 on 2022-03-19 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0014_alter_wholeshipment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholeshipment',
            name='status',
        ),
    ]
