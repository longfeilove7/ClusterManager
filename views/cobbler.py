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
# Create your views here.

class ClassCobblerAPI():
    #def __init__(self):
    server = xmlrpc.client.ServerProxy("http://127.0.0.1/cobbler_api")
    print("**********************this is cobbler api ************************")
    def cobblerModifySystem(pxeMAC): 
        server = ClassCobblerAPI.server       
        print (server.get_distros())
        print (server.get_profiles())
        print (server.get_systems())
        print (server.get_images())
        print (server.get_repos())
        token = server.login("cobbler","cobbler")
        system_id = server.new_system(token)
        
        server.modify_system(system_id,"name",pxeMAC,token)
        server.modify_system(system_id,"hostname",pxeMAC,token)
        server.modify_system(system_id,'modify_interface', {
                "macaddress-eth0"   : pxeMAC,
                "ipaddress-eth0"    : "192.168.0.1",
                "dnsname-eth0"      : "hostname.example.com",
        }, token)
        server.modify_system(system_id,"profile","centos7.5-x86_64",token)
        server.modify_system(system_id,"kernel_options", "foo=bar some=thing", token)
        server.modify_system(system_id,"ks_meta", "foo=bar some=thing", token)

        server.save_system(system_id, token)
        server.sync(token)

    def cobblerRemoveSystem(pxeMAC):
        server = ClassCobblerAPI.server
        token = server.login("cobbler","cobbler")
        system_id = server.new_system(token)
        server = ClassCobblerAPI.server
        server.remove_system(pxeMAC,token)
        server.save_system(system_id, token)
        server.sync(token)

    