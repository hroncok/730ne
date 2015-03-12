from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
     if request.user.is_authenticated():
          baddomain = not request.user.email.endswith('@fit.cvut.cz')
          if baddomain:
               auth_logout(request)
     else:
          baddomain = False

     return render_to_response('index.html', {
        'user': request.user,
        'baddomain': baddomain
    }, RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))
