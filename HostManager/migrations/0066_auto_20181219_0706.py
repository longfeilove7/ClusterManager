# Generated by Django 2.1.4 on 2018-12-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0065_auto_20181219_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installsystemhistory',
            name='installSystemResult',
            field=models.CharField(default='0', max_length=1),
        ),
    ]
