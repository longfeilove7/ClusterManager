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

class ClassInstallSystem():
    #定义查询时间，如果在方法中定义会出现第二次调用方法时变量又重新初始化
    strStartTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    strEndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def installDevice(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'install_device.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })

    def installInfo(request):
            global GLOBAL_VAR_USER
            user_list = models.Users.objects.filter(
                username=GLOBAL_VAR_USER).first()
            if request.method == 'GET':
                obj = models.Host.objects.all()
                cluster_list = models.Clusters.objects.all()
                return render(request, 'install_info.html', {
                    'obj': obj,
                    'cluster_list': cluster_list,
                    'user_list': user_list
                })

    def installInfoQuery(request):
        #每次request的时候POST提交的数据会丢失，所以采用类变量暂存
        strStartTime = ClassInstallSystem.strStartTime
        strEndTime = ClassInstallSystem.strEndTime
        if request.method == 'POST':
            print("***************POST****************")
            #获取Jquery发送的字符串时间
            strStartTime = request.POST.get('startDateTime')
            strEndTime = request.POST.get('endDateTime')
            print("ssssssssssssss", strStartTime)
            print("ssssssssssssss", strEndTime)
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
            ClassInstallSystem.strStartTime = utcStartTime.strftime(
                "%Y-%m-%d %H:%M:%S")
            ClassInstallSystem.strEndTime = utcEndTime.strftime(
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
                ClassInstallSystem.strStartTime, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(ClassInstallSystem.strEndTime,
                                                 '%Y-%m-%d %H:%M:%S')
            countQueryTime = endTime - startTime
            #利用divmod方法获取时间时分秒
            hours, remainder = divmod(countQueryTime.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            #先转成int把小数点后面的0去掉，再利用字符串zfill给前面自动加0
            hours = str(int(hours)).zfill(2)
            minutes = str(int(minutes)).zfill(2)
            seconds = str(int(seconds)).zfill(2)
            price = str(5)
            #mysql 取书整floor(number),除法取整，x div y ,除法取余数, x mod y,四舍五入，round
            #query = "select id,ifnull(sumRunTimeHour,0) as sumRunTimeHour,ifnull(sumRunTimeMinute,0) as sumRunTimeMinute,ifnull((sumRunTimeHour*" + price + "+sumRunTimeMinute/60*" + price + "),0) as sumMoney  from (select * from (SELECT * FROM hostmanager_host WHERE installstatus=1) as a left join (SELECT host_id,sum(runtimehistory)/1000000/60 div 3600  as sumRunTimeHour,round((sum(runtimehistory)/1000000/60 mod 60))  as sumRunTimeMinute FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory>'" + strStartTime + "' AND powerOffTimeHistory<'" + strEndTime + "' group by host_id) as b on a.id=b.host_id) as temp"
            query = "select id,ifnull(installStartTimeHistory,'0000-00-00 00:00:00') as installStartTimeHistory,ifnull(installEndTimeHistory,'0000-00-00 00:00:00') as installEndTimeHistory,ifnull(installRunTimeHistory,'00:00:00') as installRunTimeHistory,ifnull(installSystemStatus,0) installSystemStatus  from (select * from (SELECT * FROM hostmanager_host WHERE installstatus=1) as a left join (SELECT installStartTimeHistory,installEndTimeHistory,installRunTimeHistory,installSystemStatus,host_id FROM hostmanager_installsystemhistory WHERE installStartTimeHistory in (select max(installStartTimeHistory) from hostmanager_installsystemhistory group by host_id) ) as b on a.id=b.host_id) as temp"
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
                query = "select id,ifnull(sumRunTimeHour,0) as sumRunTimeHour,ifnull(sumRunTimeMinute,0) as sumRunTimeMinute,ifnull((sumRunTimeHour*" + price + "+sumRunTimeMinute/60*" + price + "),0) as sumMoney  from (select * from (SELECT * FROM hostmanager_host WHERE installstatus=1) as a left join (SELECT host_id,sum(runtimehistory)/1000000/60 div 3600  as sumRunTimeHour,round((sum(runtimehistory)/1000000/60 mod 60))  as sumRunTimeMinute FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory<'" + strStartTime + "' AND powerOffTimeHistory>'" + strEndTime + "' group by host_id) as b on a.id=b.host_id) as temp ORDER BY " + sort_column + " " + order
                info_list = models.Host.objects.raw(query)
            search = request.GET.get('search')
            if search:  #    判断是否有搜索字
                query = "select id,ifnull(sumRunTimeHour,0) as sumRunTimeHour,ifnull(sumRunTimeMinute,0) as sumRunTimeMinute,ifnull((sumRunTimeHour*" + price + "+sumRunTimeMinute/60*" + price + "),0) as sumMoney  from (select * from (SELECT * FROM hostmanager_host WHERE installstatus=1 AND id like \'" + "%%" + search + "%%\'" + " OR manageIP like " + "\'%%" + search + "%%\'" + " OR serviceIP like " + "\'%%" + search + "%%\'" + " OR storageIP like " + "\'%%" + search + "%%" + "\' ) as a left join (SELECT host_id,sum(runtimehistory)/1000000/60 div 3600  as sumRunTimeHour,round((sum(runtimehistory)/1000000/60 mod 60))  as sumRunTimeMinute FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory<'" + strStartTime + "' AND powerOffTimeHistory>'" + strEndTime + "' group by host_id) as b on a.id=b.host_id) as temp"
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
            #设置时区
            users_timezone = pytz.timezone('Asia/Shanghai')
            for item in pageinator.page(page):
                print("the item:", type(item), item)
                #判断是否为空，然后将带时区的时间格式转成本地时间
                if item.powerOnTime:
                    print(item.powerOnTime)
                    item.powerOnTime = item.powerOnTime.astimezone(
                        users_timezone).replace(tzinfo=None)
                    print(item.powerOnTime)
                if item.powerOffTime:
                    item.powerOffTime = item.powerOffTime.astimezone(
                        users_timezone).replace(tzinfo=None)

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
                    "countQueryTime":
                    '%s:%s:%s' % (hours, minutes, seconds),
                    "installStartTimeHistory":
                    str(item.installStartTimeHistory),
                    "installEndTimeHistory":
                    str(item.installEndTimeHistory),
                    "installRunTimeHistory":
                    str(item.installRunTimeHistory),
                    "operate":
                    str(item.installSystemStatus)
                })
            info_list_json = json.dumps(info_list_dict)
            print("the info_list_json:", type(info_list_json))
            return HttpResponse(
                info_list_json,
                content_type="application/json",
            )
    
    def installingSwitch(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiID = request.POST.get('ID')
            print("ipmiID",ipmiID)
            setValue = request.POST.get('setValue')
            print("test" + setValue)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)
            ipmiHost = db_dict['manageIP']
            powerOnTime = db_dict['powerOnTime']
            
            
            if setValue == '1':
                print("111111111111")
                powerStatus = tasks.powerStatus.delay(ipmiID,ipmiHost, ipmiUser,
                                         ipmiPassword).get()[3]
                if powerStatus == "on":
                    tasks.bootdevPxe.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()
                    result = tasks.powerCycle.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()
                if powerStatus == "off":
                    result = tasks.powerOn.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()
                print(powerStatus)
                models.Host.objects.filter(id=ipmiID).update(
                    powerOnTime=result[1])              
                installStartTime = result[1]                
                models.InstallSystemHistory.objects.all().create(host_id=ipmiID,installStartTimeHistory = installStartTime,
                    installSystemStatus=setValue, )
            else:  
                installStartTime = powerOnTime
                tasks.bootdevDisk.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()
                result = tasks.powerCycle.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()              
                installEndTime = result[1] 
                models.InstallSystemHistory.objects.filter(host_id=ipmiID,installStartTimeHistory=installStartTime).update(host_id=ipmiID,installEndTimeHistory = installEndTime,
                    installSystemStatus=setValue, )
            data = json.dumps(setValue).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'install_info.html', context)

    def installSwitchQuery(request):
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
                    | Q(roomNO__icontains=search)
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
                    "roomNO":
                    item.roomNO,
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
                    item.installStatus
                })
            results_list_json = json.dumps(results_list_dict)
            print("the results_list_json:", type(results_list_json))
            return HttpResponse(
                results_list_json,
                content_type="application/json",
            )


    def installSwitch(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            setValue = request.POST.get('setValue')
            print("test" + setValue)
            models.Host.objects.filter(id=ipmiID).update(
                installStatus=setValue, )
            data = json.dumps(setValue).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'install_device.html', context)

# the batch add install button function

    def batchInstallAdd(request):
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
            listInstall = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    installStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getInstall = db_dict['installStatus']
                dictInstall = [getID, getInstall]
                print(dictInstall)
                print(db_dict)
                listInstall.append(dictInstall)
            data = json.dumps(listInstall).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'install_device.html', context)


# the batch delete install function

    def batchInstallDelete(request):
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
            listInstall = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    installStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getInstall = db_dict['installStatus']
                dictInstall = [getID, getInstall]
                print(dictInstall)
                print(db_dict)
                listInstall.append(dictInstall)
            data = json.dumps(listInstall).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'install_device.html', context)