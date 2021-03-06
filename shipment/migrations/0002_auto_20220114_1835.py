# Generated by Django 3.2.7 on 2022-01-14 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholeshipment',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Assign_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wholeshipment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.basicuser'),
            preserve_default=False,
        ),
    ]
