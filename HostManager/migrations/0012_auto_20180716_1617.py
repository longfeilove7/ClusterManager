# Generated by Django 2.0.7 on 2018-07-16 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0011_auto_20180716_1616'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HostHistory',
            new_name='HostPowerHistory',
        ),
    ]
