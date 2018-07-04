from django.db import models

# Create your models here.


# class Hardware(models.Model):
#     hname = models.CharField(max_length=64)
#
#
class Clusters(models.Model):
    hostCluster = models.CharField(max_length=32)


# class Services(models.Model):
#     service = models.CharField(max_length=32)


class Host(models.Model):
    roomNO = models.CharField(max_length=32,null=True)
    cabinetNO = models.CharField(max_length=32,null=True)
    bladeBoxNO = models.CharField(max_length=32,null=True)
    bladeNO = models.CharField(max_length=32,null=True)
    hostName = models.CharField(max_length=32,null=True)
    serviceIP = models.GenericIPAddressField(null=True)
    manageIP = models.GenericIPAddressField(null=True)
    storageIP = models.GenericIPAddressField(null=True)
    hardware = models.CharField(max_length=64,null=True)
    service = models.CharField(max_length=32,null=True)
    powerOnTime = models.DateTimeField(null=True)
    powerOffTime = models.DateTimeField(null=True)
    checkOnline = models.CharField(max_length=32,null=True)
    runTime = models.CharField(max_length=32,null=True)
    ipmiUser = models.CharField(max_length=64,null=True)
    ipmiPassword = models.CharField(max_length=64,null=True)
    hostCluster = models.ForeignKey(Clusters,on_delete=models.CASCADE)


class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


