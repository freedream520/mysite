from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.utils import timezone
urlpatterns = patterns('',
    url(r'^index','emailsys.views.index',name='index'),
    url(r'^write','emailsys.views.write',name='write'),
    url(r'^inbox','emailsys.views.recvmail',name='recvmail'),
    url(r'^sendmail/$','emailsys.views.send_email',name='send_email'),
    url(r'^mainemail/$','emailsys.views.login',name='login'),
    url(r'^details','emailsys.views.reademail',name='reademail'),
    url(r'^(?P<pageNo>\d+)/(?P<etype>\d+)/$','emailsys.views.reademail'),
)