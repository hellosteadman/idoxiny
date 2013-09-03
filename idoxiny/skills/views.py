from django.template.response import TemplateResponse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.utils import simplejson
from django.views.decorators.http import require_POST
from idoxiny.skills.models import Skill, Profile
from idoxiny.skills.models import Skill, Profile
from idoxiny.geo.models import Postcode
from idoxiny import auth
from urllib import urlopen
import re, random

POSTCODE_REGEX = re.compile(r'(GIR 0AA)|(((A[BL]|B[ABDHLNRSTX]?|C[ABFHMORTVW]|D[ADEGHLNTY]|E[HNX]?|F[KY]|G[LUY]?|H[ADGPRSUX]|I[GMPV]|JE|K[ATWY]|L[ADELNSU]?|M[EKL]?|N[EGNPRW]?|O[LX]|P[AEHLOR]|R[GHM]|S[AEGKLMNOPRSTY]?|T[ADFNQRSW]|UB|W[ADFNRSV]|YO|ZE)[1-9]?[0-9]|((E|N|NW|SE|SW|W)1|EC[1-4]|WC[12])[A-HJKMNPR-Y]|(SW|W)([2-9]|[1-9][0-9])|EC[1-9][0-9]) [0-9][ABD-HJLNP-UW-Z]{2})')
TWITTER_CONSUMER_KEY = getattr(settings, 'DO_TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = getattr(settings, 'DO_TWITTER_CONSUMER_SECRET')

def signup(request, direction):
	if not direction in ('do', 'seek'):
		raise Http404('Direction not understood')
	
	skills = []
	postcode = ''
	error = None
	key = '%ser'% direction
	
	if request.method == 'POST':
		if request.POST.get('skill-1'):
			skills.append(
				request.POST['skill-1'].lower()
			)
		
		if request.POST.get('skill-2'):
			skills.append(
				request.POST['skill-2'].lower()
			)
		
		if request.POST.get('skill-3'):
			skills.append(
				request.POST['skill-3'].lower()
			)
		
		postcode = request.POST.get('postcode')
		
		if not postcode:
			error = u'Please give us your postcode'
		else:
			postcode = postcode.upper()
			if not POSTCODE_REGEX.match(postcode):
				error = u'Please enter your full postcode (with a space where the space goes)'
		
		if len(skills) == 0:
			if direction == 'do':
				error = u'Please enter some skills; we know you got \'em!'
			else:
				error = u'Please enter the skills you\'re looking for'
		
		for skill in skills:
			if ',' in skill or '/' in skill or '&' in skill or '-and-' in skill or '_and_' in skill or ' and ' in skill:
				error = u'Please don\'t try and split your skills up'
			
			if len(skill.split(' ')) > 3:
				if direction == 'do':
					error = u'Please keep your skills brief'
				else:
					error = u'Please keep your requirements brief'
		
		details = {
			'skills': skills,
			'postcode': postcode
		}
		
		if not error:
			request.session[key] = details
			return auth.redirect(
				getattr(settings, '%s_TWITTER_CONSUMER_KEY' % direction.upper()),
				getattr(settings, '%s_TWITTER_CONSUMER_SECRET' % direction.upper()),
				request
			)
	
	elif request.session.get(key):
		skills = request.session[key].get('skills', [])
		postcode = request.session[key].get('postcode')
	else:
		if 'skill' in request.GET:
			skills = [request.GET.get('skill')]
		
		if 'postcode' in request.GET:
			postcode = request.GET.get('postcode')
	
	return TemplateResponse(
		request,
		'skills/%s/signup.inc.html' % direction,
		{
			'form_skills': skills,
			'form_postcode': postcode,
			'form_error': error
		}
	)

def callback(request, direction):
	if not direction in ('do', 'seek'):
		raise Http404('Direction not understood')
	
	from twitter import Api
	
	result = auth.callback(
		getattr(settings, '%s_TWITTER_CONSUMER_KEY' % direction.upper()),
		getattr(settings, '%s_TWITTER_CONSUMER_SECRET' % direction.upper()),
		request
	)
	
	key = '%ser'% direction
	
	if not result:
		return HttpResponseRedirect('/')
	
	api = Api(
		getattr(settings, '%s_TWITTER_CONSUMER_KEY' % direction.upper()),
		getattr(settings, '%s_TWITTER_CONSUMER_SECRET' % direction.upper()),
		access_token_key = result.key,
		access_token_secret = result.secret
	)
	
	request.session['twitter'] = {
		'key': result.key,
		'secret': result.secret
	}
	
	user = api.VerifyCredentials()
	details = request.session.pop(key, {})
	
	try:
		profile = Profile.objects.get(
			username__iexact = user.screen_name
		)
	except Profile.DoesNotExist:
		profile = Profile(
			username = user.screen_name.lower()
		)
	
	profile.description = user.description
	profile.url = user.url
	
	postcode, created = Postcode.objects.get_or_create(
		postcode = details.get('postcode')
	)
	
	profile.postcode = postcode
	profile.save()
	
	skill_names = details.get('skills', [])
	added_skills = []
	
	if direction == 'do':
		skill_qs = profile.has_skills
	else:
		skill_qs = profile.required_skills
	
	for name in skill_names:
		slug = slugify(name)
		
		try:
			skill = Skill.objects.get(
				slug = slug
			)
		except Skill.DoesNotExist:
			skill = Skill.objects.create(
				name = name,
				slug = slug
			)
		
		if direction == 'do':
			skill_qs.add(skill)
		else:
			skill_qs.add(skill)
		
		added_skills.append(skill.pk)
	
	skill_qs.exclude(pk__in = added_skills).delete()
	
	skill_list = ['#' + skill.slug.replace('-', '').replace('_', '') for skill in skill_qs.all()]
	if len(skill_list) > 1:
		skill_list = '%s or %s' % (
			', '.join(skill_list[0:-1]),
			skill_list[-1]
		)
	else:
		skill_list = skill_list[0]
	
	if direction == 'do':
		patterns = (
			'Contact @%(username)s if you need %(skill_list)s: %(url)s',
			'If you need %(skill_list)s, find @%(username)s: %(url)s',
			'Need %(skill_list)s? Get in touch with @%(username)s: %(url)s',
			'.@%(username)s can do %(skill_list)s. @%(username)s: %(url)s'
		)
	else:
		patterns = (
			'Contact @%(username)s if you can do %(skill_list)s: %(url)s',
			'If you can do %(skill_list)s, find @%(username)s: %(url)s',
			'Freelancer with %(skill_list)s experience? Contact @%(username)s: %(url)s',
			'.@%(username)s needs %(skill_list)s: %(url)s'
		)
		
	tweet = random.choice(patterns) % {
		'username': profile.username,
		'skill_list': skill_list,
		'url': 'http://idoxiny.com%s' % profile.get_absolute_url()
	}
	
	auth.tweet(tweet)
	auth.follow(profile.username)
	
	return HttpResponseRedirect(
		profile.get_absolute_url()
	)

def profile(request, username):
	profile = get_object_or_404(Profile, username__iexact = username)
	
	return TemplateResponse(
		request,
		'skills/profile.html',
		{
			'profile': profile,
			'title_parts': (unicode(profile),),
			'meta_description': profile.description,
			'meta_keywords': [
				s.name for s in profile.has_skills.all()
			] + [
				s.name for s in profile.required_skills.all()
			]
		}
	)

def skills(request):
	return TemplateResponse(
		request,
		'skills/skills.html',
		{
			'cloud': Skill.objects.cloud(),
			'title_parts': (u'Skills',)
		}
	)

def skill(request, slug):
	skill = get_object_or_404(Skill, slug = slug)
	q = Q(profiles__has_skills = skill) | Q(profiles__required_skills = skill)
	
	return TemplateResponse(
		request,
		'skills/skill.html',
		{
			'skill': skill,
			'skill_postcodes': Postcode.objects.filter(q).distinct(),
			'title_parts': (unicode(skill), u'Skills')
		}
	)