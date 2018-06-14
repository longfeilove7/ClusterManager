# -*- coding: utf-8 -*-
#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
from celery import shared_task
from celery import task
import os, sys

#from celery import Celery #单独测试使用

#app = Celery('tasks', broker='pyamqp://guest@localhost//') #单独测试使用

# 自定义要执行的task任务
@task(name='HostManager.Tasks.printHello')
def printHello():
    file = os.popen("cmd.exe /c" + "C:\\Users\\ghost\\Documents\\GitHub\\ClusterManager\\HostManager\\cmd.bat")
    print(file.read())

@shared_task(name='HostManager.Tasks.add')
def add(x, y):
    return x + y


@shared_task(name='HostManager.Tasks.mul')
def mul(x, y):
    return x * y


@shared_task(name='HostManager.Tasks.xsum')
def xsum(numbers):
    return sum(numbers)