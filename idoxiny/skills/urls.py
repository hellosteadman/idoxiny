from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('idoxiny.skills.views',
	url(r'^skills/$', 'skills', name = 'skills'),
	url(r'^skills/(?P<slug>[\w-]+)/$', 'skill', name = 'skill'),
	url(r'^do/$', 'signup', {'direction': 'do'}, name = 'doer_signup'),
	url(r'^do/callback/$', 'callback', {'direction': 'do'}, name = 'do_callback'),
	url(r'^seek/$', 'signup', {'direction': 'seek'}, name = 'seeker_signup'),
	url(r'^seek/callback/$', 'callback', {'direction': 'seek'}, name = 'seek_signup'),
	url(r'^(?P<username>\w+)/$', 'profile', name = 'profile'),
	url(r'^(?P<username>\w+)/$', 'profile', name = 'profile')
)

urlpatterns += patterns('',
	url(r'^do/(?P<slug>\w+)/$', RedirectView.as_view(url = '/%(slug)s/')),
	url(r'^seek/(?P<slug>\w+)/$', RedirectView.as_view(url = '/%(slug)s/')),
)