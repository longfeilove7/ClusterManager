# Generated by Django 2.1 on 2018-09-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0037_auto_20180911_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkpowerstatus',
            name='checkHost',
        ),
        migrations.AddField(
            model_name='checkpowerstatus',
            name='checkHostID',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
