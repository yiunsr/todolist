"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers

from todolist import view
from accounts.views import UserViewSet
from todos.views import TodoViewSet, AdminTodoViewSet

router = routers.DefaultRouter()
router.register(r'account', UserViewSet)
router.register(r'admintodo', AdminTodoViewSet)
router.register(r'todo', TodoViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^rest/', include(router.urls)),
    path('account/', include('accounts.urls')),
    path('todo/', include('todos.urls')),
    path('sample', view.sample),
    path('', view.main),
]
