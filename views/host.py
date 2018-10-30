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

    def hostPower(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            return render(request, 'host_power.html', {
                'user_list': user_list
            })


    def hostBoot(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            return render(request, 'host_boot.html', {
                'user_list': user_list
            })

    def hostRemote(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            return render(request, 'host_remote.html', {
                'user_list': user_list
            })

    def add_host(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            cluster_list = models.Clusters.objects.all()
            return render(request, 'add_host.html', {
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

    def hostInfoQuery(request):
        info_list = models.Host.objects.all()
        limit = request.GET.get('limit')  # how many items per page
        #print("the limit :"+limit)
        offset = request.GET.get('offset')  # how many items in total in the DB
        #print("the offset :",offset)
        sort_column = request.GET.get('sort')  # which column need to sort
        if sort_column:
            print("the sort_column :" + sort_column)
            order = request.GET.get('order')  # ascending or descending
            print("the order :" + order)
        info_list_count = len(info_list)
        print(info_list_count)
        if not offset:
            offset = 0
        if not limit:
            limit = 10  # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(info_list, limit)  # 利用Django的Painator开始做分页
        page = int(int(offset) / int(limit) + 1)
        print("the page:", page)
        info_list_dict = {
            "total": info_list_count,
            "rows": []
        }  # 必须带有rows和total这2个key，total表示总数，rows表示每行的内容
        users_timezone = pytz.timezone('Asia/Shanghai')
        for item in pageinator.page(page):
            if item.powerOnTime:
                    print(item.powerOnTime)
                    item.powerOnTime = item.powerOnTime.astimezone(
                        users_timezone).replace(tzinfo=None)
                    print(item.powerOnTime)
            if item.powerOffTime:
                item.powerOffTime = item.powerOffTime.astimezone(users_timezone).replace(tzinfo=None)

            info_list_dict['rows'].append({
                "id":
                item.id,
                "roomNO":
                item.roomNO,
                "cabinetNO":
                item.cabinetNO,
                "bladeBoxNO":
                item.bladeBoxNO,
                "bladeNO":
                item.bladeNO,
                "hostName":
                item.hostName,
                "serviceIP":
                item.serviceIP,
                "manageIP":
                item.manageIP,
                "storageIP":
                item.storageIP,
                "clusterName":
                item.clusterName.clusterName,
                "hardware":
                item.hardware,
                "service":
                item.service,
                "powerOnTime":
                str(item.powerOnTime),
                "powerOffTime":
                str(item.powerOffTime),
                "runTime":
                str(item.runTime),
                "powerStatus":
                item.powerStatus
            })
        info_list_json = json.dumps(info_list_dict)
        return HttpResponse(
            info_list_json,
            content_type="application/json",
        )

    def HostDelete(request):
        if request.method == 'POST':
            ipmiID = request.POST.get('allValue')
            models.Host.objects.filter(id=ipmiID).delete()
            dictDelete = [ipmiID, 1]
            data = json.dumps(dictDelete).encode()
            return HttpResponse(data)

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

    def batchHostDelete(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print("the allValue: ", allValue, type(allValue))
            listAllValue = json.loads(allValue)
            print("the listAllValue: ", listAllValue, type(listAllValue))
            listDelete = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).delete()
                dictDelete = [ipmiID, 1]
                listDelete.append(dictDelete)
            data = json.dumps(listDelete).encode()
            return HttpResponse(data)

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