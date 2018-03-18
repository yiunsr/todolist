#-*- coding: utf-8 -*-
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^adminlist/?$',  views.adminlist),
    url(r'^dayofweeklist/?$',  views.dayofweeklist),
    url(r'^list/?$',  views.commonlist),
    url(r'^export/?$',  views.exportData),
    url(r'^import/?$',  views.importData),
]