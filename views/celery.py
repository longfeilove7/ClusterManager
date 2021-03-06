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
from views import calculate
# Create your views here.

#定义全局变量用于存储页面当前用户信息
BLOBAL_VAR_TIMEINTERVAL = IntervalSchedule.objects.all()
BLOBAL_VAR_TIMECYCLE = CrontabSchedule.objects.all()

# for celery beat about html
class ClassCeleryBeat():
    def periodic_task(request):
        global BLOBAL_VAR_TIMEINTERVAL
        global BLOBAL_VAR_TIMECYCLE
        if request.method == 'GET':
            periodic_list = PeriodicTask.objects.all()
            return render(request, 'celery/beat/periodic_task.html', {
                'periodic_list': periodic_list,
                'TimeInterval':BLOBAL_VAR_TIMEINTERVAL,
                'TimeCycle':BLOBAL_VAR_TIMECYCLE
            })

    #def add_periodic(request):
        # if request.method == 'POST':
        #     clusterName = request.POST.get('clusterName')
        #     deviceNumber = request.POST.get('deviceNumber')
        #     customerName = request.POST.get('customerName')
        #     contactPerson = request.POST.get('contactPerson')
        #     contactPhone = request.POST.get('contactPhone')
        #     contactEmail = request.POST.get('contactEmail')
        #     contactQQ = request.POST.get('contactQQ')
        #     contactWeicat = request.POST.get('contactWeicat')
        #     models.Clusters.objects.create(
        #         clusterName=clusterName,
        #         deviceNumber=deviceNumber,
        #         customerName=customerName,
        #         contactPerson=contactPerson,
        #         contactPhone=contactPhone,
        #         contactEmail=contactEmail,
        #         contactQQ=contactQQ,
        #         contactWeicat=contactWeicat,
        #     )

        #     return redirect('/periodic_task/')

    def add_periodic(request):
        print("Add Crontab")
        Name=request.POST.get('name')
        print(Name)
        password=request.POST.get('passwd')
        print(password)
        usernames=request.POST.get('username')
        print(usernames)
        commands=request.POST.get('command')
        print(commands)
        IPaddress=request.POST.get('serviceIP')
        print(IPaddress)
        timeIntervalID=request.POST.get('timeinterval')
        print(timeIntervalID)
        timeCycleID=request.POST.get('timecycle')
        print(timeCycleID)
        ClassCeleryBeat.add_periodic1(password,usernames,commands,IPaddress,Name,timeIntervalID,timeCycleID)
        return redirect('/periodic_task/')

    def add_periodic1(password,usernames,commands,IPaddress,Name,timeIntervalID,timeCycleID):
        if timeIntervalID:
            db_dict = IntervalSchedule.objects.filter(id=timeIntervalID).values()[0]
            schedule, created = IntervalSchedule.objects.get_or_create(
               every=db_dict['every'],
               period=db_dict['period'],
           )
            try:
                print("------------do try----------")
                task, created = PeriodicTask.objects.get_or_create(
                #crontab=schedule,
                name=Name,
                task='HostManager.Tasks.CustomTask',
                interval=schedule,  # we created this above.
                args=json.dumps([password,usernames,commands,IPaddress])
                # kwargs=json.dumps({
                #     'be_careful': True,
                # }),
                #expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
                )
                print("------------do try11111----------")
                if created:
                    task.enabled = True
                    task.save()
                    print("111111111111111111")
                else:
                    task.enabled = True
                    task.save()
                    print("2222222222222222")
                return True
            except:
                # print("------------do except------------")
                # periodicTask = PeriodicTask.objects.get(name=Name)
                # periodicTask.enabled = True  # 设置开启
                # periodicTask.save()
                return True
        elif timeCycleID:
            db_dict = CrontabSchedule.objects.filter(id=timeCycleID).values()[0]
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=db_dict['minute'],
                hour=db_dict['hour'],
                day_of_week=db_dict['day_of_week'],
                day_of_month=db_dict['day_of_month'],
                month_of_year=db_dict['month_of_year'],
            )
            try:
                print("------------do try----------")
                task, created = PeriodicTask.objects.get_or_create(
                crontab=schedule,
                name=Name,
                task='HostManager.Tasks.CustomTask',
                #interval=schedule,  # we created this above.
                args=json.dumps([password,usernames,commands,IPaddress])
                # kwargs=json.dumps({
                #     'be_careful': True,
                # }),
                #expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
                )
                print("------------do try11111----------")
                if created:
                    task.enabled = True
                    task.save()
                    print("111111111111111111")
                else:
                    task.enabled = True
                    task.save()
                    print("2222222222222222")
                return True
            except:
                # print("------------do except------------")
                # periodicTask = PeriodicTask.objects.get(name=Name)
                # periodicTask.enabled = True  # 设置开启
                # periodicTask.save()
                return True
        #print("start to try...except")
        #创建一个周期性任务,如果查询到就返回，如果没查询到就向数据库加入新的对象
        # try:
        #     print("------------do try----------")
        #     task, created = PeriodicTask.objects.get_or_create(
        #     #crontab=schedule,
        #     name=Name,
        #     task='HostManager.Tasks.CustomTask',
        #     interval=schedule,  # we created this above.
        #     args=json.dumps(['password','usernames','commands','IPaddress'])
        #     # kwargs=json.dumps({
        #     #     'be_careful': True,
        #     # }),
        #     #expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        #     )
        #     print("------------do try11111----------")
        #     if created:
        #         task.enabled = True
        #         task.save()
        #         print("111111111111111111")
        #     else:
        #         task.enabled = True
        #         task.save()
        #         print("2222222222222222")
        #     return True
        # except:
        #     # print("------------do except------------")
        #     # periodicTask = PeriodicTask.objects.get(name=Name)
        #     # periodicTask.enabled = True  # 设置开启
        #     # periodicTask.save()
        #     return True

        #开启任务

        #PeriodicTask.enabled = True
        print("----------------------------")


    def interval_schedule(request):
        if request.method == 'GET':
            interval_list = IntervalSchedule.objects.all()
            return render(request, 'celery/beat/interval_schedule.html', {
                'interval_list': interval_list,
            })
        if request.method == 'POST':
            every = request.POST.get('every')
            period = request.POST.get('period')
            IntervalSchedule.objects.create(
                every=every,
                period=period,
            )
            return redirect('/interval_schedule/')

    def solar_schedule(request):
        if request.method == 'GET':
            solar_list = SolarSchedule.objects.all()
            return render(request, 'celery/beat/solar_schedule.html', {
                'solar_list': solar_list,
            })

    def crontab_schedule(request):
        if request.method == 'GET':
            crontab_list = CrontabSchedule.objects.all()
            return render(request, 'celery/beat/crontab_schedule.html', {
                'crontab_list': crontab_list,
            })
        if request.method == 'POST':
            minute = request.POST.get('minute')
            hour = request.POST.get('hour')
            day_of_week = request.POST.get('day_of_week')
            day_of_month = request.POST.get('day_of_month')
            month_of_year = request.POST.get('month_of_year')
            CrontabSchedule.objects.create(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
            )
            return redirect('/crontab_schedule/')

    def crontab_edit(request, nid):
        if request.method == 'POST':
            minute = request.POST.get('minute')
            hour = request.POST.get('hour')
            day_of_week = request.POST.get('day_of_week')
            day_of_month = request.POST.get('day_of_month')
            month_of_year = request.POST.get('month_of_year')
            CrontabSchedule.objects.filter(id=nid).update(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
            )
        return redirect('/crontab_schedule/')

    def crontab_del(request, nid):
        if request.method == 'POST':
            print("tessssssss" + nid)
            CrontabSchedule.objects.filter(id=nid).delete()
            return redirect('/crontab_schedule/')

    #创建定时任务
    def create_PowerStatus(idName):
        print("start to create_PowerStatus")
        #定义一个时间间隔
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=300,
            period=IntervalSchedule.SECONDS,
        )
        print("start to try...except")
        #定义一个时间周期
        # schedule, _ = CrontabSchedule.objects.get_or_create(
        #     minute='30',
        #     hour='*',
        #     day_of_week='*',
        #     day_of_month='*',
        #     month_of_year='*',
        # )
        #创建一个周期性任务,如果查询到就返回，如果没查询到就向数据库加入新的对象
        try:
            print("------------do try----------")
            task, created = PeriodicTask.objects.get_or_create(
                #crontab=schedule,
                name=idName,
                task='HostManager.Tasks.powerStatus',
                interval=schedule,  # we created this above.
                args=json.dumps([idName]),
                # kwargs=json.dumps({
                #     'be_careful': True,
                # }),
                #expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
            )
            if created:
                task.enabled = True
                task.save()
            else:
                task.enabled = True
                task.save()
            return True
        except:
            print("------------do except------------")
            periodicTask = PeriodicTask.objects.get(name=idName)
            periodicTask.enabled = True  # 设置开启
            periodicTask.save()
            return True

        #开启任务

        #PeriodicTask.enabled = True
        print("----------------------------")

    #启动任务
    def enable_task(name):
        try:
            periodicTask = PeriodicTask.objects.get(name=name)
            periodicTask.enabled = True  # 设置开启
            periodicTask.save()
            return True
        except PeriodicTask.DoesNotExist:
            return True

    #关闭任务
    def disable_task(name):
        try:
            periodicTask = PeriodicTask.objects.get(name=name)
            periodicTask.enabled = False  # 设置关闭
            periodicTask.save()
            return True
        except PeriodicTask.DoesNotExist:
            return True

    #删除任务
    def delete_task(name):
        try:
            periodicTask = PeriodicTask.objects.get(name=name)
            periodicTask.delete()  # 设置删除
            return True
        except PeriodicTask.DoesNotExist:
            return True


class ClassCeleryResult:
    def task_result(request):
        if request.method == 'GET':
            return render(request, 'celery/result/task_result.html', {
            })

    def task_result_query(request):
        if request.method == 'GET':
            limit = request.GET.get('limit')  # how many items per page
            #print("the limit :"+limit)
            offset = request.GET.get(
                'offset')  # how many items in total in the DB
            #print("the offset :"+offset)
            search = request.GET.get('search')
            #print("the search :"+search)
            sort_column = request.GET.get('sort')  # which column need to sort
            print("the sort_column :" + sort_column)
            if sort_column:
                order = request.GET.get('order')  # ascending or descending
                print("the order :" + order)
                if order == "desc":
                    print("desc")
                    result_list = TaskResult.objects.all().order_by("-id")
                else:
                    print("asc")
                    result_list = TaskResult.objects.all().order_by(
                        sort_column)
            if search:  #    判断是否有搜索字
                result_list = TaskResult.objects.filter(
                    Q(id__icontains=search) | Q(status__icontains=search)
                    | Q(result__icontains=search)
                    | Q(date_done__icontains=search))
            else:
                result_list = TaskResult.objects.all(
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
                    "task_id":
                    item.task_id,
                    "status":
                    item.status,
                    "content_type":
                    item.content_type,
                    "content_encoding":
                    item.content_encoding,
                    "result":
                    item.result,
                    "date_done":
                    str(item.date_done),
                    "traceback":
                    item.traceback,
                    "hidden":
                    item.hidden,
                    "meta":
                    item.meta,
                })
            results_list_json = json.dumps(results_list_dict)
            print("the results_list_json:", type(results_list_json))
            return HttpResponse(
                results_list_json,
                content_type="application/json",
            )


# def sayHello(request):
#     """"""
#     # print('hello')
#     # time.sleep(5)
#     # print('work')
#     tasks.sayHello.delay() # 将任务教给celery执行
#     return HttpResponse('ok')


class ClassCeleryWorker():
    def __init__(self):
        self.powerOnTime = powerOnTime
        self.powerOffTime = powerOffTime

    def inspect_info(request):
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'celery/worker/inspect_info.html', {
                'obj': obj,
                'cluster_list': cluster_list,
            })
        if request.method == 'POST':
            roomNO = request.POST.get('roomNO')
            cabinetNO = request.POST.get('cabinetNO')
            bladeBoxNO = request.POST.get('bladeBoxNO')
            bladeNO = request.POST.get('bladeNO')
            hostName = request.POST.get('hostName')
            serviceIP = request.POST.get('serviceIP')
            manageIP = request.POST.get('manageIP')
            storageIP = request.POST.get('storageIP')
            clusterName = request.POST.get('clusterName')
            hardware = request.POST.get('hardware')
            service = request.POST.get('service')
            powerOnTime = request.POST.get('powerOnTime')
            powerOffTime = request.POST.get('powerOffTime')
            checkOnline = request.POST.get('checkOnline')
            runTime = request.POST.get('runTime')
            ipmiUser = request.POST.get('ipmiUser')
            ipmiPassword = request.POST.get('ipmiPassword')
            models.Host.objects.create(
                roomNO=roomNO,
                cabinetNO=cabinetNO,
                bladeBoxNO=bladeBoxNO,
                bladeNO=bladeNO,
                hostName=hostName,
                serviceIP=serviceIP,
                manageIP=manageIP,
                storageIP=storageIP,
                clusterName_id=clusterName,
                hardware=hardware,
                service=service,
                powerOnTime=powerOnTime,
                powerOffTime=powerOffTime,
                checkOnline=checkOnline,
                runTime=runTime,
                ipmiUser=ipmiUser,
                ipmiPassword=ipmiPassword,
            )
            print(roomNO, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/inspect_info/')

#@csrf_protect #为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件。
#@csrf_exempt #取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。

    def powerOn(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiIP = request.POST.get('IP')
            ipmiID = request.POST.get('ID')
            ipmiHost = ipmiIP
            print(ipmiIP)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)
            result = tasks.powerOn.delay(ipmiHost, ipmiUser,
                                         ipmiPassword).get()
            data = json.dumps(result).encode()
            print(result)
            print(ipmiID)
            if result[2] == "success":
                powerOnTime = result[1]
                models.Host.objects.filter(id=ipmiID).update(
                    powerOnTime=result[1], )
                models.HostPowerHistory.objects.create(
                    powerOnTimeHistory=result[1],
                    host_id=ipmiID,
                )
                models.Host.objects.filter(id=ipmiID).update(powerStatus=1, )
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)

    def powerOff(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiIP = request.POST.get('IP')
            ipmiHost = ipmiIP
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)
            result = tasks.powerOff.delay(ipmiHost, ipmiUser,
                                          ipmiPassword).get()
            print(result)
            print(type(result))
            if result[2] == "success":
                powerOnTime = db_dict['powerOnTime']
                powerOffTime = result[1]
                runTime = calculate.ClassCountCalculate.runTimeCalculate(
                    ipmiID, powerOnTime, powerOffTime)
                result.append(str(runTime))
                print(result)
                models.Host.objects.filter(id=ipmiID).update(
                    powerOffTime=result[1], )
                models.HostPowerHistory.objects.filter(
                    powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                        powerOffTimeHistory=result[1], )
                models.Host.objects.filter(id=ipmiID).update(powerStatus=0, )
            data = json.dumps(result).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)

    def powerCycle(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiIP = request.POST.get('IP')
            ipmiHost = ipmiIP
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)
            result = tasks.powerCycle.delay(ipmiHost, ipmiUser,
                                            ipmiPassword).get()
            data = json.dumps(result).encode()
            if result[2] == "success":
                print(result)
                powerOnTime = db_dict['powerOnTime']
                history_dict = models.HostPowerHistory.objects.filter(
                    powerOnTimeHistory=powerOnTime, host_id=ipmiID).values()[0]
                models.Host.objects.filter(id=ipmiID).update(
                    powerCycleTime=result[1])
                models.HostPowerHistory.objects.filter(
                    powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                        powerCycleTimes=int(history_dict['powerCycleTimes']) +
                        int(1))
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)


#批量开机函数

    def batchPowerOn(request):
        """"""
        #定义一个字典context
        context = {}
        #如果是POST请求
        if request.method == 'POST':
            #获取Jquery发送的allValue，并赋值
            allValue = request.POST.get('allValue')
            print(allValue)
            #切割字符串
            listAllValue = allValue.split("-")
            print(listAllValue)
            #定义一个列表listResult
            listResult = []
            #遍历列表
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiIP = dictAllValue['manageIP']
                print("this is ip" + ipmiIP)
                ipmiID = dictAllValue['ID']
                print(ipmiID)
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)
                ipmiHost = ipmiIP
                result = tasks.powerOn.delay(ipmiHost, ipmiUser,
                                             ipmiPassword).get()
                print("result")
                print(result)
                print(request)
                print(type(result))
                listResult.append(result)
                print(listResult)
                print(type(listResult))
                result.insert(0, ipmiID)
                if result[3] == "success":
                    powerOnTime = result[2]
                    #更新开机时间到主机信息表
                    models.Host.objects.filter(id=ipmiID).update(
                        powerOnTime=powerOnTime, )
                    #更新开机时间到历史记录表
                    models.HostPowerHistory.objects.create(
                        powerOnTimeHistory=powerOnTime,
                        host_id=ipmiID,
                    )
                    models.Host.objects.filter(id=ipmiID).update(
                        powerStatus=1, )
            data = json.dumps(listResult).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)

    def batchPowerOff(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))

                dictAllValue = eval(dictAllValue)
                ipmiIP = dictAllValue['manageIP']
                print("this is ip" + ipmiIP)
                ipmiID = dictAllValue['ID']
                print(ipmiID)
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                powerOnTime = db_dict['powerOnTime']
                print("powerOnTime:", powerOnTime)
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)
                ipmiHost = ipmiIP
                result = tasks.powerOff.delay(ipmiHost, ipmiUser,
                                              ipmiPassword).get()
                powerOffTime = result[1]

                print(request)
                print(type(result))

                listResult.append(result)

                print(listResult)
                print(type(listResult))

                runTime = calculate.ClassCountCalculate.runTimeCalculate(
                    ipmiID, powerOnTime, powerOffTime)
                result.append(str(runTime))
                result.insert(0, ipmiID)
                if result[3] == "success":
                    powerOffTime = result[2]
                    models.Host.objects.filter(id=ipmiID).update(
                        powerOffTime=powerOffTime, )
                    models.HostPowerHistory.objects.filter(
                        powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                            powerOffTimeHistory=powerOffTime, )
                    models.Host.objects.filter(id=ipmiID).update(
                        powerStatus=0, )
            data = json.dumps(listResult).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)

    def batchPowerCycle(request):
        """"""
        #定义一个字典context
        context = {}
        #如果是POST请求
        if request.method == 'POST':
            #获取Jquery发送的allValue，并赋值
            allValue = request.POST.get('allValue')
            print(allValue)
            #切割字符串
            listAllValue = allValue.split("-")
            print(listAllValue)
            #定义一个列表listResult
            listResult = []
            #遍历列表
            for dictAllValue in listAllValue:
                print(type(dictAllValue))

                dictAllValue = eval(dictAllValue)
                ipmiIP = dictAllValue['manageIP']
                print("this is ip" + ipmiIP)
                ipmiID = dictAllValue['ID']
                print(ipmiID)
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)
                ipmiHost = ipmiIP
                result = tasks.powerCycle.delay(ipmiHost, ipmiUser,
                                                ipmiPassword).get()
                print(request)
                print(type(result))
                listResult.append(result)
                print(listResult)
                print(type(listResult))
                if result[2] == "success":
                    powerOnTime = db_dict['powerOnTime']
                    history_dict = models.HostPowerHistory.objects.filter(
                        powerOnTimeHistory=powerOnTime,
                        host_id=ipmiID).values()[0]
                    models.Host.objects.filter(id=ipmiID).update(
                        powerCycleTime=result[1])
                    models.HostPowerHistory.objects.filter(
                        powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                            powerCycleTimes=int(
                                history_dict['powerCycleTimes']) + int(1))
            data = json.dumps(listResult).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'host_info.html', context)

    def batchInspectSdr(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))

                dictAllValue = eval(dictAllValue)
                ipmiIP = dictAllValue['manageIP']
                print("this is inspect ip" + ipmiIP)
                ipmiID = dictAllValue['ID']
                print(ipmiID)
                db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)
                ipmiHost = ipmiIP
                result = tasks.inspectSdr.delay(ipmiHost, ipmiUser,
                                                ipmiPassword).get()
                inspectTime = result[1]
                print(request)
                print(type(result))
                listResult.append(result)
                print(listResult)
                print(type(listResult))
                result.insert(0, ipmiID)
                powerOnTime = result[1]
                models.Automate.objects.filter(id=ipmiID).update(
                    inspectTime=result[2], )
            data = json.dumps(listResult).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'inspect_sdr.html', context)

    def inspectSdr(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiIP = request.POST.get('IP')
            ipmiHost = ipmiIP
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)
            result = tasks.inspectSdr.delay(ipmiHost, ipmiUser,
                                            ipmiPassword).get()
            data = json.dumps(result).encode()
            print(result)
            models.Automate.objects.filter(id=ipmiID).update(
                inspectTime=result[1], )
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'inspect_info.html', context)