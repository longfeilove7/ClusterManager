from django.db import models
from macaddress.fields import MACAddressField #use django-macaddress


# Create your models here.


# class Hardware(models.Model):
#     hname = models.CharField(max_length=64)
#
#
class Type(models.Model):
    TypeName = models.CharField(max_length=32,null=True)

class OperatingSystem(models.Model):
    osName = models.CharField(max_length=32,null=True)
    osNumber = models.CharField(max_length=32,null=True)
    osBit = models.CharField(max_length=32,null=True)    

class Rooms(models.Model):
    roomName = models.CharField(max_length=32,null=True)
    cabinetNumber = models.CharField(max_length=32,null=True)
    floor = models.CharField(max_length=32,null=True)
    roomArea = models.CharField(max_length=32,null=True)

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
    roomName = models.ForeignKey(Rooms,on_delete=models.CASCADE,null=True)
    cabinetNO = models.CharField(max_length=32,null=True)
    bladeBoxNO = models.CharField(max_length=32,null=True)
    bladeNO = models.CharField(max_length=32,null=True)
    hostName = models.CharField(max_length=32,null=True)
    serviceIP = models.GenericIPAddressField(null=True)
    manageIP = models.GenericIPAddressField(null=True)
    storageIP = models.GenericIPAddressField(null=True)
    hardware = models.CharField(max_length=64,null=True)
    manufacturer = models.CharField(max_length=64,null=True) #制造商
    service = models.CharField(max_length=32,null=True)
    powerOnTime = models.DateTimeField(null=True)
    powerCycleTime = models.DateTimeField(null=True)
    powerOffTime = models.DateTimeField(null=True)
    checkOnline = models.CharField(max_length=32,null=True)
    runTime = models.DurationField(null=True)
    ipmiUser = models.CharField(max_length=64,null=True)
    ipmiPassword = models.CharField(max_length=64,null=True)
    clusterName = models.ForeignKey(Clusters,on_delete=models.CASCADE,null=True)
    powerStatus = models.CharField(max_length=1,default="0",null=True)
    pingStatus = models.CharField(max_length=1,default="0",null=True)
    monitorStatus = models.CharField(max_length=1,default="0",null=True)
    billingStatus = models.CharField(max_length=1,default="0",null=True)
    installStatus = models.CharField(max_length=1,default="0",null=True)

class HostMac(models.Model):
    host = models.ForeignKey(Host,on_delete=models.CASCADE) 
    ipmiMac = MACAddressField(null=True, blank=True,unique=True)
    pxeMac = MACAddressField(null=True, blank=True,unique=True)

class HostPartProperty(models.Model): #配件属性
    host = models.ForeignKey(Host,on_delete=models.CASCADE)
    cpuNum = models.IntegerField(null=True) #CPU个数
    cpuHz = models.CharField(max_length=64,null=True) #CPU主频
    cpuCore = models.IntegerField(null=True) #CPU总内核个数
    memory = models.IntegerField(null=True) #内存大小
    diskCapacity = models.IntegerField(null=True) #硬盘总容量
    diskNum = models.IntegerField(null=True) #硬盘数量
    diskRaid = models.CharField(max_length=64,null=True) #RAID类型
    networkAdapter =  models.IntegerField(null=True) #网卡数量

class HostHumanProperty(models.Model): #人物属性
    host = models.ForeignKey(Host,on_delete=models.CASCADE)
    vendor = models.CharField(max_length=32,null=True) #供应商
    remark = models.CharField(max_length=64,null=True) #备注
    purpose = models.CharField(max_length=64,null=True) #用途
    department = models.CharField(max_length=64,null=True) #使用部门
    principal = models.CharField(max_length=64,null=True) #负责人

class HostTimeProperty(models.Model): #时间属性
    host = models.ForeignKey(Host,on_delete=models.CASCADE)
    purchasingDate = models.DateTimeField(null=True) #采购时间
    acceptanceDate = models.DateTimeField(null=True) #验收时间
    warrentyPeriod = models.IntegerField(null=True) #保质期(月)
    warrentyStartDate = models.DateTimeField(null=True) #维保开始时间
    warrentyEndDate = models.DateTimeField(null=True) #维保结束时间
    useStartDate = models.DateTimeField(null=True) #申请使用时间
    useEndDate = models.DateTimeField(null=True) #结束使用时间
    lifeCycle = models.DateTimeField(null=True) #使用状态



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

class audit(models.Model):
    username = models.CharField(max_length=32,null=True)
    actionip = models.CharField(max_length=32,null=True)
    content = models.CharField(max_length=32,null=True)

