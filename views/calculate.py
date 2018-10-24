"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
from rest_framework_swagger.views import get_swagger_view
from django.db.models import Count, Max, Avg, Min, Sum, F, Q, FloatField
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseBadRequest
from HostManager import models
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import PeriodicTasks
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import SolarSchedule
from django_celery_results.models import TaskResult
from celery import shared_task
from celery import task
from HostManager import tasks
from HostManager import periodic_tasks
from celery import Celery
from celery.schedules import crontab
from celery import app
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import pytz
from django.utils import timezone
from itertools import chain
#import django_excel as excel
from HostManager.models import Question, Choice, Host, Clusters
from django import forms
# json can't service datetime format,so use the djangojsonencoder
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from decimal import *
#import os, sys, commands
import xmlrpc.server
import xmlrpc.client
# Create your views here.

class ClassCountCalculate():
    def runTimeCalculate(ipmiID, powerOnTime, powerOffTime):
        """"""
        db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
        db_tuple = models.Host.objects.filter().values_list()[0]
        print(db_dict)
        print(db_tuple)
        print(db_dict['powerOnTime'])
        print(db_dict['powerOffTime'])
        print(powerOffTime)
        #offset-naive是不含时区的类型，而offset-aware是有时区类型
        runTime = datetime.datetime.strptime(
            powerOffTime, '%Y-%m-%d %H:%M:%S'
        ) - db_dict['powerOnTime'].replace(tzinfo=None) - datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=8,
            weeks=0)
        print(runTime)
        models.Host.objects.filter(id=ipmiID).update(runTime=runTime)
        models.HostPowerHistory.objects.filter(
            powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                runTimeHistory=runTime, )
        return (runTime)

    def countRunTimeCalculate(ipmiID):
        """"""
        # to calculate the all runtimehistory
        db_list = models.HostPowerHistory.objects.filter(
            host_id=ipmiID).values("host_id", "runTimeHistory")
        print(db_list)
        listRunTimeHistory = []
        #遍历列表获得内部字典
        for key_dict in db_list:
            #获取单条字典的对应值
            host_id = key_dict['host_id']
            runTimeHistory = key_dict['runTimeHistory']
            # set the not null to a list
            if runTimeHistory is not None:
                #print(runTimeHistory)
                listRunTimeHistory.append(runTimeHistory)
        #print(listRunTimeHistory)
        #print(type(listRunTimeHistory))
        countRunTimeHistory = datetime.timedelta(0, 0)
        for x in listRunTimeHistory:
            countRunTimeHistory += x
        # models.Host.objects.filter(id=ipmiID).update(runTime=str(runTime), )
        # models.HostPowerHistory.objects.filter(
        #     powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
        #         runTimeHistory= runTime )
        return (countRunTimeHistory)
