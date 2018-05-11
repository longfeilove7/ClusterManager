from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from HostManager import models
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
        group_list = models.Groups.objects.all()
        return render(request, 'host_info.html', {'obj': obj, 'group_list': group_list})
    if request.method == 'POST':
        hostName = request.POST.get('hostName')
        serviceIP = request.POST.get('serviceIP')
        manageIP = request.POST.get('manageIP')
        storageIP = request.POST.get('storageIP')
        hostGroup = request.POST.get('hostGroup')
        hardware = request.POST.get('hardware')
        service = request.POST.get('service')
        models.Host.objects.create(hostName=hostName,
                                   serviceIP=serviceIP,
                                   manageIP=manageIP,
                                   storageIP=storageIP,
                                   hostGroup_id=hostGroup,
                                   hardware=hardware,
                                   service=service,)
        print(hardware,serviceIP,manageIP,storageIP,hostName,service,hostGroup)
        return redirect('/host_info/')


def add_group(request):
    if request.method == 'GET':
        group_list = models.Groups.objects.all()
        return render(request, 'add_group.html', {'group_list': group_list})
    elif request.method == 'POST':
        groupName = request.POST.get('groupName')
        models.Groups.objects.create(hostGroup=groupName)
        return redirect('/add_group/')


def host_del(request, nid):
    if request.method == 'POST':
        models.Host.objects.filter(id=nid).delete()
        return redirect('/host_info/')


def host_edit(request, nid):
    if request.method == 'GET':
        host_obj = models.Host.objects.filter(id=nid)
        group_list = models.Groups.objects.all()
        return render(request, 'host_edit.html', {'host_obj': host_obj, 'group_list': group_list})
    if request.method == 'POST':
        hostName = request.POST.get('hostName')
        serviceIP = request.POST.get('serviceIP')
        manageIP = request.POST.get('manageIP')
        storageIP = request.POST.get('storageIP')
        hostGroup = request.POST.get('hostGroup')
        hardware = request.POST.get('hardware')
        service = request.POST.get('service')
        models.Host.objects.filter(id=nid).update(hostName=hostName,
                                                  serviceIP=serviceIP,
                                                  manageIP=manageIP,
                                                  storageIP=storageIP,
                                                  hostGroup_id=hostGroup,
                                                  hardware=hardware,
                                                  service=service,)
        print(hardware, serviceIP, manageIP, storageIP, hostName, service, hostGroup)
        return redirect('/host_info/')


def group_edit(request, nid):
    if request.method == 'POST':
        groupName = request.POST.get('groupName')
        models.Groups.objects.filter(id=nid).update(hostGroup=groupName)
        print(groupName)
        return redirect('/add_group/')


def group_del(request, nid):
    if request.method == 'POST':
        obj = models.Host.objects.filter(hostGroup_id=nid).first()
        if obj:
            return HttpResponse('该主机组已经被使用')
        else:
            models.Groups.objects.filter(id=nid).delete()
            return redirect('/add_group/')
