# Generated by Django 2.1 on 2018-09-11 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0033_auto_20180911_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkpowerstatus',
            old_name='checkID',
            new_name='checkHostID',
        ),
        migrations.RenameField(
            model_name='checkpowerstatus',
            old_name='checkIP',
            new_name='checkHostIP',
        ),
        migrations.AddField(
            model_name='checkpowerstatus',
            name='checkTaskID',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
