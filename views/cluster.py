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

    def cluster_del(request, nid):
        if request.method == 'POST':
            obj = models.Host.objects.filter(clusterName_id=nid).first()
            if obj:
                return HttpResponse('该主机组已经被使用')
            else:
                models.Clusters.objects.filter(id=nid).delete()
                return redirect('/add_cluster/')