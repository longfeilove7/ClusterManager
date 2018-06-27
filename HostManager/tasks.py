# -*- coding: utf-8 -*-
#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
from celery import shared_task
from celery import task
import os, sys, time
# import requests
# from lxml.etree import fromstring
# import json

#from celery import Celery #单独测试使用

#app = Celery('tasks', broker='pyamqp://guest@localhost//') #单独测试使用

# 自定义要执行的task任务
@task(name='HostManager.Tasks.printHello')
def printHello():
    #file = os.popen("cmd.exe /c" + "C:\\Users\\ghost\\Documents\\GitHub\\ClusterManager\\HostManager\\cmd.bat")
    #print(file.read())
    return 'hello celery and django...'

@shared_task(name='HostManager.Tasks.add')
def add(x, y):
    return x + y

@shared_task(name='HostManager.Tasks.mul')
def mul(x, y):
    return x * y

@shared_task(name='HostManager.Tasks.xsum')
def xsum(numbers):
    return sum(numbers)

@shared_task(name='HostManager.Tasks.sayHello')
def sayHello():
    print('hello ...')
    time.sleep(2)
    print('world ...')
    #return 'hello celery and django...'

# def index(request):
#     return render(request, 'host_info.html')

# def getIpmiIP(request):
#     ipmiHost = request.GET['manageIP']
#     print(ipmiHost)
#     #b = request.GET['b']
#     #a = int(a)
#     #b = int(b)
#     #return HttpResponse(str(a+b))

ipmiHost = "10.18.10.10"
ipmiUser = "admin"
ipmiPassword = "admin"
# API_url='http://www.xxxxxxxxxxxxxx_ajax.htm'  ##可能url并不会包含ajax关键字 

# def get_stores_info(self,page):
#     data={'pages':page} ##需要尝试，可能有些参数是冗余的
#     response=requests.post(self.API_url,data=data)
#     return response.json()
# ##定义function 执行并调用：
# def run(self):
#     page=100
#     for commodityid in range(page):
#             data=self.get_stores_info(page)

#             print(data)

#celery can not use global 
# powerStatus = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power status"
# powerOn = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power on"
# powerOff = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power off"
# powerCycle = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power cycle"
# powerReset = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power reset"
# powerDiag = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power diag"
# powerSoft = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power soft"

@shared_task(name='HostManager.Tasks.powerStatus')
def powerStatus():
    powerStatus = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power status"
    powerStatus = os.popen(powerStatus)
    print(powerStatus.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.powerOn')
def powerOn():
    powerOn = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power on"
    powerOn = os.popen(powerOn)
    print(powerOn.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.powerOff')
def powerOff():
    powerOff = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power off"
    powerOff = os.popen(powerOff)
    print(powerOff.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.powerCycle')
def powerCycle():
    powerCycle = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power cycle"
    powerCycle = os.popen(powerCycle)
    print(powerCycle.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.powerReset')
def powerReset():
    powerReset = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power reset"
    powerReset = os.popen(powerReset)
    print(powerReset.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.powerSoft')
def powerSoft():
    powerSoft = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power soft"
    powerSoft = os.popen(powerSoft)
    print(powerSoft.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevPxe')
def bootdevPxe():
    bootdevPxe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev pxe"
    bootdevPxe = os.popen(bootdevPxe)
    print(bootdevPxe.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevDisk')
def bootdevDisk():
    bootdevDisk = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev disk"
    bootdevDisk = os.popen(bootdevDisk)
    print(bootdevDisk.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevSafe')
def bootdevSafe():
    bootdevSafe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev safe"
    bootdevSafe = os.popen(bootdevSafe)
    print(bootdevSafe.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevDiag')
def bootdevDiag():
    bootdevDiag = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev diag"
    bootdevDiag = os.popen(bootdevDiag)
    print(bootdevDiag.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevCdrom')
def bootdevCdrom():
    bootdevCdrom = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev cdrom"
    bootdevCdrom = os.popen(bootdevCdrom)
    print(bootdevCdrom.read())
    print(ipmiHost)
    return 'ok'

@shared_task(name='HostManager.Tasks.bootdevBios')
def bootdevBios():
    bootdevBios = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev bios"
    bootdevBios = os.popen(bootdevBios)
    print(bootdevBios.read())
    print(ipmiHost)
    return 'ok'