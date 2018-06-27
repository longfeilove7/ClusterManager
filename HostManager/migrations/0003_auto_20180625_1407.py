# Generated by Django 2.0.6 on 2018-06-25 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0002_auto_20180625_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='bladeBoxNO',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='bladeNO',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='cabinetNO',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='checkOnline',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='hardware',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='hostName',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='manageIP',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='powerOffTime',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='powerOnTime',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='roomNO',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='runTime',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='service',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='serviceIP',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='storageIP',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
