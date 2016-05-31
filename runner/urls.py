# -*- coding: utf-8 -*-

# Copyright (C) 2014 Nerim (Philippe 'paHpa' Vivien)

from django.conf.urls import (  # noqa
    patterns, include, url,
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from runner.views import home, PortfolioView

from django.contrib import admin
admin.autodiscover()

    

urlpatterns = patterns('',
    url(r'^$',  home.as_view(), name='home'),


    url(r'^portfolio/(?P<pk>\d+)/$', PortfolioView.as_view()),
    # url(r'^blog/', include('blog.urls')),
#    url(r"^account/", include("account.urls")),

    #pinax account
    url(r"^accounts/", include("account.urls")),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^example/', 'example.views.index'),   

    url(r'^blacklist/', include('blacklist.urls' , namespace='blacklist', app_name='blacklist')),
  
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^tuto/', include('tuto.urls')),

)

# PAHPA : LOAD URL 
#print "** PAHPA ** loadind url"
from django.conf import settings

#TEST DJANGO-REST
if 'rest_framework' in settings.INSTALLED_APPS:

    from rest_framework.authtoken import views
    from account.views import SettingsView
    
    urlpatterns += patterns('',
        url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
#        url(r'^api-token-auth/', views.obtain_auth_token), 

        #si utilisation djoser account (en test)
        #url(r'^auth/', include('djoser.urls')),

        #mapping pinax 'account'
        url(r"^accounts/profile/$", SettingsView.as_view(), name="account_settings"),
    )



