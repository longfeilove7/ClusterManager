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
"""
命名规范：module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.
"""
# django-cruds-adminlte

from django.conf.urls import url
from django.contrib import admin
from HostManager import views
from django.conf.urls import include
#import os, sys, commands

urlpatterns = [
    url(r'^$', views.ClassSign.signin),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include(
        'jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    #  url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^sign-up/', views.ClassSign.signup),
    url(r'^sign-in/', views.ClassSign.signin),
    url(r'^index/', views.ClassSign.index),

    # for device url
    url(r'^host_info/', views.ClassHost.host_info),
    url(r'^host_edit-(?P<nid>\d+)/', views.ClassHost.host_edit),
    url(r'^host_del-(?P<nid>\d+)/', views.ClassHost.host_del),
    url(r'^add_host/', views.ClassHost.add_host),
    url(r'^add_cluster/', views.ClassCluster.add_cluster),
    url(r'^cluster_edit-(?P<nid>\d+)/', views.ClassCluster.cluster_edit),
    url(r'^cluster_del-(?P<nid>\d+)/', views.ClassCluster.cluster_del),
    url(r'^power_history-(?P<nid>\d+)/', views.ClassHost.power_history),

    # for device function
    url(r'^power_on/', views.ClassCeleryWorker.powerOn),
    url(r'^power_off/', views.ClassCeleryWorker.powerOff),
    url(r'^power_cycle/', views.ClassCeleryWorker.powerCycle),
    url(r'^batch_power_on/', views.ClassCeleryWorker.batchPowerOn),
    url(r'^batch_power_off/', views.ClassCeleryWorker.batchPowerOff),
    url(r'^batch_power_cycle/', views.ClassCeleryWorker.batchPowerCycle),

    # for task url
    url(r'^inspect_info/', views.ClassCeleryWorker.inspect_info),
    url(r'^task_result/',
        views.ClassCeleryResult.task_result,
        name='task_result'),
    url(r'^task_result_json/',
        views.ClassCeleryResult.task_result_json,
        name='task_result_json'),
    url(r'^solar_schedule/', views.ClassCeleryBeat.solar_schedule),
    url(r'^periodic_task/', views.ClassCeleryBeat.periodic_task),
    url(r'^add_periodic/', views.ClassCeleryBeat.add_periodic),
    url(r'^interval_schedule/', views.ClassCeleryBeat.interval_schedule),
    url(r'^crontab_schedule/', views.ClassCeleryBeat.crontab_schedule),
    url(r'^crontab_del-(?P<nid>\d+)/', views.ClassCeleryBeat.crontab_del),
    url(r'^crontab_edit-(?P<nid>\d+)/', views.ClassCeleryBeat.crontab_edit),

    # for task function
    url(r'^batch_inspect_sdr/', views.ClassCeleryWorker.batchInspectSdr),
    url(r'^inspect_sdr/', views.ClassCeleryWorker.inspectSdr),

    # for device billing
    url(r'^billing_info/', views.ClassBillingSystem.billingInfo),
    url(r'^billing_device/', views.ClassBillingSystem.billingDevice),
    url(r'^billing_price/', views.ClassBillingSystem.billingPrice),
    url(r'^billing_switch/', views.ClassBillingSystem.billingSwitch),
    url(r'^batch_billing_add/', views.ClassBillingSystem.batchBillingAdd),
    url(r'^batch_billing_delete/', views.ClassBillingSystem.batchBillingDelete),

    #for device monitor
    url(r'^monitor_info/', views.ClassMonitorSystem.monitorInfo),
    url(r'^monitor_device/', views.ClassMonitorSystem.monitorDevice),
    url(r'^monitor_price/', views.ClassMonitorSystem.monitorPrice),
    url(r'^monitor_switch/', views.ClassMonitorSystem.monitorSwitch),
    url(r'^batch_monitor_add/', views.ClassMonitorSystem.batchMonitorAdd),
    url(r'^batch_monitor_pause/', views.ClassMonitorSystem.batchMonitorPause),  
    url(r'^batch_monitor_delete/', views.ClassMonitorSystem.batchMonitorDelete),     

    #for django-excel
    url(r'^django_excel', views.upload, name='uplink'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^download_attachment/(.*)/(.*)',
        views.download_as_attachment,
        name="download_attachment"),
    url(r'^exchange/(.*)', views.exchange, name="exchange"),
    url(r'^parse/(.*)', views.parse, name="parse"),
    url(r'^import/', views.import_data, name="import"),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^export/(.*)', views.export_data, name="export"),
    url(r'^handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    url(r'^embedded_handson_view/',
        views.embed_handson_table,
        name="embed_handson_view"),
    url(r'^embedded_handson_view_single/',
        views.embed_handson_table_from_a_single_table,
        name="embed_handson_view"),
    # survey_result
    url('^survey_result/', views.survey_result, name='survey_result'),

    # testing purpose
    url(r'^import_using_isave/', views.import_data_using_isave_book_as),
    url(r'^import_sheet_using_isave/',
        views.import_sheet_using_isave_to_database),
    url(r'^import_without_bulk_save/',
        views.import_without_bulk_save,
        name="import_no_bulk_save")
]
