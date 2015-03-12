from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from signatures import models


def home(request):
    if request.user.is_authenticated():
        baddomain = not request.user.email.endswith('@fit.cvut.cz')
        if baddomain:
            auth_logout(request)
    else:
        baddomain = False

    signed_list = models.Signature.objects.filter(signed=True).order_by('timestamp')
    paginator = Paginator(signed_list, 20)
    total = signed_list.count()

    page = request.GET.get('page')
    try:
        signatures = paginator.page(page)
    except PageNotAnInteger:
        signatures = paginator.page(1)
    except EmptyPage:
        signatures = paginator.page(paginator.num_pages)

    return render_to_response('index.html', {
        'user': request.user,
        'baddomain': baddomain,
        'signatures': signatures,
        'total': total,
    }, RequestContext(request))


@login_required
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def toggle(request):
    """Mark the user as signed"""
    sig, created = models.Signature.objects.get_or_create(user=request.user)
    sig.signed = not sig.signed
    sig.save()
    return HttpResponseRedirect(reverse('home'))
