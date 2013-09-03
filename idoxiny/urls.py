from django.conf.urls import patterns, include, url
from django.contrib import admin
from bambu.bootstrap.views import DirectTemplateView
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^in/', include('idoxiny.geo.urls')),
	url(r'^$',
		DirectTemplateView.as_view(
			template_name = 'home.html',
			extra_context = {
				'menu_selection': 'home',
				'body_classes': ('home',)
			}
		),
		name = 'home'
	),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('idoxiny.skills.urls'))
)