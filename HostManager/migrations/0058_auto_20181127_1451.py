# Generated by Django 2.1.3 on 2018-11-27 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0057_rooms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='floorName',
            new_name='floor',
        ),
    ]
