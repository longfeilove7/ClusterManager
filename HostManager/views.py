from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from HostManager import models
from celery import shared_task
from celery import task
from HostManager import tasks
from celery import app
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
#import os, sys, commands
# Create your views here.


def login(request):
    if request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        obj = models.Users.objects.filter(username=u, password=p).first()
        if obj:
            return render(request, 'index.html', {'obj': obj})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        models.Users.objects.create(username=u, password=p)
        return render(request, 'sucess.html')
    else:
        return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')


def host_info(request):
    if request.method == 'GET':
        obj = models.Host.objects.all()
        cluster_list = models.Clusters.objects.all()
        return render(request, 'host_info.html', {'obj': obj, 'cluster_list': cluster_list})
    if request.method == 'POST':
        roomNO = request.POST.get('roomNO')
        cabinetNO = request.POST.get('cabinetNO')
        bladeBoxNO = request.POST.get('bladeBoxNO')
        bladeNO = request.POST.get('bladeNO')
        hostName = request.POST.get('hostName')
        serviceIP = request.POST.get('serviceIP')
        manageIP = request.POST.get('manageIP')
        storageIP = request.POST.get('storageIP')
        hostCluster = request.POST.get('hostCluster')
        hardware = request.POST.get('hardware')
        service = request.POST.get('service')
        powerOnTime = request.POST.get('powerOnTime')
        powerOffTime = request.POST.get('powerOffTime')
        checkOnline = request.POST.get('checkOnline')
        runTime = request.POST.get('runTime')
        models.Host.objects.create(
                                    roomNO=roomNO,
                                    cabinetNO=cabinetNO,
                                    bladeBoxNO=bladeBoxNO,
                                    bladeNO=bladeNO,
                                    hostName=hostName,
                                    serviceIP=serviceIP,
                                    manageIP=manageIP,
                                    storageIP=storageIP,
                                    hostCluster_id=hostCluster,
                                    hardware=hardware,
                                    service=service,
                                    powerOnTime=powerOnTime,
                                    powerOffTime=powerOffTime,
                                    checkOnline=checkOnline,
                                    runTime=runTime,)
        print(roomNO,cabinetNO,bladeBoxNO,bladeNO,hardware,serviceIP,manageIP,storageIP,hostName,service,hostCluster)
        return redirect('/host_info/')


def add_cluster(request):
    if request.method == 'GET':
        cluster_list = models.Clusters.objects.all()
        return render(request, 'add_cluster.html', {'cluster_list': cluster_list})
    elif request.method == 'POST':
        clusterName = request.POST.get('clusterName')
        models.Clusters.objects.create(hostCluster=clusterName)
        return redirect('/add_cluster/')


def host_del(request, nid):
    if request.method == 'POST':
        models.Host.objects.filter(id=nid).delete()
        return redirect('/host_info/')


def host_edit(request, nid):
    if request.method == 'GET':
        host_obj = models.Host.objects.filter(id=nid)
        cluster_list = models.Clusters.objects.all()
        return render(request, 'host_edit.html', {'host_obj': host_obj, 'cluster_list': cluster_list})
    if request.method == 'POST':
        roomNO = request.POST.get('roomNO')
        cabinetNO = request.POST.get('cabinetNO')
        bladeBoxNO = request.POST.get('bladeBoxNO')
        bladeNO = request.POST.get('bladeNO')
        hostName = request.POST.get('hostName')
        serviceIP = request.POST.get('serviceIP')
        manageIP = request.POST.get('manageIP')
        storageIP = request.POST.get('storageIP')
        hostCluster = request.POST.get('hostCluster')
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
                                                    hostCluster_id=hostCluster,
                                                    hardware=hardware,
                                                    service=service,)
        print(roomNO,cabinetNO,bladeBoxNO,bladeNO,hardware,serviceIP,manageIP,storageIP,hostName,service,hostCluster)
        return redirect('/host_info/')


def cluster_edit(request, nid):
    if request.method == 'POST':
        clusterName = request.POST.get('clusterName')
        models.Clusters.objects.filter(id=nid).update(hostCluster=clusterName)
        print(clusterName)
        return redirect('/add_cluster/')


def cluster_del(request, nid):
    if request.method == 'POST':
        obj = models.Host.objects.filter(hostCluster_id=nid).first()
        if obj:
            return HttpResponse('该主机组已经被使用')
        else:
            models.Clusters.objects.filter(id=nid).delete()
            return redirect('/add_cluster/')

# def sayHello(request):
#     """"""
#     # print('hello')
#     # time.sleep(5)
#     # print('work')
#     tasks.sayHello.delay() # 将任务教给celery执行
#     return HttpResponse('ok')

class TasksClass():
    def __init__(self):
        self.powerOnTime = powerOnTime
        self.powerOffTime = powerOffTime
#@csrf_protect #为当前函数强制设置防跨站请求伪造功能，即便settings中没有设置全局中间件。
#@csrf_exempt #取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
    def powerOn(request):
        """"""
        context = {}
        if  request.method == 'POST':   
            ipmiIP = request.POST.get('IP')               
            ipmiHost = ipmiIP        
            result = tasks.powerOn.delay(ipmiHost).get()
            data=json.dumps(result).encode()        
            print(result)        
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            powerOnTime = result[1]
            models.Host.objects.filter(id=ipmiID).update(
                powerOnTime = result[1],
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
        if  request.method == 'POST':           
            ipmiIP = request.POST.get('IP')        
            ipmiHost = ipmiIP
            result = tasks.powerOff.delay(ipmiHost).get()                    
            print(result)
            print(type(result))
                                      
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            powerOffTime = result[1]
            runTime = TasksClass.runTimeCalculate(ipmiID,powerOffTime)
            result.append(str(runTime))
            print(result)
            models.Host.objects.filter(id=ipmiID).update(                
                powerOffTime = result[1],
            )            
            data=json.dumps(result).encode()           
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()        
        else:
            return render(request, 'host_info.html', context)

    def powerCycle(request):
        """"""
        context = {}
        if  request.method == 'POST':           
            ipmiIP = request.POST.get('IP')        
            ipmiHost = ipmiIP
            result = tasks.powerCycle.delay(ipmiHost).get()
            data=json.dumps(result).encode()        
            print(result)              
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            models.Host.objects.filter(id=ipmiID).update(
                powerOnTime = result[1],
            )
            return HttpResponse(data)
        elif request.method == 'GET':
            print(request.GET)
            return ()        
        else:
            return render(request, 'host_info.html', context)

    def runTimeCalculate(ipmiID,powerOffTime):
        """"""     
        db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
        db_tuple = models.Host.objects.filter().values_list()[0]
        print(db_dict)
        print(db_tuple)
        print(db_dict['powerOnTime'])
        print(db_dict['powerOffTime'])
        print(powerOffTime)
        runTime = datetime.datetime.strptime(powerOffTime,'%Y-%m-%d %H:%M:%S') - db_dict['powerOnTime']            
        print(runTime)        
        models.Host.objects.filter(id=ipmiID).update(
            runTime = str(runTime),                       
            )               
        return  (runTime)

    def batchPowerOn(request):        
        """"""
        context = {}
        if  request.method == 'POST':   
            ipmiIP = request.POST.get('IP')               
            ipmiHost = ipmiIP        
            result = tasks.powerOn.delay(ipmiHost).get()
            data=json.dumps(result).encode()        
            print(result)        
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            powerOnTime = result[1]
            models.Host.objects.filter(id=ipmiID).update(
                powerOnTime = result[1],
            )
            return HttpResponse(data)     
        elif request.method == 'GET':
            print(request.GET)
            return ()        
        else:
            return render(request, 'host_info.html', context)
