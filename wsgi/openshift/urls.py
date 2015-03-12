from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^$', 'views.home', name='home'),
                       url(r'^logout/$', 'views.logout', name='logout'),
                       url(r'^toggle/$', 'views.toggle', name='toggle'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
