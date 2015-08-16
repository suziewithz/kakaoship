# coding:utf-8

from django.conf.urls import patterns, url

from kakaoship import views

urlpatterns = patterns('',
    url(r'^$', 'views.drawChart', name='drawChart'),
    url(r'^([\w]+)/$', 'views.drawChart', name='drawChart'),
)
