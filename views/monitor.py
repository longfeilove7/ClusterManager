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
from views import celery
# Create your views here.


class ClassMonitorSystem():
    #定义查询时间，如果在方法中定义会出现第二次调用方法时变量又重新初始化
    strStartTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    strEndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @login_required
    def monitorInfo(request):
        """"""
        if request.method == 'GET':
            return render(request, 'monitor_info.html')

    @login_required
    def monitorInfoQuery(request):
        #每次request的时候POST提交的数据会丢失，所以采用类变量暂存
        strStartTime = ClassMonitorSystem.strStartTime
        strEndTime = ClassMonitorSystem.strEndTime
        if request.method == 'POST':
            print("***************POST****************")
            #获取Jquery发送的字符串时间
            strStartTime = request.POST.get('startDateTime')
            strEndTime = request.POST.get('endDateTime')
            #将字符串时间转成时间格式
            startTime = datetime.datetime.strptime(strStartTime,
                                                   '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(strEndTime,
                                                 '%Y-%m-%d %H:%M:%S')
            print("the startTime", startTime, type(startTime))
            #设置时区
            users_timezone = pytz.timezone('Asia/Shanghai')
            print(users_timezone)
            #将本地时间格式化成UTC时间
            utcStartTime = startTime.astimezone(users_timezone).astimezone(
                pytz.utc).replace(tzinfo=None)
            print("utcStartTime", utcStartTime)
            utcEndTime = endTime.astimezone(users_timezone).astimezone(
                pytz.utc).replace(tzinfo=None)
            print("utcEndTime", utcEndTime)
            #将UTC时间赋值给类变量，以供GET请求使用
            ClassMonitorSystem.strStartTime = utcStartTime.strftime(
                "%Y-%m-%d %H:%M:%S")
            ClassMonitorSystem.strEndTime = utcEndTime.strftime(
                "%Y-%m-%d %H:%M:%S")
            data = json.dumps("success").encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print("***************GET****************")
            #获取POST过来的时间
            print(strStartTime)
            print(strEndTime)
            #将时间字符串再转成时间格式以支持timedelay
            startTime = datetime.datetime.strptime(
                ClassMonitorSystem.strStartTime, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(ClassMonitorSystem.strEndTime,
                                                 '%Y-%m-%d %H:%M:%S')
            countQueryTime = endTime - startTime
            #利用divmod方法获取时间时分秒
            hours, remainder = divmod(countQueryTime.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            #先转成int把小数点后面的0去掉，再利用字符串zfill给前面自动加0
            hours = str(int(hours)).zfill(2)
            minutes = str(int(minutes)).zfill(2)
            seconds = str(int(seconds)).zfill(2)

            #mysql 取书整floor(number),除法取整，x div y ,除法取余数, x mod y,四舍五入，round
            query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP"
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
                query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1 ) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP ORDER BY " + sort_column + " " + order
                info_list = models.Host.objects.raw(query)
            search = request.GET.get('search')
            if search:  #    判断是否有搜索字
                query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1 AND id like \'" + "%%" + search + "%%\'" + " OR manageIP like " + "\'%%" + search + "%%\'" + " OR serviceIP like " + "\'%%" + search + "%%\'" + " OR storageIP like " + "\'%%" + search + "%%" + "\' ) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP"
                print("the search :" + search, type(search))
                info_list = models.Host.objects.raw(query)
            else:
                info_list = models.Host.objects.raw(query)
            print("the obj :", info_list)
            #'RawQuerySet' object has no attribute 'count' so use len
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
            # the below is for test data
            #results_list_json = {  "total": 800, "rows": [ {"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" }]}
            for item in pageinator.page(page):
                print("the item:", type(item), item)
                info_list_dict['rows'].append({
                    "id":
                    item.id,
                    "serviceIP":
                    item.serviceIP,
                    "manageIP":
                    item.manageIP,
                    "storageIP":
                    item.storageIP,
                    "clusterName":
                    item.clusterName.clusterName,
                    "cycleTime":
                    "5分钟",
                    "countQueryTime":
                    '%s:%s:%s' % (hours, minutes, seconds),
                    "countMonitorTime":
                    #直接时间相加偶尔出现分钟大于60的情况，改用构造timedelta类型
                    str(
                        datetime.timedelta(
                            days=0,
                            seconds=0,
                            microseconds=0,
                            milliseconds=0,
                            minutes=item.countPowerOnMinute,
                            hours=item.countPowerOnHour,
                            weeks=0) + datetime.timedelta(
                                days=0,
                                seconds=0,
                                microseconds=0,
                                milliseconds=0,
                                minutes=item.countPowerOffMinute,
                                hours=item.countPowerOffHour,
                                weeks=0) + datetime.timedelta(
                                    days=0,
                                    seconds=0,
                                    microseconds=0,
                                    milliseconds=0,
                                    minutes=item.countPowerFailMinute,
                                    hours=item.countPowerFailHour,
                                    weeks=0)),
                    # '%s:%s:00' %
                    # (str(item.countPowerOnHour + item.countPowerOffHour +
                    #      item.countPowerFailHour).zfill(2),
                    #  str(item.countPowerOnMinute + item.countPowerOffMinute +
                    #      item.countPowerFailMinute).zfill(2)),
                    "countPowerOnTime":
                    '%s:%s:00' % (str(item.countPowerOnHour).zfill(2),
                                  str(item.countPowerOnMinute).zfill(2)
                                  ),  #将表格中小时和分钟列以字符串合并            
                    "countPowerOffTime":
                    '%s:%s:00' % (str(item.countPowerOffHour).zfill(2),
                                  str(item.countPowerOffMinute).zfill(2)),
                    "countPowerFailTime":
                    '%s:%s:00' % (str(item.countPowerFailHour).zfill(2),
                                  str(item.countPowerFailMinute).zfill(2))
                })
            info_list_json = json.dumps(info_list_dict)
            print("the info_list_json:", type(info_list_json))
            return HttpResponse(
                info_list_json,
                content_type="application/json",
            )

    @login_required
    def monitorDevice(request):
        """"""
        if request.method == 'GET':
            return render(request, 'monitor_device.html')

    @login_required
    def monitorSwitchQuery(request):
        """"""
        context = {}
        if request.method == 'GET':
            print("***************GET****************")
            limit = request.GET.get('limit')  # how many items per page
            #print("the limit :"+limit)
            offset = request.GET.get(
                'offset')  # how many items in total in the DB
            #print("the offset :"+offset)
            search = request.GET.get('search')
            #print("the search :"+search)
            #sort_column = request.GET.get('sort')   # which column need to sort
            #print("the sort_column :"+sort_column)
            order = request.GET.get('order')  # ascending or descending
            #print("the order :"+order)
            if search:  #    判断是否有搜索字
                result_list = models.Host.objects.filter(
                    Q(id__icontains=search)
                    | Q(roomName__icontains=search)
                    | Q(cabinetNO__icontains=search)
                    | Q(bladeBoxNO__icontains=search)
                    | Q(bladeNO__icontains=search)
                    | Q(hostName__icontains=search)
                    | Q(serviceIP__icontains=search)
                    | Q(manageIP__icontains=search)
                    | Q(storageIP__icontains=search)
                    | Q(hardware__icontains=search)
                    | Q(service__icontains=search))
            else:
                result_list = models.Host.objects.all(
                )  # must be wirte the line code here
            result_list_count = result_list.count()
            if not offset:
                offset = 0
            if not limit:
                limit = 10  # 默认是每页20行的内容，与前端默认行数一致
            pageinator = Paginator(result_list,
                                   limit)  # 利用Django的Painator开始做分页
            page = int(int(offset) / int(limit) + 1)
            print("the page:", page)
            results_list_dict = {
                "total": result_list_count,
                "rows": []
            }  # 必须带有rows和total这2个key，total表示总数，rows表示每行的内容
            # the below is for test data
            #results_list_json = {  "total": 800, "rows": [ {"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" }]}
            for item in pageinator.page(page):
                print("the item:", type(item), item)
                results_list_dict['rows'].append({
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
                    str(item.serviceIP),
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
                    "operate":
                    item.monitorStatus
                })
            results_list_json = json.dumps(results_list_dict)
            print("the results_list_json:", type(results_list_json))
            return HttpResponse(
                results_list_json,
                content_type="application/json",
            )

# the monitor price function

    @login_required
    def monitorPrice(request):
        """"""
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            monitor_list = models.monitor.objects.all()
            return render(
                request, 'monitor_price.html', {
                    'obj': obj,
                    'cluster_list': cluster_list,
                    'monitor_list': monitor_list
                })

# the monitor switch button function

    @login_required
    def monitorSwitch(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            setValue = request.POST.get('setValue')
            #print("setValue" + setValue)
            idName = request.POST.get('ID')
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiHost = db_dict['manageIP']
            ipmiUser = db_dict['ipmiUser']
            #print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            #print(ipmiPassword)
            models.Host.objects.filter(id=ipmiID).update(
                monitorStatus=setValue, )
            data = json.dumps(setValue).encode()
            # countRunTimeHistory = ClassCountCalculate.countRunTimeCalculate(ipmiID)
            # print(countRunTimeHistory)
            #if the setValue equal 1 then to set beat
            if setValue == "1":
                celery.ClassCeleryBeat.create_PowerStatus(idName)
                #ClassCeleryBeat.enable_task(idName)
            #if the setValue equal 0 then to stop beat
            elif setValue == "0":
                celery.ClassCeleryBeat.disable_task(idName)
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html')

# the batch add monitor button function

    @login_required
    def batchMonitorAdd(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print("the allValue: ", allValue, type(allValue))
            listAllValue = json.loads(allValue)
            print("the listAllValue: ", listAllValue, type(listAllValue))
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    monitorStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getmonitor = db_dict['monitorStatus']
                dictMonitor = [getID, getmonitor]
                print(dictMonitor)
                print(db_dict)
                listMonitor.append(dictMonitor)
                idName = ipmiID
                ipmiUser = db_dict['ipmiUser']
                ipmiHost = db_dict['manageIP']
                ipmiPassword = db_dict['ipmiPassword']
                celery.ClassCeleryBeat.create_PowerStatus(idName)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)

# the batch Pause monitor function

    @login_required
    def batchMonitorPause(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print("the allValue: ", allValue, type(allValue))
            listAllValue = json.loads(allValue)
            print("the listAllValue: ", listAllValue, type(listAllValue))
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    monitorStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getmonitor = db_dict['monitorStatus']
                dictMonitor = [getID, getmonitor]
                print(dictMonitor)
                print(db_dict)
                listMonitor.append(dictMonitor)
                idName = ipmiID
                celery.ClassCeleryBeat.disable_task(idName)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)


# the batch delete monitor function

    @login_required
    def batchMonitorDelete(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print("the allValue: ", allValue, type(allValue))
            listAllValue = json.loads(allValue)
            print("the listAllValue: ", listAllValue, type(listAllValue))
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    monitorStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getmonitor = db_dict['monitorStatus']
                dictMonitor = [getID, getmonitor]
                print(dictMonitor)
                print(db_dict)
                listMonitor.append(dictMonitor)
                idName = ipmiID
                celery.ClassCeleryBeat.delete_task(idName)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)