from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('idoxiny.geo.views',
	url(r'^(?P<slug>[\w]+)/$', 'area', name = 'area'),
)