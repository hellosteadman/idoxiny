from idoxiny.skills.models import Skill, Profile
from django.conf import settings

def skills(request):
	return {
		'skills': Skill.objects.only('name', 'slug'),
		'doers': Profile.objects.filter(has_skills__isnull = False).distinct(),
		'seekers': Profile.objects.filter(required_skills__isnull = False).distinct(),
		'DO_TWITTER_CONSUMER_KEY': getattr(settings, 'DO_TWITTER_CONSUMER_KEY', '')
	}