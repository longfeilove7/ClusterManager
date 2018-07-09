#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
"""ClusterManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# django-cruds-adminlte

from django.conf.urls import url
from django.contrib import admin
from HostManager import views
from django.conf.urls import include
#import os, sys, commands

urlpatterns = [
    url(r'^$', views.login),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    
    url(r'^host_info/', views.host_info),
    url(r'^host_edit-(?P<nid>\d+)/', views.host_edit),
    url(r'^host_del-(?P<nid>\d+)/', views.host_del),
    url(r'^add_cluster/', views.add_cluster),
    url(r'^cluster_edit-(?P<nid>\d+)/', views.cluster_edit),
    url(r'^cluster_del-(?P<nid>\d+)/', views.cluster_del),
    url(r'^power_on/', views.TasksClass.powerOn),
    url(r'^power_off/', views.TasksClass.powerOff),
    url(r'^power_cycle/', views.TasksClass.powerCycle),
    url(r'^batch_power_on/', views.TasksClass.batchPowerOn),
    url(r'^batch_power_off/', views.TasksClass.batchPowerOff),
    
    #for django-excel
    url(r'^django_excel', views.upload, name='uplink'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^download_attachment/(.*)/(.*)', views.download_as_attachment,
        name="download_attachment"),
    url(r'^exchange/(.*)', views.exchange, name="exchange"),
    url(r'^parse/(.*)', views.parse, name="parse"),
    url(r'^import/', views.import_data, name="import"),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^export/(.*)', views.export_data, name="export"),
    url(r'^handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    url(r'^embedded_handson_view/',
        views.embed_handson_table, name="embed_handson_view"),
    url(r'^embedded_handson_view_single/',
        views.embed_handson_table_from_a_single_table,
        name="embed_handson_view"),
    # survey_result
    url('^survey_result/',
        views.survey_result, name='survey_result'),

    # testing purpose
    url(r'^import_using_isave/',
        views.import_data_using_isave_book_as),
    url(r'^import_sheet_using_isave/',
        views.import_sheet_using_isave_to_database),
    url(r'^import_without_bulk_save/',
        views.import_without_bulk_save, name="import_no_bulk_save")
    
]
