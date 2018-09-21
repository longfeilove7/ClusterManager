# -*- coding: utf-8 -*-
#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
from celery import shared_task
from celery import task
import os, sys, time
import datetime
from django.utils import timezone
from HostManager import models
import pytz
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import PeriodicTasks
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import SolarSchedule
from django_celery_results.models import TaskResult


#查询电源状态,通过bind=true，给任务增加self参数，获得任务ID:self.request.id
@shared_task(bind=True, name='HostManager.Tasks.powerStatus')
def powerStatus(self,idName,ipmiHost, ipmiUser, ipmiPassword):
    powerStatus = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power status"
    powerStatus = os.popen(powerStatus)
    returnRead = powerStatus.read()
    print(returnRead)
    nowTime = timezone.now()
    if "on" in returnRead:        
        models.checkPowerOn.objects.create(
                checkTaskID=self.request.id,
                checkHost_id=idName,
                checkHostIP=ipmiHost,
                checkTime=nowTime,
                checkResult="on",                
            )        
        return idName,ipmiHost, nowTime, "on"
    elif "off" in returnRead:
        models.checkPowerOff.objects.create(
                checkTaskID=self.request.id,
                checkHost_id=idName,
                checkHostIP=ipmiHost,
                checkTime=nowTime,
                checkResult="off",                
            )
        return idName,ipmiHost, nowTime, "off"
    else:
        models.checkPowerFail.objects.create(
                checkTaskID=self.request.id,
                checkHost_id=idName,
                checkHostIP=ipmiHost,
                checkTime=nowTime,
                checkResult="fail",                
            )
        return idName,ipmiHost, nowTime, "fail"


#电源上电开机
@shared_task(name='HostManager.Tasks.powerOn')
def powerOn(ipmiHost, ipmiUser, ipmiPassword):
    powerOn = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power on"
    powerOn = os.popen(powerOn)
    returnRead = powerOn.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Up/On" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#电源下电硬关机
@shared_task(name='HostManager.Tasks.powerOff')
def powerOff(ipmiHost, ipmiUser, ipmiPassword):
    powerOff = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power off"
    powerOff = os.popen(powerOff)
    returnRead = powerOff.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#电源硬重起
@shared_task(name='HostManager.Tasks.powerCycle')
def powerCycle(ipmiHost, ipmiUser, ipmiPassword):
    powerCycle = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power cycle"
    powerCycle = os.popen(powerCycle)
    returnRead = powerCycle.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Cycle" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#电源软重起
@shared_task(name='HostManager.Tasks.powerReset')
def powerReset(ipmiHost, ipmiUser, ipmiPassword):
    powerReset = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power reset"
    powerReset = os.popen(powerReset)
    returnRead = powerReset.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#电源软关机
@shared_task(name='HostManager.Tasks.powerSoft')
def powerSoft(ipmiHost, ipmiUser, ipmiPassword):
    powerSoft = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " power soft"
    powerSoft = os.popen(powerSoft)
    returnRead = powerSoft.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置PXE启动
@shared_task(name='HostManager.Tasks.bootdevPxe')
def bootdevPxe(ipmiHost, ipmiUser, ipmiPassword):
    bootdevPxe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev pxe"
    bootdevPxe = os.popen(bootdevPxe)
    returnRead = bootdevPxe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置磁盘启动
@shared_task(name='HostManager.Tasks.bootdevDisk')
def bootdevDisk(ipmiHost, ipmiUser, ipmiPassword):
    bootdevDisk = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev disk"
    bootdevDisk = os.popen(bootdevDisk)
    returnRead = bootdevDisk.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置安全模式启动
@shared_task(name='HostManager.Tasks.bootdevSafe')
def bootdevSafe(ipmiHost, ipmiUser, ipmiPassword):
    bootdevSafe = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev safe"
    bootdevSafe = os.popen(bootdevSafe)
    returnRead = bootdevSafe.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置诊断启动
@shared_task(name='HostManager.Tasks.bootdevDiag')
def bootdevDiag(ipmiHost, ipmiUser, ipmiPassword):
    bootdevDiag = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev diag"
    bootdevDiag = os.popen(bootdevDiag)
    returnRead = bootdevDiag.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置CD-ROM启动
@shared_task(name='HostManager.Tasks.bootdevCdrom')
def bootdevCdrom(ipmiHost, ipmiUser, ipmiPassword):
    bootdevCdrom = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev cdrom"
    bootdevCdrom = os.popen(bootdevCdrom)
    returnRead = bootdevCdrom.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#设置BIOS启动
@shared_task(name='HostManager.Tasks.bootdevBios')
def bootdevBios(ipmiHost, ipmiUser, ipmiPassword):
    bootdevBios = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " chassis bootdev bios"
    bootdevBios = os.popen(bootdevBios)
    returnRead = bootdevBios.read()
    print(returnRead)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if "Down/Off" in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"


#获取SDR信息
@shared_task(name='HostManager.Tasks.inspectSdr')
def inspectSdr(ipmiHost, ipmiUser, ipmiPassword):
    nowTime = datetime.datetime.now()
    print(type(nowTime))
    inspectTime = nowTime.strftime('%Y-%m-%d-%H-%M-%S')
    inspectSdr = "ipmitool -H " + ipmiHost + " -U " + ipmiUser + " -P " + ipmiPassword + " sdr  >>" + "inspect/" + inspectTime + ".csv"
    inspectTitle = "echo IPMI:" + ipmiHost + "  Time:" + inspectTime + ">>" + "inspect/" + inspectTime + ".csv"
    os.popen(inspectTitle)
    inspectSdr = os.popen(inspectSdr)
    returnRead = inspectSdr.read()
    print(returnRead)
    nowTime = nowTime.strftime('%Y-%m-%d %H:%M:%S')
    if "Unable" not in returnRead:
        return ipmiHost, nowTime, "success"
    else:
        return ipmiHost, nowTime, "fail"

#ping测试
@task(name='HostManager.Tasks.fping', bind=True)
def fping(self):
    #从数据库获得IP地址列表
    db_list = models.Host.objects.values_list("serviceIP", flat=True)
    #确认一下获取到的IP个数
    print(len(db_list))
    result_list = []
    alive_list = []
    dead_list = []
    #使用str = ' '.join(list)快速将列表转成字符串（以空格分割）
    serviceIP = ' '.join(db_list)
    db_list = serviceIP.split(' ')
    #确认一下转化成字符串的IP个数
    print(len(db_list))
    fping = "fping " + serviceIP
    fping = os.popen(fping)
    returnRead = fping.read()
    # print("*********************************")
    # print(returnRead)
    # print(type(returnRead))
    # print("*********************************")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    returnRead_list = returnRead.split('\n')
    # print(returnRead_list)    
    for key in returnRead_list:       
        #正常return会终止循环，所以不能使用循环return返回结果。
        if "alive" in key:
            #self.request.id,获取任务ID，根据ID将结果写入数据库。
            #遍历key，将含有alive的重建一个列表
            alive_list.append(key)            
        elif "unreachable" in key:
            #遍历key，将含有unreachable的重建一个列表
            dead_list.append(key)
        else:
            #self.request.id,获取任务ID，根据ID将结果写入数据库。
            print("***************************************")
    result_list.append(alive_list)
    result_list.append(dead_list)    
    return result_list

@shared_task
def test(arg):
    print('world')