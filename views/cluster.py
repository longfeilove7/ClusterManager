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

class ClassCluster:
    def add_cluster(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            cluster_list = models.Clusters.objects.all()
            return render(request, 'add_cluster.html', {
                'cluster_list': cluster_list,
                'user_list': user_list
            })
        elif request.method == 'POST':
            clusterName = request.POST.get('clusterName')
            deviceNumber = request.POST.get('deviceNumber')
            customerName = request.POST.get('customerName')
            contactPerson = request.POST.get('contactPerson')
            contactPhone = request.POST.get('contactPhone')
            contactEmail = request.POST.get('contactEmail')
            contactQQ = request.POST.get('contactQQ')
            contactWeicat = request.POST.get('contactWeicat')
            models.Clusters.objects.create(
                clusterName=clusterName,
                deviceNumber=deviceNumber,
                customerName=customerName,
                contactPerson=contactPerson,
                contactPhone=contactPhone,
                contactEmail=contactEmail,
                contactQQ=contactQQ,
                contactWeicat=contactWeicat,
            )

            return redirect('/add_cluster/')

    def clusterInfoQuery(request):
            info_list = models.Clusters.objects.all()            
            limit = request.GET.get('limit')  # how many items per page
            #print("the limit :"+limit)
            offset = request.GET.get(
                'offset')  # how many items in total in the DB
            #print("the offset :",offset)
            sort_column = request.GET.get('sort')  # which column need to sort
            search = request.GET.get('search')
            if sort_column:
                print("the sort_column :" + sort_column)
                order = request.GET.get('order')  # ascending or descending
                print("the order :" + order)
                if order == "asc":
                    info_list = models.Clusters.objects.order_by(sort_column)
                else:
                    info_list = models.Clusters.objects.order_by("-"+sort_column)
                print(info_list)            
            elif search:  #    判断是否有搜索字
                info_list = models.Clusters.objects.filter(
                    Q(id__icontains=search)
                    | Q(clusterName__icontains=search)
                    | Q(deviceNumber__icontains=search)
                    | Q(customerName__icontains=search)
                    | Q(contactPerson__icontains=search)
                    | Q(contactPhone__icontains=search)
                    | Q(contactEmail__icontains=search)
                    | Q(contactQQ__icontains=search)
                    | Q(contactWeicat__icontains=search)
                    )
            else:
                info_list = models.Clusters.objects.all(
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
                    "id":
                    item.id,
                    "clusterName":
                    item.clusterName,
                    "deviceNumber":
                    item.deviceNumber,
                    "customerName":
                    item.customerName,
                    "contactPerson":
                    item.contactPerson,
                    "contactPhone":
                    item.contactPhone,
                    "contactEmail":
                    item.contactEmail,
                    "contactQQ":
                    item.contactQQ,
                    "contactWeicat":
                    item.contactWeicat                    
                })
            info_list_json = json.dumps(info_list_dict)
            return HttpResponse(
                info_list_json,
                content_type="application/json",
            )

    def cluster_edit(request, nid):
        if request.method == 'POST':
            clusterName = request.POST.get('clusterName')
            deviceNumber = request.POST.get('deviceNumber')
            customerName = request.POST.get('customerName')
            contactPerson = request.POST.get('contactPerson')
            contactPhone = request.POST.get('contactPhone')
            contactEmail = request.POST.get('contactEmail')
            contactQQ = request.POST.get('contactQQ')
            contactWeicat = request.POST.get('contactWeicat')
            models.Clusters.objects.filter(id=nid).update(
                clusterName=clusterName,
                deviceNumber=deviceNumber,
                customerName=customerName,
                contactPerson=contactPerson,
                contactPhone=contactPhone,
                contactEmail=contactEmail,
                contactQQ=contactQQ,
                contactWeicat=contactWeicat,
            )
            print(clusterName)
            return redirect('/add_cluster/')

    def ClusterDelete(request):
        if request.method == 'POST':
            ipmiID = request.POST.get('allValue')
            obj = models.Host.objects.filter(clusterName_id=ipmiID).first()
            if obj:
                dictDelete = [ipmiID, 0]                              
            else:
                models.Clusters.objects.filter(id=ipmiID).delete()
                dictDelete = [ipmiID, 1]               
            data = json.dumps(dictDelete).encode()
            return HttpResponse(data)        

    def batchClusterDelete(request):    
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
                obj = models.Host.objects.filter(clusterName_id=ipmiID).first()
                if obj:
                    dictDelete = [ipmiID, 0]
                    listDelete.append(dictDelete)                   
                else:
                    models.Clusters.objects.filter(id=ipmiID).delete()
                    dictDelete = [ipmiID, 1]                
                    listDelete.append(dictDelete)
            data = json.dumps(listDelete).encode()
            return HttpResponse(data)        