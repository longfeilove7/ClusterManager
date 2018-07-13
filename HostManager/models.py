from django.db import models

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
    powerOffTime = models.DateTimeField(null=True)
    checkOnline = models.CharField(max_length=32,null=True)
    runTime = models.CharField(max_length=32,null=True)
    ipmiUser = models.CharField(max_length=64,null=True)
    ipmiPassword = models.CharField(max_length=64,null=True)
    clusterName = models.ForeignKey(Clusters,on_delete=models.CASCADE)

class Automate(models.Model):
    inspectTime =models.CharField(max_length=32,null=True)
    
    


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

