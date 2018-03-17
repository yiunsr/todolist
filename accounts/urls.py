#-*- coding: utf-8 -*-
from django.conf.urls import  url
from . import views 

urlpatterns = [
    url(r'^login/?$',  views._login),
    url(r'^signup/?$',  views.signup),
    url(r'^list/?$',  views._list),
]