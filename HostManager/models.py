from django.db import models
from macaddress.fields import MACAddressField #use django-macaddress
# Create your models here.


# class Hardware(models.Model):
#     hname = models.CharField(max_length=64)
#
#
class Clusters(models.Model):
    clusterName = models.CharField(max_length=32,null=True)
    deviceNumber = models.CharField(max_length=32,null=True)  
    customerName = models.CharField(max_length=32,null=True)
    contactPerson = models.CharField(max_length=32,null=True)
    contactPhone = models.CharField(max_length=32,null=True)
    contactEmail = models.EmailField(max_length=32,null=True)
    contactQQ = models.CharField(max_length=32,null=True)
    contactWeicat = models.CharField(max_length=32,null=True)



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
    powerCycleTime = models.DateTimeField(null=True)
    powerOffTime = models.DateTimeField(null=True)
    checkOnline = models.CharField(max_length=32,null=True)
    runTime = models.DurationField(null=True)
    ipmiUser = models.CharField(max_length=64,null=True)
    ipmiPassword = models.CharField(max_length=64,null=True)
    clusterName = models.ForeignKey(Clusters,on_delete=models.CASCADE)
    powerStatus = models.CharField(max_length=1,default="0")
    monitorStatus = models.CharField(max_length=1,default="0")
    billingStatus = models.CharField(max_length=1,default="0")
    installStatus = models.CharField(max_length=1,default="0")

class HostMac(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE) 
    ipmiMac = MACAddressField(null=True, blank=True,unique=True)
    pxeMac = MACAddressField(null=True, blank=True,unique=True)

class HostPowerHistory(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE) 
    powerOnTimeHistory = models.DateTimeField(null=True)
    powerCycleTimes = models.IntegerField(default="0")
    powerOffTimeHistory = models.DateTimeField(null=True)
    runTimeHistory = models.DurationField(null=True)

class HostCountPowerHistory(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE)   
    countRunTimeHistory = models.DurationField(null=True)    

class checkPowerOn(models.Model):
    checkTaskID = models.CharField(max_length=255,null=True)
    checkHost = models.ForeignKey(Host,null=True,on_delete=models.CASCADE) 
    checkHostIP = models.GenericIPAddressField(null=True)
    checkTime = models.DateTimeField(null=True)
    checkResult =  models.CharField(max_length=32,null=True)   

class checkPowerOff(models.Model):
    checkTaskID = models.CharField(max_length=255,null=True)
    checkHost = models.ForeignKey(Host,null=True,on_delete=models.CASCADE) 
    checkHostIP = models.GenericIPAddressField(null=True)
    checkTime = models.DateTimeField(null=True)
    checkResult =  models.CharField(max_length=32,null=True)   
    
class checkPowerFail(models.Model):
    checkTaskID = models.CharField(max_length=255,null=True)
    checkHost = models.ForeignKey(Host,null=True,on_delete=models.CASCADE) 
    checkHostIP = models.GenericIPAddressField(null=True)
    checkTime = models.DateTimeField(null=True)
    checkResult =  models.CharField(max_length=32,null=True)   

class Automate(models.Model):
    inspectTime =models.CharField(max_length=32,null=True)
    
class Billing(models.Model):
    clusterName = models.ForeignKey(Clusters,on_delete=models.CASCADE)
    billingNumber = models.CharField(max_length=32,null=True)
    billingPrice = models.CharField(max_length=32,null=True)  
    billingStartTime = models.CharField(max_length=32,null=True)
    billingStopTime = models.CharField(max_length=32,null=True)

class BillingHistory(models.Model):
    clusterName = models.CharField(max_length=32,null=True)
    deviceNumber = models.CharField(max_length=32,null=True)
    billingNumber = models.CharField(max_length=32,null=True)
    billingPrice = models.CharField(max_length=32,null=True)  
    billingStartTime = models.CharField(max_length=32,null=True)
    billingStopTime = models.CharField(max_length=32,null=True)
    billingNowTime = models.CharField(max_length=32,null=True)
    billingCount = models.CharField(max_length=32,null=True)

class InstallSystemHistory(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE) 
    installStartTimeHistory = models.DateTimeField(null=True)
    installEndTimeHistory = models.DateTimeField(null=True)
    installRunTimeHistory = models.DurationField(null=True)
    installSystemStatus = models.CharField(max_length=1,default="0")

class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10, unique=True,
                            default="question")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

