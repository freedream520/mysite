# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader
from emailsys.models import *
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render,get_object_or_404,render_to_response
from django.core.mail import send_mail,BadHeaderError
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.core.paginator import Paginator 
import datetime 
import sys
import os
import imaplib   
import email   
import string
import base64
import re  
epath=os.getcwd().replace('\\', '/')
unseen=0
@csrf_protect
def index(request):
    context = Context({
    })
    context.update(csrf(request))
    return render_to_response('emailsys/login.html',context)
def write(request):
    context = Context({
    })
    context.update(csrf(request))
    return render_to_response('emailsys/index.html',context)
@csrf_protect
def login(request):
    context = Context({
    })
    context.update(csrf(request))
    if request.method== 'POST':
        user=request.POST.get('euser','')
        host=request.POST.get('host','')
        password=request.POST.get('epassword','')
        if user and host and password:
            address=Emailaddress()
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
                address.login_ip =  request.META['HTTP_X_FORWARDED_FOR'].split(",")[0]
            else:  
                address.login_ip = request.META['REMOTE_ADDR'].split(",")[0]
            address.host=host
            address.user=user
            address.pwd=password
            address.pub_date=datetime.datetime.now()
            address.emailtype=''
            address.save()
            return render_to_response('emailsys/main.html',context)
        else:
            return HttpResponse('errors.')
@csrf_protect
def send_email(request):
    if request.method == 'POST':
        subject=request.POST.get('subject','')
        message=request.POST.get('comment','')
        to_email = request.POST.get('toemail','')
        if subject and message  and to_email:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
                ip =  request.META['HTTP_X_FORWARDED_FOR'].split(",")[0]
            else:  
                ip = request.META['REMOTE_ADDR'].split(",")[0] 
            mailmsg=Emailaddress.objects.filter(login_ip=ip).order_by('-pub_date')[0]
            mailmsg.emailtype='sent'
            host=mailmsg.host
            user=mailmsg.user
            EMAIL_HOST = 'smtp'+'.'+host
            EMAIL_HOST_USER = user+'@'+host
            EMAIL_HOST_PASSWORD=mailmsg.pwd
            mailmsg.save()
            try:
                import smtplib
                from email.mime.text import MIMEText
                mail_to=to_email
                    #设置服务器，用户名、口令以及邮箱的后缀
                mail_host=EMAIL_HOST
                mail_user=user
                mail_pass=EMAIL_HOST_PASSWORD
                mail_postfix=host
                me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
                msg = MIMEText(message,'html',_charset='UTF-8')
                msg['Subject'] = subject
                msg['From'] = me
                msg['To'] = mail_to
                s = smtplib.SMTP()
                s.connect(mail_host)
                s.login(mail_user,mail_pass)
                s.sendmail(me, mail_to, msg.as_string())
                s.close()
            except Exception, e:
                return HttpResponse('ERRORS:'+str(e))
            return HttpResponse('success.')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Invalid header found.')
    else:
        return HttpResponse('Invalid header found.')
@csrf_protect
def recvmail(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR'].split(",")[0]
    else:  
        ip = request.META['REMOTE_ADDR'].split(",")[0] 
    mailmsg=Emailaddress.objects.filter(login_ip=ip).order_by('-pub_date')[0]
    host=mailmsg.host
    user=mailmsg.user
    EMAIL_HOST = 'imap'+'.'+host
    EMAIL_HOST_USER = user+'@'+host
    EMAIL_HOST_PASSWORD=mailmsg.pwd 
    
    conn = imaplib.IMAP4(EMAIL_HOST)  
    conn.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    conn.select()
    typ, data = conn.search(None, 'UNSEEN')
    global unseen
    unseen=0
    for inum in data[0].split():
        unseen=unseen+1

    def htmlparser(html):
        html=re.sub("<[\\s]*?script[^>]*?>[\\s\\S]*?<[\\s]*?\\/[\\s]*",'',html)
        html=re.sub("<[\\s]*?style[^>]*?>[\\s\\S]*?<[\\s]*?\\/[\\s]*?s",'',html)
        html=re.sub("<[^>]+>",'',html)
        html=re.sub('script>','',html)
        html=re.sub('tyle>','',html)
        html=re.sub('/s','',html)
        html=re.sub('a>[^\>]+>','',html)
        html=re.sub('startdate>[^\>]+>','',html)
        return html
    def extract_body(payload):   
        if isinstance(payload,str):   
          return payload   
        else:   
          return '\n'.join([extract_body(part.get_payload()) for part in payload])
    try:
        for num in data[0].split():
            econtent=Emailcontent()
            typ, msg_data = conn.fetch(num, '(RFC822)')   
            for response_part in msg_data:   
             if isinstance(response_part, tuple):   
                msg = email.message_from_string(response_part[1])   
                subject=msg['subject']
                efrom=msg['From']
                date=msg['Date']
                try:
                    b=email.Header.decode_header(subject)[0][0].decode('utf-8')
                    
                except:
                    b = email.Header.decode_header(subject)[0][0]
                    b=b.decode('gbk')
                subcode=email.Header.decode_header(subject)[0][1]
                
                econtent.subject=b
                try:
                    d=email.Header.decode_header(efrom)[1][0]
                    econtent.emailfrom=d
                    
                except:
                    g=email.Header.decode_header(efrom)[0][0]
                    econtent.emailfrom=g
                try:
                    c=email.Header.decode_header(date)[0][0].decode('utf-8')
                except:
                    c= email.Header.decode_header(date)[0][0]
                econtent.emaildate=c
                payload=msg.get_payload() 
                body=extract_body(payload)
                if subcode=='utf-8':
                    a=body.decode('utf-8')
                    a=htmlparser(a)
                else:
                    a=base64.decodestring(body)
                    a=htmlparser(a).strip(" ").strip("\n")
                    a=a.decode('gbk')
                econtent.content=a
                econtent.address=mailmsg
                econtent.save()
    except Exception, e:
                return HttpResponse('ERRORS:'+str(e))
        
   # p=Emailaddress.objects.filter(emailtype='recv',user=mailmsg.user,host=mailmsg.host)   
    context = Context({
    'unseen_count':unseen,
   # 'seen_count':Emailcontent.objects.filter(address=p).count()
    })
    context.update(csrf(request))
  #  for su,co in sub ,cont:
   #     content=emailcontent()
   #     content.email_address=emailaddress.objects.filter(login_ip=ip).order_by('-pub_date')[0]
   #     content.email_address.emailtype='recv'
   #     content.subject=su
   #     content.content=co
   #     content.save()
    return render_to_response('emailsys/inbox.html',context)
def reademail(request,pageNo=None):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR'].split(",")[0]
    else:  
        ip = request.META['REMOTE_ADDR'].split(",")[0] 
    mailmsg=Emailaddress.objects.filter(login_ip=ip).order_by('-pub_date')[0]
    host=mailmsg.host
    user=mailmsg.user
    EMAIL_HOST = 'imap'+'.'+host
    EMAIL_HOST_USER = user+'@'+host
    EMAIL_HOST_PASSWORD=mailmsg.pwd
    mailmsg.emailtype='recv'
    mailmsg.save()
    conn = imaplib.IMAP4(EMAIL_HOST)  
    conn.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    conn.select()
    typ, data = conn.search(None, 'UNSEEN')
    for num in data[0].split():
         typ, response = conn.store(num, '+FLAGS', r'(\Seen)')  
    try:   
        conn.close()   
    except:   
        pass  
    conn.logout()    
    try:  
        pgNo=int(pageNo)  
    except:  
        pgNo=1
    readmsg=Emailaddress.objects.filter(login_ip=ip).order_by('-pub_date')[0]
    datas=Emailcontent.objects.filter(address=readmsg).order_by('-id')[:unseen]
    paginator = Paginator(datas, 5)  
    if pgNo==0:  
        pgNo=1  
    if pgNo>paginator.num_pages:  
        pgNo=paginator.num_pages  
    curPage=paginator.page(pgNo)
    context = Context({
    'page':curPage,
    'pcount':paginator.num_pages, 
    })
    context.update(csrf(request))
    return render_to_response('emailsys/details.html',context)
