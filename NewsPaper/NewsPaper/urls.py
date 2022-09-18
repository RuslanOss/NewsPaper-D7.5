"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


import logging


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]

logger_dr = logging.getLogger('django.request')
logger_cn = logging.getLogger('django')

logger_dr.error("Hello! I'm an error in your app. Enjoy:)")
logger_cn.error("Hello! I'm another error in your app. Enjoy:)")
