#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader
from blog.models import *
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render,get_object_or_404,render_to_response
from django.core.paginator import Paginator  
import datetime  
from django.core.urlresolvers import reverse
from django.db.models import Q  
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request,pageNo=None,etype=None,keyword=None):  
    try:  
        pgNo=int(pageNo)  
    except:  
        pgNo=1  
    try:  
        etype=int(etype)  
    except:  
        etype=None    
    if etype:  
        datas=Essay.objects.all().filter(eType=etype)
    elif keyword:  
          
        datas=Essay.objects.all().filter(Q(title__icontains=keyword)|Q(abstract__icontains=keyword)|Q(content__icontains=keyword)).distinct() 

    else:  
        datas=Essay.objects.all()
    recentList=datas[:5]  
    paginator = Paginator(datas, 5)  
    if pgNo==0:  
        pgNo=1  
    if pgNo>paginator.num_pages:  
        pgNo=paginator.num_pages  
    curPage=paginator.page(pgNo)
    context={
            'page':curPage,  
            'essay_type':EssayType.objects.all(),  
            'pcount':paginator.num_pages,  
            'recent':recentList,  
            'archives':Archive.objects.all()}
    context.update(csrf(request))
    return render_to_response('blog/index.html',context)
#文章详细信息
@csrf_protect
def essay_details(request,eid=None):
    #返回文章详细信息或者404页面
    essay=get_object_or_404(Essay,id=eid)
    recentList=Essay.objects.all()[:5]
    #新用户的Session
    if request.session.get('e'+str(eid),True):
        request.session['e'+str(eid)]=False
        #这里可以用一个timer实现，浏览次数保存在内存中，
        #timer定期将浏览次数提交到数据库
        #文章浏览次数+1
        essay.view_count=essay.view_count+1
        essay.save()
    context={
    'essay':essay,
    'essay_type':EssayType.objects.all(),
    'archives':Archive.objects.all(),
    'date_format':essay.pub_date.strftime('%A %B %d %Y').split(),
    'recent':recentList
    }
    context.update(csrf(request))
    return render_to_response('blog/details.html',context)
#根据关键字来搜索文章    
def search(request):
    if request.method == 'POST':
        #从POST请求中获取查询关键字
        key=request.POST.get('keyword',None)
        return index(request,keyword=key)
    else:
        return index(request)
    

#存储用户留言信息
def leave_comment(request,eid=None):
    if request.method == 'POST' and eid:
        uname=request.POST.get('uname',None)
        content=request.POST.get('comment',None)
        email=request.POST.get('email',None)
        essay=Essay.objects.get(id=eid)
        if uname and content and email and essay:
            comment=Comment()
            comment.uname=re.sub("/<(.*)>.*<\/\1>|<(.*) \/>/",'',uname)
            comment.content=re.sub("/<(.*)>.*<\/\1>|<(.*) \/>/",'',content)
            comment.email=re.sub("/<(.*)>.*<\/\1>|<(.*) \/>/",'',email)
            comment.essay=essay
            comment.pub_date=datetime.datetime.now()
            comment.save()
            return essay_details(request,eid)
        return index(request)
    
    return index(request)

