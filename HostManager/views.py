from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from HostManager import models
from celery import shared_task
from celery import task
from HostManager import tasks
from celery import app
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
                                    service=service,)
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

def powerOn(request):
    """"""
    # print('hello')
    # time.sleep(5)
    # print('work')
    #app.task('test_cmd.excute', args=['ls /'], queue='test_cmd')
    #tasks.excute('test_cmd.excute', args=['ls /'], queue='test_cmd') # 将任务教给celery执行
    tasks.powerOn.delay()
    return HttpResponse('ok')

def powerOff(request):
    """"""
    # print('hello')
    # time.sleep(5)
    # print('work')
    #app.task('test_cmd.excute', args=['ls /'], queue='test_cmd')
    #tasks.excute('test_cmd.excute', args=['ls /'], queue='test_cmd') # 将任务教给celery执行
    tasks.powerOff.delay()
    return HttpResponse('ok')

# def index(req):
#     print(req.GET.get('url'))
#     if req.GET.get('url')=='power_off':
#         return HttpResponse("hello,this is a test")
#     else:
#         return HttpResponse("hahahaha")