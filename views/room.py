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
from HostManager.models import Question, Choice, Host, Rooms
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


class ClassRoom:
    @login_required
    def addRoom(request):
        if request.method == 'GET':
            room_list = models.Rooms.objects.all()
            return render(request, 'add_room.html', {'room_list': room_list})
        elif request.method == 'POST':
            roomName = request.POST.get('roomName')
            cabinetNumber = request.POST.get('cabinetNumber')
            floor = request.POST.get('floor')
            roomArea = request.POST.get('roomArea')
            models.Rooms.objects.create(
                roomName=roomName,
                cabinetNumber=cabinetNumber,
                floor=floor,
                roomArea=roomArea)
            return redirect('/add_room/')

    @login_required
    def roomInfoQuery(request):
        info_list = models.Rooms.objects.all()
        limit = request.GET.get('limit')  # how many items per page
        #print("the limit :"+limit)
        offset = request.GET.get('offset')  # how many items in total in the DB
        #print("the offset :",offset)
        sort_column = request.GET.get('sort')  # which column need to sort
        search = request.GET.get('search')
        if sort_column:
            print("the sort_column :" + sort_column)
            order = request.GET.get('order')  # ascending or descending
            print("the order :" + order)
            if order == "asc":
                info_list = models.Rooms.objects.order_by(sort_column)
            else:
                info_list = models.Rooms.objects.order_by("-" + sort_column)
            print(info_list)
        elif search:  #    判断是否有搜索字
            info_list = models.Rooms.objects.filter(
                Q(id__icontains=search)
                | Q(roomName__icontains=search)
                | Q(cabinetNumber__icontains=search)
                | Q(floor__icontains=search)
                | Q(roomArea__icontains=search))
        else:
            info_list = models.Rooms.objects.all(
            )  # must be wirte the line code here
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
        for item in pageinator.page(page):
            info_list_dict['rows'].append({
                "id": item.id,
                "roomName": item.roomName,
                "cabinetNumber": item.cabinetNumber,
                "floor": item.floor,
                "roomArea": item.roomArea
            })
        info_list_json = json.dumps(info_list_dict)
        return HttpResponse(
            info_list_json,
            content_type="application/json",
        )

    @login_required
    def roomEdit(request, nid):
        if request.method == 'POST':
            roomName = request.POST.get('roomName')
            cabinetNumber = request.POST.get('cabinetNumber')
            floor = request.POST.get('floor')
            roomArea = request.POST.get('roomArea')
            models.Rooms.objects.filter(id=nid).update(
                roomName=roomName,
                cabinetNumber=cabinetNumber,
                floor=floor,
                roomArea=roomArea)
            print(roomName)
            return redirect('/add_room/')

    @login_required
    def roomDelete(request):
        if request.method == 'POST':
            ipmiID = request.POST.get('allValue')
            obj = models.Host.objects.filter(roomName_id=ipmiID).first()
            if obj:
                dictDelete = [ipmiID, 0]
            else:
                models.Rooms.objects.filter(id=ipmiID).delete()
                dictDelete = [ipmiID, 1]
            data = json.dumps(dictDelete).encode()
            return HttpResponse(data)

    @login_required
    def batchRoomDelete(request):
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
                obj = models.Host.objects.filter(roomName_id=ipmiID).first()
                if obj:
                    dictDelete = [ipmiID, 0]
                    listDelete.append(dictDelete)
                else:
                    models.Rooms.objects.filter(id=ipmiID).delete()
                    dictDelete = [ipmiID, 1]
                    listDelete.append(dictDelete)
            data = json.dumps(listDelete).encode()
            return HttpResponse(data)
