from django.conf.urls.defaults import *
import views

################################################################################
urlpatterns = patterns('mysite.views',
    url(r'^$', views.home, name="home"),
    url(r'^client$', views.client, name="client"),
    url(r'^api/submit_award$', views.submit_award, name="submit_award"),
)
