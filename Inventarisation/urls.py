"""Inventarisation URL Configuration

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
from django.template.defaulttags import url
from django.urls import path, include, re_path

from task_logger.views import process_message, get_token, process_host_info_json

admin.site.site_header = 'Inventory Portal'
urlpatterns = [
    path('baton/', include('baton.urls')),
    path('special', process_message),
    path('token', get_token),
    path('host_info_update', process_host_info_json),
    path('', admin.site.urls),
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
]
