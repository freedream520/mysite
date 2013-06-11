from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.utils import timezone
urlpatterns = patterns('',
    url(r'^index','websee.views.webseeindex',name='index'),
    url(r'^play','websee.views.play',name='play'),

)
