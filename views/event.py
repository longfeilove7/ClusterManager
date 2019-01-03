from rest_framework_swagger.views import get_swagger_view
from django.db.models import Count, Max, Avg, Min, Sum, F, Q, FloatField
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseBadRequest,request
from HostManager import models
from HostManager.models import audit
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
from django.contrib import auth

class eventlog():

    def event(request):
        #eventlist = models.audit.objects.all()
        eventlist = models.audit.objects.all().order_by('-id')[:10]
        return render(request, 'event.html', {'eventlist': eventlist})
