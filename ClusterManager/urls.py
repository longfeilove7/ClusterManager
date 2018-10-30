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
#from HostManager import views
from views import cobbler
from views import views
from views import celery
from views import billing
from views import monitor
from views import install
from views import calculate
from views import portal
from views import host
from views import cluster
from views import port
from views import sign
from django.conf.urls import include
#import os, sys, commands

urlpatterns = [
    url(r'^$', sign.ClassSign.signin),
    url(r'^swagger/', views.schema_view),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include(
        'jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    #  url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^sign-up/', sign.ClassSign.signup),
    url(r'^sign-in/', sign.ClassSign.signin),

    #for portal
    url(r'^index/', portal.ClassPortal.index),
    url(r'^dashboard1/', portal.ClassPortal.dashboard1),
    url(r'^dashboard2/', portal.ClassPortal.dashboard2),

    # for device url
    url(r'^host_info/', host.ClassHost.host_info),
       url(r'^host_power/', host.ClassHost.hostPower),
          url(r'^host_boot/', host.ClassHost.hostBoot),
                 url(r'^host_remote/', host.ClassHost.hostRemote),
    url(r'^host_info_query/',
        host.ClassHost.hostInfoQuery,
        name='host_info_query'),
    url(r'^host_edit-(?P<nid>\d+)/', host.ClassHost.host_edit),
    url(r'^add_host/', host.ClassHost.add_host),
    url(r'^host_delete/', host.ClassHost.HostDelete),
    url(r'^batch_host_delete/', host.ClassHost.batchHostDelete),
    url(r'^power_history-(?P<nid>\d+)/', host.ClassHost.power_history),

    # for cluster
    url(r'^add_cluster/', cluster.ClassCluster.add_cluster,
        name='add_cluster'),
    url(r'^cluster_info_query/',
        cluster.ClassCluster.clusterInfoQuery,
        name='cluster_info_query'),
    url(r'^cluster_edit-(?P<nid>\d+)/', cluster.ClassCluster.cluster_edit),
    url(r'^batch_cluster_delete/', cluster.ClassCluster.batchClusterDelete),
    url(r'^cluster_delete/', cluster.ClassCluster.ClusterDelete),

    # for device function
    url(r'^power_on/', celery.ClassCeleryWorker.powerOn),
    url(r'^power_off/', celery.ClassCeleryWorker.powerOff),
    url(r'^power_cycle/', celery.ClassCeleryWorker.powerCycle),
    url(r'^batch_power_on/', celery.ClassCeleryWorker.batchPowerOn),
    url(r'^batch_power_off/', celery.ClassCeleryWorker.batchPowerOff),
    url(r'^batch_power_cycle/', celery.ClassCeleryWorker.batchPowerCycle),

    # for task url
    url(r'^inspect_info/', celery.ClassCeleryWorker.inspect_info),
    url(r'^task_result/',
        celery.ClassCeleryResult.task_result,
        name='task_result'),
    url(r'^task_result_query/',
        celery.ClassCeleryResult.task_result_query,
        name='task_result_query'),
    url(r'^solar_schedule/', celery.ClassCeleryBeat.solar_schedule),
    url(r'^periodic_task/', celery.ClassCeleryBeat.periodic_task),
    url(r'^add_periodic/', celery.ClassCeleryBeat.add_periodic),
    url(r'^interval_schedule/', celery.ClassCeleryBeat.interval_schedule),
    url(r'^crontab_schedule/', celery.ClassCeleryBeat.crontab_schedule),
    url(r'^crontab_del-(?P<nid>\d+)/', celery.ClassCeleryBeat.crontab_del),
    url(r'^crontab_edit-(?P<nid>\d+)/', celery.ClassCeleryBeat.crontab_edit),

    # for task function
    url(r'^batch_inspect_sdr/', celery.ClassCeleryWorker.batchInspectSdr),
    url(r'^inspect_sdr/', celery.ClassCeleryWorker.inspectSdr),

    # for device billing
    url(r'^billing_info/', billing.ClassBillingSystem.billingInfo),
    url(r'^billing_info_query/',
        billing.ClassBillingSystem.billingInfoQuery,
        name='billing_info_query'),
    url(r'^billing_device/', billing.ClassBillingSystem.billingDevice),
    url(r'^billing_price/', billing.ClassBillingSystem.billingPrice),
    url(r'^billing_switch/', billing.ClassBillingSystem.billingSwitch),
    url(r'^billing_switch_query/',
        billing.ClassBillingSystem.billingSwitchQuery,
        name='billing_switch_query'),
    url(r'^batch_billing_add/', billing.ClassBillingSystem.batchBillingAdd),
    url(r'^batch_billing_delete/',
        billing.ClassBillingSystem.batchBillingDelete),
    url(r'^billing_time_query/', billing.ClassBillingSystem.billingInfoQuery),

    #for device monitor
    url(r'^monitor_info/', monitor.ClassMonitorSystem.monitorInfo),
    url(r'^monitor_info_query/',
        monitor.ClassMonitorSystem.monitorInfoQuery,
        name='monitor_info_query'),
    url(r'^monitor_device/', monitor.ClassMonitorSystem.monitorDevice),
    url(r'^monitor_price/', monitor.ClassMonitorSystem.monitorPrice),
    url(r'^monitor_switch/', monitor.ClassMonitorSystem.monitorSwitch),
    url(r'^monitor_switch_query/',
        monitor.ClassMonitorSystem.monitorSwitchQuery,
        name='monitor_switch_query'),
    url(r'^batch_monitor_add/', monitor.ClassMonitorSystem.batchMonitorAdd),
    url(r'^batch_monitor_pause/',
        monitor.ClassMonitorSystem.batchMonitorPause),
    url(r'^batch_monitor_delete/',
        monitor.ClassMonitorSystem.batchMonitorDelete),
    url(r'^monitor_time_query/', monitor.ClassMonitorSystem.monitorInfoQuery),

    # for device install os
    url(r'^install_info/', install.ClassInstallSystem.installInfo),
    url(r'^install_info_query/',
        install.ClassInstallSystem.installInfoQuery,
        name='install_info_query'),
    url(r'^installing_switch/', install.ClassInstallSystem.installingSwitch),
    url(r'^install_device/', install.ClassInstallSystem.installDevice),
    url(r'^install_switch/', install.ClassInstallSystem.installSwitch),
    url(r'^install_switch_query/',
        install.ClassInstallSystem.installSwitchQuery,
        name='install_switch_query'),
    url(r'^batch_install_add/', install.ClassInstallSystem.batchInstallAdd),
    url(r'^batch_install_pause/',
        install.ClassInstallSystem.batchInstallDelete),
    url(r'^batch_install_delete/',
        install.ClassInstallSystem.batchInstallDelete),
    # url(r'^install_time_query/', views.ClassInstallSystem.installInfoQuery),

    #for django-excel
    url(r'^django_excel', port.upload, name='uplink'),
    url(r'^download/(.*)', port.download, name="download"),
    url(r'^download_attachment/(.*)/(.*)',
        port.download_as_attachment,
        name="download_attachment"),
    url(r'^exchange/(.*)', port.exchange, name="exchange"),
    url(r'^parse/(.*)', port.parse, name="parse"),
    url(r'^import/', port.import_data, name="import"),
    url(r'^import_sheet/', port.import_sheet, name="import_sheet"),
    url(r'^export/(.*)', port.export_data, name="export"),
    url(r'^handson_view/', port.handson_table, name="handson_view"),

    # handson table view
    url(r'^embedded_handson_view/',
        port.embed_handson_table,
        name="embed_handson_view"),
    url(r'^embedded_handson_view_single/',
        port.embed_handson_table_from_a_single_table,
        name="embed_handson_view"),
    # survey_result
    url('^survey_result/', port.survey_result, name='survey_result'),

    # testing purpose
    url(r'^import_using_isave/', port.import_data_using_isave_book_as),
    url(r'^import_sheet_using_isave/',
        port.import_sheet_using_isave_to_database),
    url(r'^import_without_bulk_save/',
        port.import_without_bulk_save,
        name="import_no_bulk_save")
]
