# -*- coding: utf-8 -*-
from django.db import models
class Emailaddress(models.Model):
    login_ip=models.CharField(max_length=20)
    user = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    pwd = models.CharField(max_length=200)
    emailtype = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.user
class Emailcontent(models.Model):
    subject=models.CharField(max_length=200)
    emailfrom=models.CharField(max_length=200)
    emaildate=models.CharField(max_length=200)
    content=models.TextField(max_length=2000)
    address=models.ForeignKey(Emailaddress,  
    related_name='email_address')
    def __unicode__(self):
        return self.subject
