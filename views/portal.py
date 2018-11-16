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
from django.contrib.auth.decorators import login_required
# Create your views here.

class ClassPortal():
    
    def index(request):
        #返回index页面
        return render(request, 'index.html')

    @login_required
    def dashboard1(request):
        #返回dashboard1页面
            return render(request, 'dashboard1.html')


#仪表板2
    @login_required
    def dashboard2(request):
        if request.method == 'GET':            
            inspect_list_count = PeriodicTask.objects.filter(
                task='HostManager.Tasks.inspectSdr').count()
            periodicTask_list_count = PeriodicTask.objects.all().count()
            powerStatus_list_count = PeriodicTask.objects.filter(
                task='HostManager.Tasks.powerStatus').count()            
            fping_list_count = PeriodicTask.objects.filter(
                task='HostManager.Tasks.fping').count()
            otherTask_list_count = periodicTask_list_count - powerStatus_list_count - fping_list_count
            taskResult_success_count = TaskResult.objects.filter(status = 'SUCCESS').count()
            taskResult_fail_count = TaskResult.objects.filter(status = 'FAIL').count()
            A_deviceCount = models.Host.objects.filter(roomNO = 'A机房').count()
            B_deviceCount = models.Host.objects.filter(roomNO = 'B机房').count()
            C_deviceCount = models.Host.objects.filter(roomNO = 'C机房').count()
            N_deviceCount = models.Host.objects.filter(roomNO = 'N机房').count()
            
            
            return render(
                request, 'dashboard2.html', {                    
                    'inspect_list_count': inspect_list_count,
                    'periodicTask_list_count': periodicTask_list_count,
                    'powerStatus_list_count': powerStatus_list_count,
                    'otherTask_list_count': otherTask_list_count,
                    'fping_list_count': fping_list_count,                    
                    'A_deviceCount':A_deviceCount,
                    'B_deviceCount':B_deviceCount,
                    'C_deviceCount':C_deviceCount,
                    'N_deviceCount':N_deviceCount,
                    'taskResult_success_count':taskResult_success_count,
                    'taskResult_fail_count':taskResult_fail_count                   
                })