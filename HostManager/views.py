from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseBadRequest
from HostManager import models
from celery import shared_task
from celery import task
from HostManager import tasks
from celery import app
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
#import django_excel as excel
from HostManager.models import Question, Choice, Host, Clusters
from django import forms
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
            ipmiID = request.POST.get('ID')               
            ipmiHost = ipmiIP
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)        
            result = tasks.powerOn.delay(ipmiHost,ipmiUser,ipmiPassword).get()
            data=json.dumps(result).encode()        
            print(result)            
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
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)        
            result = tasks.powerOff.delay(ipmiHost,ipmiUser,ipmiPassword).get()                    
            print(result)
            print(type(result))
                                      
            
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
            ipmiID = request.POST.get('ID')
            print(ipmiID)
            db_dict = models.Host.objects.filter(id=ipmiID).values()[0]
            ipmiUser = db_dict['ipmiUser']
            print(ipmiUser)
            ipmiPassword = db_dict['ipmiPassword']
            print(ipmiPassword)        
            result = tasks.powerCycle.delay(ipmiHost,ipmiUser,ipmiPassword).get()
            data=json.dumps(result).encode()        
            print(result)              
            
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
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)                   
                ipmiHost = ipmiIP        
                result = tasks.powerOn.delay(ipmiHost,ipmiUser,ipmiPassword).get()
                print(request)
                print(type(result))
                
                listResult.append(result)
                
                print(listResult)       
                print(type(listResult))        
               
                result.insert(0,ipmiID)
                powerOnTime = result[1]
                models.Host.objects.filter(id=ipmiID).update(
                    powerOnTime = result[2],
                )
            data=json.dumps(listResult).encode()    
            return HttpResponse(data)     
        elif request.method == 'GET':
            print(request.GET)
            return ()        
        else:
            return render(request, 'host_info.html', context)

    def batchPowerOff(request):        
        """"""
        context = {}
        if  request.method == 'POST':   
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
                ipmiUser = db_dict['ipmiUser']
                print(ipmiUser)
                ipmiPassword = db_dict['ipmiPassword']
                print(ipmiPassword)                   
                ipmiHost = ipmiIP        
                result = tasks.powerOff.delay(ipmiHost,ipmiUser,ipmiPassword).get()
                powerOffTime = result[1]                
                
                print(request)
                print(type(result))
                
                listResult.append(result)
                
                print(listResult)       
                print(type(listResult))        
               
                runTime = TasksClass.runTimeCalculate(ipmiID,powerOffTime)
                result.append(str(runTime))
                result.insert(0,ipmiID)
                powerOffTime = result[1]
                models.Host.objects.filter(id=ipmiID).update(
                    powerOffTime = result[2],
                )
            data=json.dumps(listResult).encode()    
            return HttpResponse(data)     
        elif request.method == 'GET':
            print(request.GET)
            return ()        
        else:
            return render(request, 'host_info.html', context)

data = [
    [1, 2, 3],
    [4, 5, 6]
]


class UploadFileForm(forms.Form):
    file = forms.FileField()


# Create your views here.
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Excel file upload and download example',
            'header': ('Please choose any excel file ' +
                       'from your cloned repository:')
        })


def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(
        data, file_type, file_name=file_name)


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
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
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
    return render(
        request,
        'upload_form.html',
        {'form': form})


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
    return excel.make_response_from_tables(
        [Question, Choice], 'handsontable.html')


def embed_handson_table(request):
    """
    Renders two table in a handsontable
    """
    content = excel.pe.save_book_as(
        models=[Question, Choice],
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Question,
        dest_file_type='handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


def survey_result(request):
    question = Question.objects.get(slug='ide')
    query_sets = Choice.objects.filter(question=question)
    column_names = ['choice_text', 'votes']

    # Obtain a pyexcel sheet from the query sets
    sheet = excel.pe.get_sheet(query_sets=query_sets,
                               column_names=column_names)
    sheet.name_columns_by_row(0)
    sheet.column.format('votes', int)

    # Transform the sheet into an svg chart
    svg = excel.pe.save_as(
        array=[sheet.column['choice_text'], sheet.column['votes']],
        dest_file_type='svg',
        dest_chart_type='pie',
        dest_title=question.question_text,
        dest_width=600,
        dest_height=400
    )

    return render(
        request,
        'survey_result.html',
        dict(svg=svg.read())
    )


def import_sheet_using_isave_to_database(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].isave_to_database(
                model=Question,
                mapdict=['question_text', 'pub_date', 'slug'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {'form': form})


def import_data_using_isave_book_as(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].isave_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def import_without_bulk_save(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']],
                bulk_save=False
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })