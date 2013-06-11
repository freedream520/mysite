from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render,get_object_or_404,render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
def webseeindex(request):
    return render_to_response('websee/index.html')
def play(request):
  		return render_to_response('websee/play.html')