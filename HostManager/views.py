"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
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
#import os, sys, commands
# Create your views here.

#定义全局变量用于存储页面当前用户信息
GLOBAL_VAR_USER = "0"


#自定义类转化django数据库to JSON，以支持想要的时间格式
class ClassLazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)


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


#系统注册函数

    def signup(request):
        #如果是POST请求
        if request.method == "POST":
            #通过django的request.POST.get()获取用户名
            GLOBAL_VAR_USER = request.POST.get('user')
            #通过django的request.POST.get()获取密码
            local_var_password = request.POST.get('pwd')
            #根据用户名和密码创建用户信息
            models.Users.objects.create(
                username=GLOBAL_VAR_USER, password=local_var_password)
            #返回注册成功页面
            return render(request, 'sucess.html')
        else:
            #返回用户注册页面
            return render(request, 'sign-up.html')

    def index(request):
        #声明使用全局变量
        global GLOBAL_VAR_USER
        #查询数据库用户名
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        #返回index页面
        return render(request, 'index.html', {'user_list': user_list})


class ClassHost:
    def host_info(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'host_info.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })

    def add_host(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'add_host.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
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
            return redirect('/add_host/')

    def host_del(request, nid):
        if request.method == 'POST':
            models.Host.objects.filter(id=nid).delete()
            return redirect('/add_host/')

    def host_edit(request, nid):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            cluster_list = models.Clusters.objects.all()
            return render(
                request, 'host_edit.html', {
                    'host_obj': host_obj,
                    'cluster_list': cluster_list,
                    'user_list': user_list
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
            ipmiUser = request.POST.get('ipmiUser')
            ipmiPassword = request.POST.get('ipmiPassword')
            models.Host.objects.filter(id=nid).update(
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
                ipmiUser=ipmiUser,
                ipmiPassword=ipmiPassword,
            )
            print(roomNO, cabinetNO, bladeBoxNO, bladeNO, hardware, serviceIP,
                  manageIP, storageIP, hostName, service, clusterName)
            return redirect('/add_host/')

    def power_history(request, nid):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            host_obj = models.Host.objects.filter(id=nid)
            history_list = models.HostPowerHistory.objects.filter(host_id=nid)
            cluster_list = models.Clusters.objects.all()
            return render(
                request, 'power_history.html', {
                    'history_list': history_list,
                    'user_list': user_list,
                    'cluster_list': cluster_list
                })


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


# for celery beat about html
class ClassCeleryBeat():
    def periodic_task(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            periodic_list = PeriodicTask.objects.all()
            return render(request, 'celery/beat/periodic_task.html', {
                'periodic_list': periodic_list,
                'user_list': user_list
            })

    def add_periodic(request):
        if request.method == 'POST':
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

            return redirect('/periodic_task/')

    def interval_schedule(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            interval_list = IntervalSchedule.objects.all()
            return render(request, 'celery/beat/interval_schedule.html', {
                'interval_list': interval_list,
                'user_list': user_list
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
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            solar_list = SolarSchedule.objects.all()
            return render(request, 'celery/beat/solar_schedule.html', {
                'solar_list': solar_list,
                'user_list': user_list
            })

    def crontab_schedule(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            crontab_list = CrontabSchedule.objects.all()
            return render(request, 'celery/beat/crontab_schedule.html', {
                'crontab_list': crontab_list,
                'user_list': user_list
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
    def create_PowerStatus(idName, ipmiHost, ipmiUser, ipmiPassword):
        #定义一个时间间隔
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=300,
            period=IntervalSchedule.SECONDS,
        )
        #定义一个时间周期
        # schedule, _ = CrontabSchedule.objects.get_or_create(
        #     minute='30',
        #     hour='*',
        #     day_of_week='*',
        #     day_of_month='*',
        #     month_of_year='*',
        # )
        #创建一个周期性任务,如果查询到就返回，如果没查询到就向数据库加入新的对象
        PeriodicTask.objects.get_or_create(
            #crontab=schedule,
            name=idName,
            task='HostManager.Tasks.powerStatus',
            interval=schedule,  # we created this above.
            args=json.dumps([idName, ipmiHost, ipmiUser, ipmiPassword]),
            # kwargs=json.dumps({
            #     'be_careful': True,
            # }),
            #expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        )
        #开启任务
        PeriodicTask.enabled = True

    #关闭任务
    def disable_task(name):
        try:
            periodicTask = PeriodicTask.objects.get(name=name)
            periodicTask.enabled = False  # 设置关闭
            periodicTask.save()
            return True
        except PeriodicTask.DoesNotExist:
            return True

    #关闭任务
    def delete_task(name):
        try:
            periodicTask = PeriodicTask.objects.get(name=name)
            periodicTask.delete()  # 设置删除
            return True
        except PeriodicTask.DoesNotExist:
            return True


class ClassCeleryResult:
    def task_result(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            return render(request, 'celery/result/task_result.html', {
                'user_list': user_list,
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
            #sort_column = request.GET.get('sort')   # which column need to sort
            #print("the sort_column :"+sort_column)
            order = request.GET.get('order')  # ascending or descending
            #print("the order :"+order)
            if search:  #    判断是否有搜索字
                result_list = TaskResult.objects.filter(
                    id=search, status=search, result=search)
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
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'celery/worker/inspect_info.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
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
                runTime = ClassCountCalculate.runTimeCalculate(
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

                runTime = ClassCountCalculate.runTimeCalculate(
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


class ClassCountCalculate():
    def runTimeCalculate(ipmiID, powerOnTime, powerOffTime):
        """"""
        db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
        db_tuple = models.Host.objects.filter().values_list()[0]
        print(db_dict)
        print(db_tuple)
        print(db_dict['powerOnTime'])
        print(db_dict['powerOffTime'])
        print(powerOffTime)
        #offset-naive是不含时区的类型，而offset-aware是有时区类型
        runTime = datetime.datetime.strptime(
            powerOffTime, '%Y-%m-%d %H:%M:%S'
        ) - db_dict['powerOnTime'].replace(tzinfo=None) - datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=8,
            weeks=0)
        print(runTime)
        models.Host.objects.filter(id=ipmiID).update(runTime=runTime)
        models.HostPowerHistory.objects.filter(
            powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                runTimeHistory=runTime, )
        return (runTime)

    def countRunTimeCalculate(ipmiID):
        """"""
        # to calculate the all runtimehistory
        db_list = models.HostPowerHistory.objects.filter(
            host_id=ipmiID).values("host_id", "runTimeHistory")
        print(db_list)
        listRunTimeHistory = []
        #遍历列表获得内部字典
        for key_dict in db_list:
            #获取单条字典的对应值
            host_id = key_dict['host_id']
            runTimeHistory = key_dict['runTimeHistory']
            # set the not null to a list
            if runTimeHistory is not None:
                #print(runTimeHistory)
                listRunTimeHistory.append(runTimeHistory)
        #print(listRunTimeHistory)
        #print(type(listRunTimeHistory))
        countRunTimeHistory = datetime.timedelta(0, 0)
        for x in listRunTimeHistory:
            countRunTimeHistory += x
        # models.Host.objects.filter(id=ipmiID).update(runTime=str(runTime), )
        # models.HostPowerHistory.objects.filter(
        #     powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
        #         runTimeHistory= runTime )
        return (countRunTimeHistory)


class ClassBillingSystem():
    def billingInfo(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            #filter the billing value equal 1
            host = models.Host.objects.filter(billingStatus=1)
            #obj =  host.annotate(countPowerOnHour=5*Count("checkpoweron")/60).annotate(countPowerOffHour=5*Count("checkpoweroff")/60).annotate(countPowerFailHour=5*Count("checkpowerfail")/60).annotate(countPowerOnMinute=5*Count("checkpoweron")%60).annotate(countPowerOffMinute=5*Count("checkpoweroff")%60).annotate(countPowerFailMinute=5*Count("checkpowerfail")%60)
            #设置每台机器1小时的租用价格
            price = str(5)
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
                'cluster_list': cluster_list,
                'user_list': user_list
            })

    def billingDevice(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'billing_device.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })
# the billing price function

    def billingPrice(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            billing_list = models.Billing.objects.all()
            return render(
                request, 'billing_price.html', {
                    'obj': obj,
                    'cluster_list': cluster_list,
                    'user_list': user_list,
                    'billing_list': billing_list
                })

# the billing switch button function

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

    def batchBillingAdd(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listBilling = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiID = dictAllValue['ID']
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

    def batchBillingDelete(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listBilling = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiID = dictAllValue['ID']
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


class ClassMonitorSystem():
    #定义查询时间，如果在方法中定义会出现第二次调用方法时变量又重新初始化
    strStartTime = "0000-00-00 00:00:00"
    strEndTime = "0000-00-00 00:00:00"

    def monitorInfo(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            return render(request, 'monitor_info.html',
                          {'user_list': user_list})

    def monitorInfoQuery(request): 
        #每次request的时候POST提交的数据会丢失，所以采用类变量暂存      
        strStartTime = ClassMonitorSystem.strStartTime
        strEndTime = ClassMonitorSystem.strEndTime

        if request.method == 'GET':
            print("2222222222222222222")
            print(strStartTime)
            print(strEndTime)
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
            #print("the offset :"+offset)
            search = request.GET.get('search')
            print("the search :"+search,type(search))

            #sort_column = request.GET.get('sort')   # which column need to sort
            #print("the sort_column :"+sort_column)
            order = request.GET.get('order')  # ascending or descending
            #print("the order :"+order)
            if search:  #    判断是否有搜索字
                query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1 AND id like \'"+"%%"+search+"%%\'" +" OR manageIP like "+ "\'%%"+search+"%%\'" +" OR serviceIP like "+ "\'%%"+search+"%%\'" +" OR storageIP like "+ "\'%%"+search+"%%"+"\' ) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP"
                
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
                limit = 15  # 默认是每页20行的内容，与前端默认行数一致
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
                    '%s:%s:00' %
                    (str(item.countPowerOnHour + item.countPowerOffHour +
                         item.countPowerFailHour).zfill(2),
                     str(item.countPowerOnMinute + item.countPowerOffMinute +
                         item.countPowerFailMinute).zfill(2)),
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
        if request.method == 'POST':
            strStartTime = request.POST.get('startDateTime')
            strEndTime = request.POST.get('endDateTime')
            startTime = datetime.datetime.strptime(strStartTime,
                                                   '%Y-%m-%d %H:%M:%S')
            endTime = datetime.datetime.strptime(strEndTime,
                                                 '%Y-%m-%d %H:%M:%S')
            print("the startTime", startTime, type(startTime))
            users_timezone = pytz.timezone('Asia/Shanghai')
            print(users_timezone)
            utcStartTime = startTime.replace(tzinfo=None)
            print(utcStartTime)
            ClassMonitorSystem.strStartTime = request.POST.get('startDateTime')
            ClassMonitorSystem.strEndTime = request.POST.get('endDateTime')
            print("111111111111111111111111111111111")
            data = json.dumps("listBilling").encode()
            return HttpResponse(data)

    def monitorDevice(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            return render(request, 'monitor_device.html', {
                'obj': obj,
                'cluster_list': cluster_list,
                'user_list': user_list
            })
# the monitor price function

    def monitorPrice(request):
        """"""
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            obj = models.Host.objects.all()
            cluster_list = models.Clusters.objects.all()
            monitor_list = models.monitor.objects.all()
            return render(
                request, 'monitor_price.html', {
                    'obj': obj,
                    'cluster_list': cluster_list,
                    'user_list': user_list,
                    'monitor_list': monitor_list
                })

# the monitor switch button function

    def monitorSwitch(request):
        """"""
        context = {}
        if request.method == 'POST':
            ipmiID = request.POST.get('ID')
            #print(ipmiID)
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
                ClassCeleryBeat.create_PowerStatus(idName, ipmiHost, ipmiUser,
                                                   ipmiPassword)
            #if the setValue equal 0 then to stop beat
            elif setValue == "0":
                ClassCeleryBeat.disable_task(idName)
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)

# the batch add monitor button function

    def batchMonitorAdd(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiID = dictAllValue['ID']
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
                ClassCeleryBeat.create_PowerStatus(idName, ipmiHost, ipmiUser,
                                                   ipmiPassword)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)

# the batch Pause monitor function

    def batchMonitorPause(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiID = dictAllValue['ID']
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
                ClassCeleryBeat.disable_task(idName)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)

# the batch delete monitor function

    def batchMonitorDelete(request):
        """"""
        context = {}
        if request.method == 'POST':
            allValue = request.POST.get('allValue')
            print(allValue)
            listAllValue = allValue.split("-")
            print(listAllValue)
            listResult = []
            setValue = request.POST.get('setValue')
            print(setValue)
            listMonitor = []
            for dictAllValue in listAllValue:
                print(type(dictAllValue))
                dictAllValue = eval(dictAllValue)
                ipmiID = dictAllValue['ID']
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
                ClassCeleryBeat.delete_task(idName)
            data = json.dumps(listMonitor).encode()
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()
        else:
            return render(request, 'monitor_device.html', context)


# the batch add monitor button function

    def monitorTimeQuery(request):
        """"""
        print("333333333333333333333333333333333")
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        context = {}
        if request.method == 'POST':
            strStartTime = request.POST.get('startDateTime')
            print(strStartTime)
            strEndTime = request.POST.get('endDateTime')
            query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP"
            #mysql 取书整floor(number),除法取整，x div y ,除法取余数, x mod y,四舍五入，round
        query = "SELECT id,ifnull(countPowerOffHour,0) AS countPowerOffHour,ifnull(countPowerOffMinute,0) AS countPowerOffMinute,ifnull(countPowerOnHour,0) AS countPowerOnHour,ifnull(countPowerOnMinute,0) AS countPowerOnMinute,ifnull(countPowerFailHour,0) AS countPowerFailHour,ifnull(countPowerFailMinute,0) AS countPowerFailMinute FROM (SELECT * FROM ((SELECT * FROM hostmanager_host WHERE monitorstatus=1) AS a) LEFT JOIN (SELECT checkHost_id AS OFF_id,(COUNT(*)-1)*5 div 60 as countPowerOffHour,(COUNT(*)-1)*5 mod 60 as countPowerOffMinute FROM hostmanager_checkpoweroff WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as b on a.id=b.OFF_id LEFT JOIN (SELECT checkHost_id AS ON_id,(COUNT(*)-1)*5 div 60 as countPowerOnHour,(COUNT(*)-1)*5 mod 60 as countPowerOnMinute FROM hostmanager_checkpoweron WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as c on a.id=c.ON_id LEFT JOIN (SELECT checkHost_id AS FAIL_id,(COUNT(*)-1)*5 div 60 as countPowerFailHour,(COUNT(*)-1)*5 mod 60 as countPowerFailMinute FROM hostmanager_checkpowerfail WHERE checktime<'" + strEndTime + "' AND checktime>'" + strStartTime + "'  GROUP BY checkhost_id) as d on a.id=d.FAIL_id) AS TEMP"
        limit = request.GET.get('limit')  # how many items per page
        #print("the limit :"+limit)
        offset = request.GET.get('offset')  # how many items in total in the DB
        #print("the offset :"+offset)
        search = request.GET.get('search')
        #print("the search :"+search)
        #sort_column = request.GET.get('sort')   # which column need to sort
        #print("the sort_column :"+sort_column)
        order = request.GET.get('order')  # ascending or descending
        #print("the order :"+order)
        if search:  #    判断是否有搜索字
            info_list = TaskResult.objects.filter(
                id=search, status=search, result=search)
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
                "countMonitorTime":
                str(item.countPowerOnHour + item.countPowerOffHour +
                    item.countPowerFailHour) + ":" +
                str(item.countPowerOnMinute + item.countPowerOffMinute +
                    item.countPowerFailMinute) + "'",
                "countPowerOnTime":
                str(item.countPowerOnHour) + ":" + str(item.countPowerOnMinute)
                + "'",  #将表格中小时和分钟列以字符串合并            
                "countPowerOffTime":
                str(item.countPowerOffHour) + ":" + str(
                    item.countPowerOffMinute) + "'",
                "countPowerFailTime":
                str(item.countPowerFailHour) + ":" + str(
                    item.countPowerFailMinute) + "'"
            })
        info_list_json = json.dumps(info_list_dict)
        print("the info_list_json:", type(info_list_json))
        return HttpResponse(
            info_list_json,
            content_type="application/json",
        )
data = [[1, 2, 3], [4, 5, 6]]


class UploadFileForm(forms.Form):
    file = forms.FileField()


# Create your views here.
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(
                filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request, 'upload_form.html', {
            'form':
            form,
            'title':
            'Excel file upload and download example',
            'header':
            ('Please choose any excel file ' + 'from your cloned repository:')
        })


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(data, file_type, file_name=file_name)


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            Question, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Question, Choice], 'xls', file_name="book")
    elif atype == "custom":
        question = Question.objects.get(slug='ide')
        query_sets = Choice.objects.filter(question=question)
        column_names = ['choice_text', 'id', 'votes']
        return excel.make_response_from_query_sets(
            query_sets, column_names, 'xls', file_name="custom")
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[['question_text', 'pub_date', 'slug'],
                          ['question', 'choice_text', 'votes']])
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request, 'upload_form.html', {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=2,
                model=Question,
                mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})


def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()


def parse(request, data_struct_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        if data_struct_type == "array":
            return JsonResponse({"result": filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records":
            return JsonResponse({"result": filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def handson_table(request):
    return excel.make_response_from_tables([Question, Choice],
                                           'handsontable.html')


def embed_handson_table(request):
    """
    Renders two table in a handsontable
    """
    content = excel.pe.save_book_as(
        models=[Question, Choice],
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(request, 'custom-handson-table.html',
                  {'handsontable_content': content.read()})


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Question, dest_file_type='handsontable.html', dest_embed=True)
    content.seek(0)
    return render(request, 'custom-handson-table.html',
                  {'handsontable_content': content.read()})


def survey_result(request):
    question = Question.objects.get(slug='ide')
    query_sets = Choice.objects.filter(question=question)
    column_names = ['choice_text', 'votes']

    # Obtain a pyexcel sheet from the query sets
    sheet = excel.pe.get_sheet(
        query_sets=query_sets, column_names=column_names)
    sheet.name_columns_by_row(0)
    sheet.column.format('votes', int)

    # Transform the sheet into an svg chart
    svg = excel.pe.save_as(
        array=[sheet.column['choice_text'], sheet.column['votes']],
        dest_file_type='svg',
        dest_chart_type='pie',
        dest_title=question.question_text,
        dest_width=600,
        dest_height=400)

    return render(request, 'survey_result.html', dict(svg=svg.read()))


def import_sheet_using_isave_to_database(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES['file'].isave_to_database(
                model=Question, mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})


def import_data_using_isave_book_as(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES['file'].isave_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[['question_text', 'pub_date', 'slug'],
                          ['question', 'choice_text', 'votes']])
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request, 'upload_form.html', {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_without_bulk_save(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[['question_text', 'pub_date', 'slug'],
                          ['question', 'choice_text', 'votes']],
                bulk_save=False)
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request, 'upload_form.html', {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })
