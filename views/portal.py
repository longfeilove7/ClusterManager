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

class ClassPortal():
    def index(request):
        #声明使用全局变量
        global GLOBAL_VAR_USER
        #查询数据库用户名
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        #返回index页面
        return render(request, 'index.html', {'user_list': user_list})

    def dashboard1(request):
        #如果是POST请求
        if request.method == "POST":
            #声明调用全局变量
            global GLOBAL_VAR_USER
            #通过django的request.POST.get()方法获取user值，并赋值给全局变量
            GLOBAL_VAR_USER = request.POST.get('user')
            #通过django的request.POST.get()方法获取pwd值，并赋值给局部变量
            local_var_password = request.POST.get('pwd')
            #查询数据库用户名和密码是否匹配
            user_list = models.Users.objects.filter(
                username=GLOBAL_VAR_USER, password=local_var_password).first()
            #如果user_list为非空
            if user_list:
                #渲染主页，并返回用户名
                return render(request, 'index.html', {'user_list': user_list})
            else:
                #返回登录页面
                return render(request, 'sign-in.html')
        else:
            #如果是GET请求，返回登录页面
            return render(request, 'sign-in.html')


#仪表板2

    def dashboard2(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
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
                    'user_list': user_list,
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