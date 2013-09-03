from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from idoxiny.geo.models import Area
from idoxiny.skills.models import Profile

def area(request, slug):
	a = get_object_or_404(Area, slug = slug)
	
	return TemplateResponse(
		request,
		'geo/area.html',
		{
			'area': a,
			'area_doers': Profile.objects.filter(postcode__area = a, has_skills__isnull = False).distinct(),
			'area_seekers': Profile.objects.filter(postcode__area = a, required_skills__isnull = False).distinct(),
			'title_parts': (unicode(a),)
		}
	)