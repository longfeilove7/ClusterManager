"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
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

# Create your views here.

def UserIP(request):
    '''
    获取用户IP
    '''

    ip = ''


    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    return ip

class ClassBillingSystem():
    #定义查询时间，如果在方法中定义会出现第二次调用方法时变量又重新初始化
    strStartTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    strEndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @login_required
    def billingInfo(request):
        """"""        
        if request.method == 'GET':
            #filter the billing value equal 1
            host = models.Host.objects.filter(billingStatus=1)
            # print(host[0].clusterName_id)
            cid = host[0].clusterName_id
            bil_pric = models.Billing.objects.filter(clusterName_id=cid)
            # print(bil_pric[0].billingPrice)
            #obj =  host.annotate(countPowerOnHour=5*Count("checkpoweron")/60).annotate(countPowerOffHour=5*Count("checkpoweroff")/60).annotate(countPowerFailHour=5*Count("checkpowerfail")/60).annotate(countPowerOnMinute=5*Count("checkpoweron")%60).annotate(countPowerOffMinute=5*Count("checkpoweroff")%60).annotate(countPowerFailMinute=5*Count("checkpowerfail")%60)
            #设置每台机器1小时的租用价格
            price = str(bil_pric[0].billingPrice)
            # price = str(12.8)
            # clsname = host.clusterName
            # billing_list = models.Billing.objects.get(clusterName=clsname)
            # price = billing_list.
            obj = models.Host.objects.raw(
                "select id,ifnull(sumRunTimeHour,0) as sumRunTimeHour,ifnull(sumRunTimeMinute,0) as sumRunTimeMinute,ifnull((sumRunTimeHour*"
                + price + "+sumRunTimeMinute/60*" + price +
                "),0) as sumMoney  from (select * from (SELECT * FROM hostmanager_host WHERE billingstatus=1) as a left join (SELECT host_id,sum(runtimehistory)/1000000/60 div 3600  as sumRunTimeHour,round((sum(runtimehistory)/1000000/60 mod 60))  as sumRunTimeMinute FROM hostmanager_hostpowerhistory group by host_id) as b on a.id=b.host_id) as temp"
            )
            cluster_list = models.Clusters.objects.all()
            # the .aggregate(Sum()) to sum  .aggregate(Avg()) to average.but can't use for timedelta
            test = models.HostPowerHistory.objects.all().aggregate(
                Count("powerCycleTimes"))
            print(test)
            return render(request, 'billing_info.html', {
                'obj': obj,
                'cluster_list': cluster_list
                # 'billing_list': billing_list
            })
    @login_required
    def billingInfoQuery(request):
        #每次request的时候POST提交的数据会丢失，所以采用类变量暂存
        strStartTime = ClassBillingSystem.strStartTime
        strEndTime = ClassBillingSystem.strEndTime
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
            ClassBillingSystem.strStartTime = utcStartTime.strftime(
                "%Y-%m-%d %H:%M:%S")
            ClassBillingSystem.strEndTime = utcEndTime.strftime(
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
                ClassBillingSystem.strStartTime, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(ClassBillingSystem.strEndTime,
                                                 '%Y-%m-%d %H:%M:%S')
            countQueryTime = endTime - startTime
            #利用divmod方法获取时间时分秒
            hours, remainder = divmod(countQueryTime.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            #先转成int把小数点后面的0去掉，再利用字符串zfill给前面自动加0
            hours = str(int(hours)).zfill(2)
            minutes = str(int(minutes)).zfill(2)
            seconds = str(int(seconds)).zfill(2)
            host = models.Host.objects.filter(billingStatus=1)
            cid = host[0].clusterName_id
            bil_pric = models.Billing.objects.filter(clusterName_id=cid)
            # print(bil_pric[0].billingPrice)
            #obj =  host.annotate(countPowerOnHour=5*Count("checkpoweron")/60).annotate(countPowerOffHour=5*Count("checkpoweroff")/60).annotate(countPowerFailHour=5*Count("checkpowerfail")/60).annotate(countPowerOnMinute=5*Count("checkpoweron")%60).annotate(countPowerOffMinute=5*Count("checkpoweroff")%60).annotate(countPowerFailMinute=5*Count("checkpowerfail")%60)
            #设置每台机器1小时的租用价格
            price = str(bil_pric[0].billingPrice)

            # price = str(12.8)
            #mysql 取书整floor(number),除法取整，x div y ,除法取余数, x mod y,四舍五入，round
            query = "SELECT id,ifnull(sumRunTime,0) AS sumRunTime,ifnull(sumMoney,0) AS sumMoney FROM (SELECT * FROM (SELECT * FROM hostmanager_host WHERE billingStatus=1) AS a LEFT JOIN (select host_id ,sum(runTimeHistory)/1000000/3600 as sumRunTime,sum(runTimeHistory)/1000000/3600*"+price+" as sumMoney FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory>'" + strStartTime + "' AND powerOffTimeHistory<'" + strEndTime + "' group by host_id) AS b ON a.id=b.host_id) AS TEMP"
            #print(query,"1111111111111111111111111111111111111111111111111111")
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
                query = "SELECT id,ifnull(sumRunTime,0) AS sumRunTime,ifnull(sumMoney,0) AS sumMoney FROM (SELECT * FROM (SELECT * FROM hostmanager_host WHERE billingStatus=1) AS a LEFT JOIN (select host_id ,sum(runTimeHistory)/1000000/3600 as sumRunTime,sum(runTimeHistory)/1000000/3600*"+price+" as sumMoney FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory>'" + strStartTime + "' AND powerOffTimeHistory<'" + strEndTime + "' group by host_id) AS b ON a.id=b.host_id) AS TEMP ORDER BY " + sort_column + " " + order
                info_list = models.Host.objects.raw(query)
            search = request.GET.get('search')
            if search:  #    判断是否有搜索字
                query = "SELECT id,ifnull(sumRunTime,0) AS sumRunTime,ifnull(sumMoney,0) AS sumMoney FROM (SELECT * FROM (SELECT * FROM hostmanager_host WHERE billingStatus=1 AND id like \'" + "%%" + search + "%%\'" + " OR manageIP like " + "\'%%" + search + "%%\'" + " OR serviceIP like " + "\'%%" + search + "%%\'" + " OR storageIP like " + "\'%%" + search + "%%" + "\' ) AS a LEFT JOIN (select host_id ,sum(runTimeHistory)/1000000/3600 as sumRunTime,sum(runTimeHistory)/1000000/3600*"+price+" as sumMoney FROM hostmanager_hostpowerhistory WHERE powerOnTimeHistory>'" + strStartTime + "' AND powerOffTimeHistory<'" + strEndTime + "' group by host_id) AS b ON a.id=b.host_id) AS TEMP"

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
                    "price":
                    price,
                    "countQueryTime":
                    '%s:%s:%s' % (hours, minutes, seconds),
                    "powerOnTime":
                    str(item.powerOnTime),
                    "powerOffTime":
                    str(item.powerOffTime),
                    "sumRunTime":
                    str((item.sumRunTime).quantize(Decimal('0.00'))),
                    "sumMoney":
                    str((item.sumMoney).quantize(Decimal('0.00')))
                })
            info_list_json = json.dumps(info_list_dict)
            print("the info_list_json:", type(info_list_json))
            return HttpResponse(
                info_list_json,
                content_type="application/json",
            )
    @login_required
    def billingDevice(request):
        """"""       
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'billing_device.html', {
                'obj': obj,
                'cluster_list': cluster_list
            })
# the billing price function
    @login_required
#     @property
    def billingPrice(request):
        """"""       
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            billing_list = models.Billing.objects.all()
            return render(
                request, 'billing_price.html', {
                    'obj': obj,
                    'cluster_list': cluster_list,
                    'billing_list': billing_list
                })
    #添加单价
    # @property
    @login_required
    def addprice(request):
        user = request.user.username


        new_cluster = request.POST.get("clusterName")
        # new_deviceNumber = request.POST.get("deviceNumber")
        new_billingNumber = request.POST.get("billingNumber")
        new_billingPrice = request.POST.get("billingPrice")
        # newcls = Clusters()
        # newcls.clusterName =
        models.Billing.objects.create(
            # clusterName = new_cluster,
            billingNumber = new_billingNumber,
            clusterName_id = new_cluster,
            billingPrice = new_billingPrice
        )
        audit.objects.create(username=user, actionip=UserIP(request), content="添加单价")
        return redirect('/billing_price/')
    #修改单价
    @login_required
    def editbill(request,nid):
        new_billingNumber = request.POST.get("billingNumber")
        new_billingPrice = request.POST.get("billingPrice")
        billpric = models.Billing.objects.get(id=nid)
        billpric.billingPrice = new_billingPrice
        billpric.billingNumber = new_billingNumber
        billpric.save()
        return redirect('/billing_price/')
    #删除单价
    @login_required
    def delbill(request,nid):
        # del_clsid = request.POST.get("spanID")
        # print(nid)
        user = request.user.username
        if nid:
            del_obj = models.Billing.objects.get(id=nid)
            del_obj.delete()
        audit.objects.create(username=user, actionip=UserIP(request), content="删除单价")
        return redirect('/billing_price/')
        # pass


    @login_required
    def billingSwitchQuery(request):
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
                    item.billingStatus
                })
            results_list_json = json.dumps(results_list_dict)
            print("the results_list_json:", type(results_list_json))
            return HttpResponse(
                results_list_json,
                content_type="application/json",
            )

# the billing switch button function
    @login_required
    def billingSwitch(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            setValue = request.POST.get('setValue')
            print("test" + setValue)
            models.Host.objects.filter(id=ipmiID).update(
                billingStatus=setValue, )
            data = json.dumps(setValue).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'billing_device.html', context)

# the batch add billing button function
    @login_required
    def batchBillingAdd(request):
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
            listBilling = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    billingStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getBilling = db_dict['billingStatus']
                dictBilling = [getID, getBilling]
                print(dictBilling)
                print(db_dict)
                listBilling.append(dictBilling)
            data = json.dumps(listBilling).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'billing_device.html', context)


# the batch delete billing function
    @login_required
    def batchBillingDelete(request):
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
            listBilling = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                ipmiID = dictAllValue['id']
                print(ipmiID)
                models.Host.objects.filter(id=ipmiID).update(
                    billingStatus=setValue, )
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                getID = db_dict['id']
                getBilling = db_dict['billingStatus']
                dictBilling = [getID, getBilling]
                print(dictBilling)
                print(db_dict)
                listBilling.append(dictBilling)
            data = json.dumps(listBilling).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'billing_device.html', context)

