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

#定义全局变量用于存储页面当前用户信息
GLOBAL_VAR_USER = "0"

class ClassHost:
    def host_info(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'host_info.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })    

    def add_host(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'add_host.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })
        if request.method == 'POST':
            roomNO = request.POST.get('roomNO')
            cabinetNO = request.POST.get('cabinetNO')
            bladeBoxNO = request.POST.get('bladeBoxNO')
            bladeNO = request.POST.get('bladeNO')
            hostName = request.POST.get('hostName')
            serviceIP = request.POST.get('serviceIP')
            manageIP = request.POST.get('manageIP')
            storageIP = request.POST.get('storageIP')
            clusterName = request.POST.get('clusterName')
            hardware = request.POST.get('hardware')
            service = request.POST.get('service')
            powerOnTime = request.POST.get('powerOnTime')
            powerOffTime = request.POST.get('powerOffTime')
            checkOnline = request.POST.get('checkOnline')
            runTime = request.POST.get('runTime')
            ipmiUser = request.POST.get('ipmiUser')
            ipmiPassword = request.POST.get('ipmiPassword')
            models.Host.objects.create(
                roomNO=roomNO,
                cabinetNO=cabinetNO,
                bladeBoxNO=bladeBoxNO,
                bladeNO=bladeNO,
                hostName=hostName,
                serviceIP=serviceIP,
                manageIP=manageIP,
                storageIP=storageIP,
                clusterName_id=clusterName,
                hardware=hardware,
                service=service,
                powerOnTime=powerOnTime,
                powerOffTime=powerOffTime,
                checkOnline=checkOnline,
                runTime=runTime,
                ipmiUser=ipmiUser,
                ipmiPassword=ipmiPassword,
            )
            print(roomNO, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/add_host/')

    def host_del(request, nid):
        if request.method == 'POST':
            models.Host.objects.filter(id=nid).delete()
            return redirect('/add_host/')

    def host_edit(request, nid):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            cluster_list = models.Clusters.objects.all()
            return render(
                request, 'host_edit.html', {
                    'host_obj': host_obj,
                    'cluster_list': cluster_list,
                    'user_list': user_list
                })
        if request.method == 'POST':
            roomNO = request.POST.get('roomNO')
            cabinetNO = request.POST.get('cabinetNO')
            bladeBoxNO = request.POST.get('bladeBoxNO')
            bladeNO = request.POST.get('bladeNO')
            hostName = request.POST.get('hostName')
            serviceIP = request.POST.get('serviceIP')
            manageIP = request.POST.get('manageIP')
            storageIP = request.POST.get('storageIP')
            clusterName = request.POST.get('clusterName')
            hardware = request.POST.get('hardware')
            service = request.POST.get('service')
            ipmiUser = request.POST.get('ipmiUser')
            ipmiPassword = request.POST.get('ipmiPassword')
            models.Host.objects.filter(id=nid).update(
                roomNO=roomNO,
                cabinetNO=cabinetNO,
                bladeBoxNO=bladeBoxNO,
                bladeNO=bladeNO,
                hostName=hostName,
                serviceIP=serviceIP,
                manageIP=manageIP,
                storageIP=storageIP,
                clusterName_id=clusterName,
                hardware=hardware,
                service=service,
                ipmiUser=ipmiUser,
                ipmiPassword=ipmiPassword,
            )
            print(roomNO, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/add_host/')

    def power_history(request, nid):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            history_list = models.HostPowerHistory.objects.filter(host_id=nid)
            cluster_list = models.Clusters.objects.all()
            return render(
                request, 'power_history.html', {
                    'history_list': history_list,
                    'user_list': user_list,
                    'cluster_list': cluster_list
                })