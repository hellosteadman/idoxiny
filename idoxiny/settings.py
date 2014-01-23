from settings_local import *
from os import path

TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Mark Steadman', 'marksteadman@me.com'),
)

MANAGERS = ADMINS
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True
SITE_ROOT = path.abspath(path.dirname(__file__) + '/../')
MEDIA_ROOT = path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '79p(*b1ad8*g+b92ae_7=szx9b$31gzf&ak1cq6&@h8tif8nqr'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'idoxiny.urls'

TEMPLATE_DIRS = (
	path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'bambu.bootstrap.context_processors.basics',
	'idoxiny.geo.context_processors.postcodes',
	'idoxiny.skills.context_processors.skills'
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'raven.contrib.django.raven_compat',
	'south',
	'bambu.navigation',
	'bambu.analytics',
	'bambu.bootstrap.v2',
	'bambu.enqueue',
	'idoxiny.skills',
	'idoxiny.geo'
)

GOOGLE_ANALYTICS_IDS = ('UA-29554105-4',)