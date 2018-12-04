"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
from django.contrib import auth         #导入auth模块
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
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
# Create your views here.

#定义全局变量用于存储页面当前用户信息
GLOBAL_VAR_USER = "0"

#系统登录类ClassSign
#系统登录函数signin
class ClassSign():
    def signin(request):
        #如果是POST请求
        if request.method == "POST":
            #声明调用全局变量
            global GLOBAL_VAR_USER
            #通过django的request.POST.get()方法获取user值，并赋值给全局变量
            GLOBAL_VAR_USER = request.POST.get('user')
            #通过django的request.POST.get()方法获取pwd值，并赋值给局部变量
            local_var_password = request.POST.get('pwd')
            #查询数据库用户名和密码是否匹配
            user=authenticate(username=GLOBAL_VAR_USER,password=local_var_password)  # 验证用户名和密码，返回用户对象
            #如果user为非空
            if user:
                login(request,user)         # 用户登陆
                #渲染主页，并返回用户名
                return render(request, 'index.html', {'user': user})
            else:                
                return HttpResponse("用户名或密码错误")
                #返回登录页面
                #return render(request, 'sign-in.html')
        else:
            #如果是GET请求，返回登录页面
            return render(request, 'sign-in.html')


#系统注册函数

    def signup(request):
        #如果是POST请求
        if request.method == "POST":
            #通过django的request.POST.get()获取用户名
            GLOBAL_VAR_USER = request.POST.get('user')
            #通过django的request.POST.get()获取密码
            local_var_password = request.POST.get('pwd')
            #根据用户名和密码创建用户信息            
            user=User.objects.create_user(username=GLOBAL_VAR_USER,password=local_var_password)
            #返回注册成功页面
            return render(request, 'sucess.html')
        else:
            #返回用户注册页面
            return render(request, 'sign-up.html')

    def signout(request):
            
            logout(request)     # 注销用户
            
            return redirect("/sign-up/")























