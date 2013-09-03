from idoxiny.geo.models import Postcode

def postcodes(request):
	return {
		'postcodes': Postcode.objects.filter(profiles__isnull = False).distinct()
	}