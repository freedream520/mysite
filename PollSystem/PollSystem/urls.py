from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^$', home),
	url(r'^(?P<pageNo>\d+)/$','blog.views.index',name='index'),
	url(r'^essay/(?P<eid>\d+)/$','blog.views.essay_details',name='essay_details'),
	url(r'^search/$','blog.views.search',name='search'),
	url(r'^sendmail/$','emailsys.views.send_mail',name='send_mail'),
	url(r'^leavemsg/(?P<eid>\d+)/$','blog.views.leave_comment',name='leave_comment'),
	url(r'^(?P<pageNo>\d+)/(?P<etype>\d+)/$','blog.views.index'),
	url(r'^appliction/',appliction),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/',include('tinymce.urls')),
)
urlpatterns += patterns('blog.views',
    url(r'^blog/',include('blog.urls',namespace="blog")),
)
urlpatterns += patterns('polls.views',
    url(r'^polls/',include('polls.urls',namespace="polls")),
)
urlpatterns += patterns('websee.views',
    url(r'^websee/',include('websee.urls',namespace="websee")),
)
urlpatterns += patterns('emailsys.views',
    url(r'^emailsys/',include('emailsys.urls',namespace="emailsys")),
)