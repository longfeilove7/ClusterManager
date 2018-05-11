from django.db import models

# Create your models here.


# class Hardware(models.Model):
#     hname = models.CharField(max_length=64)
#
#
class Groups(models.Model):
    hostGroup = models.CharField(max_length=32)


# class Services(models.Model):
#     service = models.CharField(max_length=32)


class Host(models.Model):
    roomNO = models.CharField(max_length=32)
    cabinetNO = models.CharField(max_length=32)
    bladeBoxNO = models.CharField(max_length=32)
    bladeNO = models.CharField(max_length=32)
    hostName = models.CharField(max_length=32)
    serviceIP = models.GenericIPAddressField()
    manageIP = models.GenericIPAddressField()
    storageIP = models.GenericIPAddressField()
    hardware = models.CharField(max_length=64)
    service = models.CharField(max_length=32)
    powerOnTime = models.CharField(max_length=32)
    powerOffTime = models.CharField(max_length=32)
    checkOnline = models.CharField(max_length=32)
    runTime = models.CharField(max_length=32)
    hostGroup = models.ForeignKey(Groups,on_delete=models.CASCADE)


class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


