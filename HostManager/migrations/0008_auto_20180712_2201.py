# Generated by Django 2.0.7 on 2018-07-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0007_automate'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusters',
            name='contactEmail',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='contactPerson',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='contactPhone',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='contactQQ',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='contactWeicat',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='customerName',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='clusters',
            name='deviceNumber',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='clusters',
            name='hostCluster',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
