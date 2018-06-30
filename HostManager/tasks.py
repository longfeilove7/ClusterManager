# -*- coding: utf-8 -*-
#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
from celery import shared_task
from celery import task
import os, sys, time
import datetime

ipmiUser = "admin"
ipmiPassword = "admin"
@shared_task(name='HostManager.Tasks.powerStatus')
def powerStatus(ipmiHost):
    powerStatus = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power status"
    powerStatus = os.popen(powerStatus)
    returnRead =powerStatus.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.powerOn')
def powerOn(ipmiHost):
    powerOn = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power on"
    powerOn = os.popen(powerOn)
    returnRead = powerOn.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Up/On" in returnRead:                 
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail" 
    
@shared_task(name='HostManager.Tasks.powerOff')
def powerOff(ipmiHost):
    powerOff = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power off"
    powerOff = os.popen(powerOff)
    returnRead = powerOff.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.powerCycle')
def powerCycle(ipmiHost):
    powerCycle = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power cycle"
    powerCycle = os.popen(powerCycle)
    returnRead = powerCycle.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.powerReset')
def powerReset(ipmiHost):
    powerReset = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power reset"
    powerReset = os.popen(powerReset)
    returnRead = powerReset.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.powerSoft')
def powerSoft(ipmiHost):
    powerSoft = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power soft"
    powerSoft = os.popen(powerSoft)
    returnRead = powerSoft.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevPxe')
def bootdevPxe(ipmiHost):
    bootdevPxe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev pxe"
    bootdevPxe = os.popen(bootdevPxe)
    returnRead = bootdevPxe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevDisk')
def bootdevDisk(ipmiHost):
    bootdevDisk = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev disk"
    bootdevDisk = os.popen(bootdevDisk)
    returnRead = bootdevDisk.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevSafe')
def bootdevSafe(ipmiHost):
    bootdevSafe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev safe"
    bootdevSafe = os.popen(bootdevSafe)
    returnRead = bootdevSafe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevDiag')
def bootdevDiag(ipmiHost):
    bootdevDiag = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev diag"
    bootdevDiag = os.popen(bootdevDiag)
    returnRead = bootdevDiag.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevCdrom')
def bootdevCdrom(ipmiHost):
    bootdevCdrom = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev cdrom"
    bootdevCdrom = os.popen(bootdevCdrom)
    returnRead = bootdevCdrom.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"

@shared_task(name='HostManager.Tasks.bootdevBios')
def bootdevBios(ipmiHost):
    bootdevBios = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev bios"
    bootdevBios = os.popen(bootdevBios)
    returnRead = bootdevBios.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:         
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, " fail"