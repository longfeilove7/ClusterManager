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
from django.conf.urls import url
from django.contrib import admin
from HostManager import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^host_info/', views.host_info),
    url(r'^host_edit-(?P<nid>\d+)/', views.host_edit),
    url(r'^host_del-(?P<nid>\d+)/', views.host_del),
    url(r'^add_group/', views.add_group),
    url(r'^group_edit-(?P<nid>\d+)/', views.group_edit),
    url(r'^group_del-(?P<nid>\d+)/', views.group_del),
]
