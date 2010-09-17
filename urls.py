from django.conf.urls.defaults import *
from settings import MEDIA_ROOT
from django.views.static import serve

import mysite

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^', include('money.mysite.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('awards.mysite.urls')),
    #(r'^login/$', 'django.contrib.auth.views.login'),#, {'template_name': 'login.html'}),
    #(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	(r'^static/(?P<path>.*)$', serve,
     {'document_root': MEDIA_ROOT,
      'show_indexes': True}),
)
