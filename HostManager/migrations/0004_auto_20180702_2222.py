# Generated by Django 2.0.6 on 2018-07-02 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0003_auto_20180625_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='powerOffTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='powerOnTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='runTime',
            field=models.DateTimeField(null=True),
        ),
    ]
