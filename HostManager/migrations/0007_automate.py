# Generated by Django 2.0.7 on 2018-07-12 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostManager', '0006_auto_20180706_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Automate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspectTime', models.CharField(max_length=32, null=True)),
            ],
        ),
    ]
