"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
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
        ClassCeleryBeat.getPowerStatus()
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

    def getPowerStatus():
        #从数据库获得IP地址列表
        db_list = models.Host.objects.values("id", "manageIP", "ipmiUser","ipmiPassword")        
        #遍历列表获得内部字典
        for key_dict in db_list:
            #获取单条字典的对应值
            idName = key_dict['id']
            ipmiHost = key_dict['manageIP']            
            ipmiUser = key_dict['ipmiUser']            
            ipmiPassword = key_dict['ipmiPassword']
            #调用创建任务函数，并传参数
            ClassCeleryBeat.create_PowerStatus(idName, ipmiHost, ipmiUser,
                                        ipmiPassword)

    #创建定时任务
    def create_PowerStatus(idName, ipmiHost, ipmiUser, ipmiPassword):
        #定义一个时间间隔
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=180,
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
            args=json.dumps([ipmiHost, ipmiUser, ipmiPassword]),
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
            PeriodicTask = celery_models.PeriodicTask.objects.get(name=name)
            PeriodicTask.enabled = False  # 设置关闭
            PeriodicTask.save()
            return True
        except celery_models.PeriodicTask.DoesNotExist:
            return True


class ClassCeleryResult:
    def task_result(request):
        global GLOBAL_VAR_USER
        user_list = models.Users.objects.filter(
            username=GLOBAL_VAR_USER).first()
        if request.method == 'GET':
            # obj = django.dbmodel.django_celery_beat_crontabschedule.objects.all()
            results_list = TaskResult.objects.all().values()
            #results_list = results_list['id']
            print(type(results_list))
            results_list_json = serialize(
                'json', TaskResult.objects.all(), cls=ClassLazyEncoder)
            return render(
                request, 'celery/result/task_result.html', {
                    'results_list': results_list,
                    'user_list': user_list,
                    'results_list_json': results_list_json
                })

    def task_result_json(request):

        rows_list = []
        if request.method == 'GET':
            #serialize to json and indent.
            results_list_json = serialize(
                'json',
                TaskResult.objects.all(),
                cls=ClassLazyEncoder,
                skipkeys=True)
            #print(results_list_json)
            print(type(results_list_json))
            # for json to list
            results_list_list = json.loads(results_list_json)
            print(type(results_list_list))
            for i in results_list_list:
                #print ("序号：%s   值：%s" % (results_list_list.index(i) + 1, i))
                # for list to dict
                results_list_dict = i['fields']
                # add id to dict
                results_list_dict['id'] = i['pk']
                #print(results_list_dict)

                rows_list.append(results_list_dict)
            print(rows_list)
            total = len(rows_list)
            print(total)
            results_list_json = {"total": total, "rows": rows_list}
            # the below is for test data
            #results_list_json = {  "total": 800, "rows": [ {"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" },{"id": 0, "name": "Item 0", "price": "$0" }]}
            results_list_json = json.dumps(
                results_list_json, indent=4, separators=(',', ': '))

            print(type(results_list_json))
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

            powerOnTime = result[1]
            models.Host.objects.filter(id=ipmiID).update(
                powerOnTime=result[1], )
            models.HostPowerHistory.objects.create(
                powerOnTimeHistory=result[1],
                host_id=ipmiID,
            )
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
            powerOnTime = db_dict['powerOnTime']

            powerOffTime = result[1]
            runTime = ClassCeleryWorker.runTimeCalculate(
                ipmiID, powerOnTime, powerOffTime)
            result.append(str(runTime))
            print(result)
            models.Host.objects.filter(id=ipmiID).update(
                powerOffTime=result[1], )
            models.HostPowerHistory.objects.filter(
                powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                    powerOffTimeHistory=result[1], )
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
        models.Host.objects.filter(id=ipmiID).update(runTime=str(runTime), )
        models.HostPowerHistory.objects.filter(
            powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                runTimeHistory=str(runTime), )
        return (runTime)


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
                print(request)
                print(type(result))

                listResult.append(result)

                print(listResult)
                print(type(listResult))

                result.insert(0, ipmiID)
                powerOnTime = result[1]
                models.Host.objects.filter(id=ipmiID).update(
                    powerOnTime=result[2], )
                models.HostPowerHistory.objects.create(
                    powerOnTimeHistory=result[2],
                    host_id=ipmiID,
                )
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

                runTime = ClassCeleryWorker.runTimeCalculate(
                    ipmiID, powerOnTime, powerOffTime)
                result.append(str(runTime))
                result.insert(0, ipmiID)
                powerOffTime = result[1]
                models.Host.objects.filter(id=ipmiID).update(
                    powerOffTime=result[2], )
                models.HostPowerHistory.objects.filter(
                    powerOnTimeHistory=powerOnTime, host_id=ipmiID).update(
                        powerOffTimeHistory=result[2], )
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
