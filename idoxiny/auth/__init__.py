from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from oauth.oauth import OAuthConsumer, OAuthRequest, OAuthToken, OAuthSignatureMethod_HMAC_SHA1
from httplib import HTTPConnection, HTTPSConnection
from urllib import urlopen

SIGNATURE_METHOD = OAuthSignatureMethod_HMAC_SHA1

def redirect(key, secret, request):
	consumer = OAuthConsumer(
		str(key),
		str(secret)
	)
	
	oauth_request = OAuthRequest.from_consumer_and_token(
		consumer, http_url = 'https://twitter.com/oauth/request_token'
	)
	
	oauth_request.sign_request(SIGNATURE_METHOD(), consumer, None)
	url = oauth_request.to_url()
	
	connection = HTTPSConnection('twitter.com')
	connection.request(oauth_request.http_method, url)
	response = connection.getresponse()
	resp = response.read()
	
	token = OAuthToken.from_string(resp)
	request.session['unauth_token'] = token
	
	auth_url = 'https://twitter.com/oauth/authorize'
	if isinstance(auth_url, (list, tuple)):
		params = auth_url[1]
		auth_url = auth_url[0]
	else:
		params = {}
	
	oauth_request = OAuthRequest.from_consumer_and_token(
		consumer, token = token,
		http_url = auth_url, parameters = params
	)
	
	oauth_request.sign_request(SIGNATURE_METHOD(), consumer, token)
	
	if request.is_ajax():
		return HttpResponse(
			'<script>document.location = \'%s\';</script>' % oauth_request.to_url()
		)
	else:
		return HttpResponseRedirect(
			oauth_request.to_url()
		)
	
def callback(key, secret, request):
	token = request.session.get('unauth_token')
	if not token:
		raise Exception('No unauthorised token')
	
	if token.key != request.GET.get('oauth_token', None):
		raise Exception('Token does not match')
	
	verifier = request.GET.get('oauth_verifier')
	consumer = OAuthConsumer(
		str(key), str(secret)
	)
	
	oauth_request = OAuthRequest.from_consumer_and_token(
		consumer, token = token,
		http_url = 'https://twitter.com/oauth/access_token',
		parameters = {
			'oauth_verifier': verifier
		}
	)
	
	oauth_request.sign_request(SIGNATURE_METHOD(), consumer, token)
	url = oauth_request.to_url()
	
	access_token = OAuthToken.from_string(
		urlopen(url).read()
	)
	
	return access_token
	
def tweet(text):
	if len(text) > 140 or not text:
		return
	
	from twitter import Api
	from django.conf import settings
	
	api = Api(
		getattr(settings, 'DO_TWITTER_CONSUMER_KEY'),
		getattr(settings, 'DO_TWITTER_CONSUMER_SECRET'),
		getattr(settings, 'TWITTER_ACCESS_TOKEN_KEY'),
		getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET')
	)
	
	return api.PostUpdate(text)

def follow(username):
	from twitter import Api
	from django.conf import settings
	
	api = Api(
		getattr(settings, 'DO_TWITTER_CONSUMER_KEY'),
		getattr(settings, 'DO_TWITTER_CONSUMER_SECRET'),
		getattr(settings, 'TWITTER_ACCESS_TOKEN_KEY'),
		getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET')
	)
	
	return api.CreateFriendship(username)