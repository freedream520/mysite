from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from blog.models import *
from django.utils import timezone


urlpatterns = patterns('',
    url(r'^index','blog.views.index',name='index'),

)
