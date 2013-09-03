from django.db import models
from idoxiny.skills import managers
from django.db.models import Count

class Skill(models.Model):
	name = models.CharField(max_length = 50)
	slug = models.SlugField(max_length = 50, unique = True)
	objects = managers.SkillManager()
	
	def __unicode__(self):
		return self.name
	
	@models.permalink
	def get_absolute_url(self):
		return ('skill', [self.slug])
	
	class Meta:
		ordering = ('slug',)
	
	class QuerySet(models.query.QuerySet):
		def cloud(self):
			numbered = [
				n for n in
				self.annotate(
					count = Count('doers')
				).filter(
					count__gt = 0
				).values_list(
					'count', flat = True
				).order_by('count')
			]
			
			min_size = 1
			max_size = 4
			min_number = numbered[0]
			max_number = numbered[-1]
			
			cloud = []
			for skill in self.all().filter(doers__isnull = False).distinct():
				size = min_size + (
					(
						max_number - (max_number - (skill.doers.count() - min_number))
					) * (
						max_size - min_size
					) / (
						(max_number - min_number) or 1
					)
				)
				
				cloud.append(
					{
						'name': skill.name,
						'slug': skill.slug,
						'url': skill.get_absolute_url(),
						'size': size
					}
				)
			
			return cloud

class Profile(models.Model):
	username = models.CharField(max_length = 50, unique = True)
	description = models.CharField(max_length = 200, null = True, blank = True)
	url = models.CharField(max_length = 255, null = True, blank = True)
	has_skills = models.ManyToManyField('Skill', related_name = 'doers', null = True, blank = True)
	required_skills = models.ManyToManyField('Skill', related_name = 'seekers', null = True, blank = True)
	postcode = models.ForeignKey('geo.Postcode', related_name = 'profiles')
	posted = models.DateTimeField(auto_now_add = True, auto_now = True)
	objects = managers.ProfileManager()
	
	def __unicode__(self):
		return self.username
	
	@models.permalink
	def get_absolute_url(self):
		return ('profile', [self.username])
	
	class Meta:
		ordering = ('-posted',)
		get_latest_by = 'posted'
	
	class QuerySet(models.query.QuerySet):
		def near(self, latitude, longitude):
			sql = """((ACOS(SIN(%(latitude)s * PI() / 180) * 
			SIN(`%(Postcode)s`.`latitude` * PI() / 180) + COS(%(latitude)s * PI() / 180) *
			COS(`%(Postcode)s`.`latitude` * PI() / 180) * COS((%(longitude)s - 
			`%(Postcode)s`.`longitude`) * PI() / 180)) * 180 / PI()) * 60 * 1.1515) <= 25""" % {
				'latitude': latitude,
				'longitude': longitude,
				'Postcode': Postcode._meta.db_table
			}
			
			return self.select_related().extra(
				where = [sql]
			).distinct()
			
class Tweets(models.Model):
	profile = models.ForeignKey('Profile', related_name = 'tweets')
	text = models.CharField(max_length = 140)
	posted = models.DateTimeField(auto_now_add = True)
	
	def __unicode__(self):
		return self.text
	
	class Meta:
		ordering = ('-posted',)
		get_latest_by = 'posted'