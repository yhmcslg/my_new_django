"""offer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^validate/$','app001.views.validate',name='validate'),
    url(r'^test/$','app001.views.test'),
    url(r'^search/$','app001.views.search'),
    url(r'^index/(\w+)?$','app001.views.index'),
    url(r'^log/(\w+)$','app001.views.log'),
    url(r'^login/$','app001.views.login'),
    url(r'^logout/$','app001.views.logout'),
    url(r'^web_console/(\w+)?$','app001.views.web_console'),
    url(r'^upload/$','app001.views.upload'),
    url(r'^login_view/$','app001.views.login_view'),
    url(r'^sendmail/$','app001.views.sendmail'),
]
