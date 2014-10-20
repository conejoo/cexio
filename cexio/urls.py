from django.conf.urls import patterns, include, url

from django.contrib import admin
from front import views as front
from api import views as api
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cexio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/(?P<collection>\w{0,50})/$', api.get),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', front.index, name='index'),
)
