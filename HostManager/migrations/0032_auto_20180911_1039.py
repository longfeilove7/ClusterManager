# Generated by Django 2.1 on 2018-09-11 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0031_auto_20180911_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpowerstatus',
            name='checkTime',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
