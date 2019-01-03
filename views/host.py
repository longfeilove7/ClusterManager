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
from django.contrib.auth.decorators import login_required

# Create your views here.


class ClassHost:
    @login_required
    def host_info(request):
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            room_list = models.Rooms.objects.all()
            return render(request, 'host_info.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'room_list': room_list
            })

    @login_required
    def hostDetail(request, nid):
        if request.method == 'GET':
            obj = models.Host.objects.filter(id=nid)
            history_list = models.HostPowerHistory.objects.filter(host_id=nid)
            cluster_list = models.Clusters.objects.all()
            room_list = models.Rooms.objects.all()
            return render(request, 'host_detail.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                 'history_list': history_list,
                 'room_list': room_list
            })



    @login_required
    def hostPower(request):
        if request.method == 'GET':
            return render(request, 'host_power.html')

    @login_required
    def hostBoot(request):
        if request.method == 'GET':
            return render(request, 'host_boot.html')

    @login_required
    def hostRemote(request):
        if request.method == 'GET':
            return render(request, 'host_remote.html')

    @login_required
    def addHost(request):
        if request.method == 'GET':
            cluster_list = models.Clusters.objects.all()
            room_list = models.Rooms.objects.all()
            return render(request, 'add_host.html',
                          {'cluster_list': cluster_list,
                          'room_list': room_list})
        if request.method == 'POST':
            roomName = request.POST.get('roomName')
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
                roomName_id=roomName,
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
            print(roomName, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/add_host/')

    @login_required
    def hostInfoQuery(request):
        if request.method == 'POST':
            print("****************hostInfoQuery POST********************")
            advanceSearch = request.POST.get('allValue')
            print("****", advanceSearch)
            if advanceSearch:
                advanceSearch = json.loads(advanceSearch)
                print("the search is :", advanceSearch, type(advanceSearch))
                info_list = Q()
                for item in advanceSearch:
                    print(item, type(item))
                    item = json.loads(item)
                    print(item, type(item))
                    info_list = models.Host.objects.filter(Q(**item))
                print("the advance search info_list is :", info_list)
            data = json.dumps("success").encode()
            return HttpResponse(data)
        if request.method == 'GET':
            print("****************hostInfoQuery GET********************")
            info_list = models.Host.objects.all()
            limit = request.GET.get('limit')  # how many items per page
            #print("the limit :"+limit)
            offset = request.GET.get(
                'offset')  # how many items in total in the DB
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
                    print("powerOnTime",item.powerOnTime)
                    item.powerOnTime = item.powerOnTime.astimezone(
                        users_timezone).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
                    print("powerOnTime",type(item.powerOnTime))
                    print("powerOnTime",item.powerOnTime)
                if item.powerOffTime:
                    item.powerOffTime = item.powerOffTime.astimezone(
                        users_timezone).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
                    print("powerOffTime",item.powerOffTime,type(item.powerOffTime))
                
                info_list_dict['rows'].append({
                    "id":
                    item.id,
                    "roomName":
                    item.roomName.roomName,
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

    @login_required
    def HostDelete(request):
        if request.method == 'POST':
            ipmiID = request.POST.get('allValue')
            models.Host.objects.filter(id=ipmiID).delete()
            dictDelete = [ipmiID, 1]
            data = json.dumps(dictDelete).encode()
            return HttpResponse(data)

    @login_required
    def host_edit(request, nid):
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            cluster_list = models.Clusters.objects.all()
            room_list = models.Rooms.objects.all()
            return render(request, 'host_edit.html', {
                'host_obj': host_obj,
                'cluster_list': cluster_list,
                'room_list': room_list
            })
        if request.method == 'POST':
            roomName = request.POST.get('roomName')
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
                roomName_id=roomName,
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
            print(roomName, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/add_host/')

    @login_required
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

    @login_required
    def power_history(request, nid):
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            history_list = models.HostPowerHistory.objects.filter(host_id=nid)
            cluster_list = models.Clusters.objects.all()
            room_list = models.Clusters.objects.all()
            return render(request, 'power_history.html', {
                'history_list': history_list,
                'cluster_list': cluster_list,
                'room_list': room_list
            })
