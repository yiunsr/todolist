#-*- coding: utf-8 -*-
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^list/?$',  views._list),
    url(r'^export/?$',  views.exportData),
    url(r'^import/?$',  views.importData),
]