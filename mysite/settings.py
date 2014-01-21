"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ujyvdv8t5ua7b6=(cxdt=+#zs9s@=jyym$ni12=^v984g9^4p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
	'freepl',
	'lockdown',
)
"""
here mention where your templates are. so wherever you put the repo, 
just the /home/mj part will change accordingly where you keep 
it
"""


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lockdown.middleware.LockdownMiddleware', 
)

LOCKDOWN_PASSWORDS = ('iwantaccess', )
LOCKDOWN_FORM = 'lockdown.forms.LockdownForm'
ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

"""
As I am using mysql database. 
So following is the details on my local system.
You should first create a database on your own system and then replace
'mydja' with your database name and your username and password
"""
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'mydja',
        'USER': 'root',
        'PASSWORD': '123456', 
        'HOST': 'localhost',
        'PORT': '8000',
    }
}

TEMPLATE_DIRS = '/home/mj/freepl/templates'
PROJECT_DIR='/home/mj/freepl'
STATIC_ROOT = '/home/mj/freepl'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
"""
for the following only the /home/mj part will change depending on where 
you keep this repo
"""
PROJECT_DIR='/home/mj/freepl/'
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)

STATIC_ROOT = '/home/mj/freepl'
STATIC_URL = '/static/'
