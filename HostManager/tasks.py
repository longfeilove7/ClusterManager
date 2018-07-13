# -*- coding: utf-8 -*-
#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
from celery import shared_task
from celery import task
import os, sys, time
import datetime
from HostManager import models

#ipmiUser = "admin"
#ipmiPassword = "admin"
@shared_task(name='HostManager.Tasks.powerStatus')
def powerStatus(ipmiHost,ipmiUser,ipmiPassword):
    powerStatus = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power status"
    powerStatus = os.popen(powerStatus)
    returnRead =powerStatus.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.powerOn')
def powerOn(ipmiHost,ipmiUser,ipmiPassword):
    powerOn = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power on"
    powerOn = os.popen(powerOn)
    returnRead = powerOn.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Up/On" in returnRead:                 
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail" 
    
@shared_task(name='HostManager.Tasks.powerOff')
def powerOff(ipmiHost,ipmiUser,ipmiPassword):
    powerOff = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power off"
    powerOff = os.popen(powerOff)
    returnRead = powerOff.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.powerCycle')
def powerCycle(ipmiHost,ipmiUser,ipmiPassword):
    powerCycle = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power cycle"
    powerCycle = os.popen(powerCycle)
    returnRead = powerCycle.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Cycle" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.powerReset')
def powerReset(ipmiHost,ipmiUser,ipmiPassword):
    powerReset = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power reset"
    powerReset = os.popen(powerReset)
    returnRead = powerReset.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.powerSoft')
def powerSoft(ipmiHost,ipmiUser,ipmiPassword):
    powerSoft = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power soft"
    powerSoft = os.popen(powerSoft)
    returnRead = powerSoft.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevPxe')
def bootdevPxe(ipmiHost,ipmiUser,ipmiPassword):
    bootdevPxe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev pxe"
    bootdevPxe = os.popen(bootdevPxe)
    returnRead = bootdevPxe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevDisk')
def bootdevDisk(ipmiHost,ipmiUser,ipmiPassword):
    bootdevDisk = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev disk"
    bootdevDisk = os.popen(bootdevDisk)
    returnRead = bootdevDisk.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevSafe')
def bootdevSafe(ipmiHost,ipmiUser,ipmiPassword):
    bootdevSafe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev safe"
    bootdevSafe = os.popen(bootdevSafe)
    returnRead = bootdevSafe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevDiag')
def bootdevDiag(ipmiHost,ipmiUser,ipmiPassword):
    bootdevDiag = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev diag"
    bootdevDiag = os.popen(bootdevDiag)
    returnRead = bootdevDiag.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevCdrom')
def bootdevCdrom(ipmiHost,ipmiUser,ipmiPassword):
    bootdevCdrom = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev cdrom"
    bootdevCdrom = os.popen(bootdevCdrom)
    returnRead = bootdevCdrom.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.bootdevBios')
def bootdevBios(ipmiHost,ipmiUser,ipmiPassword):
    bootdevBios = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev bios"
    bootdevBios = os.popen(bootdevBios)
    returnRead = bootdevBios.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@shared_task(name='HostManager.Tasks.inspectSdr')
def inspectSdr(ipmiHost,ipmiUser,ipmiPassword):
    nowTime = datetime.datetime.now()    
    print(type(nowTime))
    inspectTime = nowTime.strftime('%Y-%m-%d-%H-%M-%S')
    inspectSdr = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " sdr  >>" + "inspect/"+ inspectTime + ".csv"
    inspectTitle = "echo IPMI:" + ipmiHost + "  Time:" + inspectTime  + ">>" + "inspect/"+ inspectTime + ".csv"
    os.popen(inspectTitle)   
    inspectSdr = os.popen(inspectSdr)
    returnRead = inspectSdr.read()
    print(returnRead)  
    nowTime = nowTime.strftime('%Y-%m-%d %H:%M:%S')    
    if "Unable" not in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

@task(name='HostManager.Tasks.fping')
def fping(ipHost,ipmiUser,ipmiPassword):
    # db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
    # print(db_dict)
    # return(db_dict)    
    fping = "fping " + ipHost
    fping = os.popen(fping)
    returnRead = fping.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "alive" in returnRead:
        return   ipHost, nowTime, "alive"
    else:
        return   ipHost, nowTime, "dead"  