# Generated by Django 2.0.6 on 2018-06-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='ipmiPassword',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='ipmiUser',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
