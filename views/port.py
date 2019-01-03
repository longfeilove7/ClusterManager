"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
from rest_framework_swagger.views import get_swagger_view
from django.db.models import Count, Max, Avg, Min, Sum, F, Q, FloatField
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpRequest, HttpResponseBadRequest,FileResponse,JsonResponse
from HostManager import models
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import PeriodicTasks
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import SolarSchedule
from django_celery_results.models import TaskResult
import django_excel
from celery import shared_task
from celery import task
from HostManager import tasks
from celery import Celery
from celery.schedules import crontab
from celery import app
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import xlwt,xlrd
from io import StringIO,BytesIO
import json,os
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
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from decimal import *
#import os, sys, commands
import xmlrpc.server
import xmlrpc.client
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadhandler import FileUploadHandler
# Create your views here.

data = [[1, 2, 3], [4, 5, 6]]



class UploadFileForm(forms.Form):
    file = forms.FileField()
class FileUploadForm(forms.Form):
    my_file = forms.FileField(label='文件名称:')

@login_required
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


def download(request):
    file=open('templates/sample-data.xls','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="sample-data.xls"'
    return response


def download_as_attachment(request, file_type, file_name):
    return excel.make_response_from_array(data, file_type, file_name=file_name)


def export_data(request,type):
    if request.method == "GET":

        return render(request,"export.html")


def dump_data(request):

        data = models.Host.objects.all().order_by('id')
        if data:
            #创建表
            ws = xlwt.Workbook(encoding='utf-8')
            #创建sheet
            sheet = ws.add_sheet('host',cell_overwrite_ok=True)
            #表头设置
            style_head = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour 0x19;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)
            sheet.write(0,0,"ID",style_head)
            sheet.write(0,1,"主机名",style_head)
            sheet.write(0,2,"IP",style_head)
            sheet.write(0,3,"机房",style_head)
            sheet.write(0,4,"电源状态",style_head)
            sheet.write(0,5,"计费状态",style_head)
            excel_row = 1
            for dat in data:
                id = dat.id
                hostname = dat.hostName
                serviceip = dat.serviceIP
                roomname = dat.roomName.roomName
                powerstatus = dat.powerStatus
                billingstatus = dat.billingStatus
                sheet.write(excel_row,0,id)
                sheet.write(excel_row, 1, hostname)
                sheet.write(excel_row, 2, serviceip)
                sheet.write(excel_row, 3, roomname)
                sheet.write(excel_row, 4, powerstatus)
                sheet.write(excel_row, 5, billingstatus)
                excel_row += 1
            exit_file = os.path.exists("hostname.xls")
            if exit_file:
                os.remove(r'hostname.xls')
            # ws.save()
            # sio = StringIO.StringIO()
            # ws.save(sio)
            # sio.seek(0)
            output = BytesIO()
            ws.save(output)
            output.seek(0)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=hostname.xls'
            response.write(output.getvalue())
            return response





def import_data(request):

    if request.method == "POST":
        myform = FileUploadForm(request.POST, request.FILES)


        print(myform)
        # type_excle = f.name.split('.')[1]
        if myform.is_valid():
            f = request.FILES['my_file']
            print(f)
            wb = wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            print(table)
            nrows = table.nrows

            for i in range(1, nrows):
                rowValues = table.row_values(i)  # 一行的数据
                models.Host.objects.create(hostName=rowValues[0],serviceIP=rowValues[1],manageIP=rowValues[2],storageIP=rowValues[3],roomName_id=rowValues[4],cabinetNO=rowValues[5],bladeBoxNO=rowValues[6],bladeNO=rowValues[7])
                        # good = models.GoodsManage.objects.get(international_code=rowValues[0])
                        # models.SupplierGoodsManage.objects.create(goods=good, sale_price=rowValues[1],
                        #                                           sale_min_count=rowValues[2])


        return JsonResponse({'msg': 'ok'})


    else:
        form = FileUploadForm()
    return render(
        request, 'upload_form.html', {
            'form': form,
            'title': 'Import excel data into database example',
            'what': '数据导入：'
        })


@login_required
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


@login_required
def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()


@login_required
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


@login_required
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


@login_required
def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Question, dest_file_type='handsontable.html', dest_embed=True)
    content.seek(0)
    return render(request, 'custom-handson-table.html',
                  {'handsontable_content': content.read()})


@login_required
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


@login_required
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


@login_required
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


@login_required
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
