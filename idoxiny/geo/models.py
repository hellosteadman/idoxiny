from django.db import models
from django.utils import simplejson
from django.template.defaultfilters import slugify
from urllib import urlencode, urlopen
import re
	
class Postcode(models.Model):
	postcode = models.CharField(max_length = 10, unique = True)
	area = models.ForeignKey('Area', related_name = 'postcodes')
	latitude = models.CharField(max_length = 36)
	longitude = models.CharField(max_length = 36)
	
	def __unicode__(self):
		return self.postcode
	
	def save(self, *args, **kwargs):
		if not self.latitude and not self.longitude:
			params = {
				'address': '%s, UK' % self.postcode,
				'sensor': 'false'
			}
			
			url = 'http://maps.googleapis.com/maps/api/geocode/json?%s' % urlencode(params)
			request = urlopen(url)
			response = simplejson.loads(request.read())
			results = response.get('results', [])
			
			if any(results):
				coords = results[0]['geometry']['location']
				
				if len(coords) >= 2:
					self.latitude, self.longitude = coords['lat'], coords['lng']
		
		if (self.latitude and self.longitude) and not self.pk:
			url = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat=%s&lng=%s&username=meegloo' % (
				self.latitude, self.longitude
			)
			
			request = urlopen(url)
			
			try:
				json = simplejson.load(request)
			finally:
				request.close()
			
			names = json.get('geonames', [])
			if len(names) > 0:
				name = names[0]['name']
				slug = slugify(name)
				
				try:
					self.area = Area.objects.get(
						slug = slug
					)
				except Area.DoesNotExist:
					self.area = Area.objects.create(
						name = name,
						slug = slug
					)
					
		super(Postcode, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ('postcode',)

class Area(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, unique = True)
	
	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return ('area', [self.slug])
	
	class Meta:
		ordering = ('slug',)