# Django development settings for sikteeri project.

from os import environ
import json
import django.conf.global_settings as DEFAULT_SETTINGS
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONFIGURATION = environ.get('SIKTEERI_CONFIGURATION', '')
if not CONFIGURATION:
    msg = """No configuration found.
        Set environment variable SIKTEERI_CONFIGURATION to a json
        config file path or 'dev' for development.

        export SIKTEERI_CONFIGURATION=dev"""
    raise SystemExit(msg)

if CONFIGURATION == 'dev':
    # SECURITY WARNING: don't run with debug turned on in production!
    # We don't make it possible to set DEBUG on from config file.
    DEBUG = True
    TEMPLATE_DEBUG = True
    #DEBUG_TOOLBAR_PATCH_SETTINGS = False
    CONFIGURATION = os.path.join(BASE_DIR, 'config-dev.json')
    config = {}
else:
    DEBUG = False
    TEMPLATE_DEBUG = False

with open(CONFIGURATION, 'rb') as f:
    try:
        config = json.load(f)
    except ValueError as ve:
        raise SystemExit("Config JSON syntax error: {}".format(ve))
assert config.__class__ == dict, "Config must be dictionary"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('SECRET_KEY')

# Where to put collectstatic output
STATIC_ROOT = config.get('STATIC_ROOT', None)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config.get('ALLOWED_HOSTS', [])

USE_X_FORWARDED_HOST = bool(config.get('USE_X_FORWARDED_HOST', False))

# Database is configured from DATABASE_URL
DATABASE_URL = config.get('DATABASE_URL', '')
DATABASES = dict(default=dj_database_url.parse(DATABASE_URL))

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# http://www.i18nguy.com/unicode/language-identifiers.html
TIME_ZONE = config.get('TIME_ZONE', 'Europe/Helsinki')
SHORT_DATE_FORMAT = config.get('SHORT_DATE_FORMAT', 'd.m.Y')
LANGUAGE_CODE = config.get('LANGUAGE_CODE', 'fi-fi')

# URL base for static files
STATIC_URL = config.get('STATIC_URL', '/static/')

# If set, this string will be displayed and sikteeri is disabled
MAINTENANCE_MESSAGE = config.get('MAINTENANCE_MESSAGE', None)

# Show 30 items per page in listview
ENTRIES_PER_PAGE= int(config.get('ENTRIES_PER_PAGE', 30))

# Hosts allowed to fetch statistics etc. without authentication
TRUSTED_HOSTS = config.get('TRUSTED_HOSTS', [])

# Helper function
def get_required(key):
    value = config.get(key)
    if not value:
        raise SystemExit('{0} needs to be set in config'.format(key))
    return value

# Billing settings
IBAN_ACCOUNT_NUMBER = get_required('IBAN_ACCOUNT_NUMBER')
BIC_CODE = get_required('BIC_CODE')
BILLING_FROM_EMAIL = get_required('BILLING_FROM_EMAIL')
BILLING_CC_EMAIL = config.get('BILLING_CC_EMAIL')
BILL_SUBJECT = get_required('BILL_SUBJECT')
REMINDER_SUBJECT = get_required('REMINDER_SUBJECT')

# Send bills how many days before new cycle starts
BILL_DAYS_BEFORE_CYCLE = int(get_required('BILL_DAYS_BEFORE_CYCLE'))

# New bills will have a due date how many days in the future?
BILL_DAYS_TO_DUE = int(get_required('BILL_DAYS_TO_DUE'))

# Send reminders how many days after previous due date?
REMINDER_GRACE_DAYS = int(get_required('REMINDER_GRACE_DAYS'))
ENABLE_REMINDERS = config.get('ENABLE_REMINDERS', False)

# If set, a copy of reminders is sent to account@domain
UNIX_EMAIL_DOMAIN = config.get('UNIX_EMAIL_DOMAIN', None)

# Generic email settings
FROM_EMAIL = get_required('FROM_EMAIL')
SYSADMIN_EMAIL = get_required('SYSADMIN_EMAIL')

# When PRODUCTION is true, show production graphics and colours.
# Otherwise indicate that this is a development environment (logo, colour)
PRODUCTION = config.get('PRODUCTION', False)

######################################################
# Implementation details below - should not need
# operational configuration
######################################################

LOGIN_REDIRECT_URL = 'frontpage'

# Always 1 - sites not implemented
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sikteeri/static'),
    os.path.join(BASE_DIR, 'membership/static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'sikteeri/templates/'),
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "sikteeri.context_processors.is_production",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'membership',
    'services',
    'south',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'sikteeri.ForceDefaultLanguageMiddleware.ForceDefaultLanguageMiddleware',
    'sikteeri.GitVersionHeaderMiddleware.GitVersionHeaderMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# This shouldn't have to be configurable. Why would anyone run
# non-TLS non-debug site? Or run debug over TLS...
if DEBUG:
    SESSION_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SECURE = True

# No need for javascript to access the session cookie
SESSION_COOKIE_HTTPONLY = True

ROOT_URLCONF = 'sikteeri.urls'

WSGI_APPLICATION = 'sikteeri.wsgi.application'

LOGIN_URL = 'login'

SOUTH_TESTS_MIGRATE = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Paper reminder templates
PAPER_REMINDER_TEMPLATE = '/dev/null'

#####################################################
## Logging configuration
#####################################################

ADMINS = config.get('ADMINS')
MANAGERS = config.get('MANAGERS')

## FIXME: should be configured from configuration file

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'sikteeri': {
            'handlers': ['console'],
        },
    }
}

#####################################################
## Email configuration
#####################################################

EMAIL_SUBJECT_PREFIX = get_required('EMAIL_SUBJECT_PREFIX')
EMAIL_MBOX_FILE_PATH = config.get('EMAIL_MBOX_FILE_PATH', None)

if EMAIL_MBOX_FILE_PATH:
    print "Emails redirected to {0}".format(EMAIL_MBOX_FILE_PATH)
    EMAIL_BACKEND = 'sikteeri.mboxemailbackend.EmailBackend'
elif not PRODUCTION:
    print "Console email backend in use"
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
else:
    raise NotImplementedError("Production email configuration to be verified")

#####################################################
## LDAP support
#####################################################

AUTH_USE_LDAP = config.get('AUTH_USE_LDAP', False)

if AUTH_USE_LDAP:
    from django_auth_ldap.config import LDAPSearch
    from django_auth_ldap.config import GroupOfNamesType
    import ldap

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    AUTH_LDAP_SERVER_URI = config.get('AUTH_LDAP_SERVER_URI')
    AUTH_LDAP_START_TLS = config.get('AUTH_LDAP_START_TLS', False)

    # Use anonymous binding
    AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = config.get(
        'AUTH_LDAP_BIND_AS_AUTHENTICATING_USER', True)
    AUTH_LDAP_BIND_DN = config.get('AUTH_LDAP_BIND_DN', '')
    AUTH_LDAP_BIND_PASSWORD = config.get('AUTH_LDAP_BIND_PASSWORD', '')

    # direct search for users
    AUTH_LDAP_USER_DN_TEMPLATE = config.get('AUTH_LDAP_USER_DN_TEMPLATE')
    assert AUTH_LDAP_USER_DN_TEMPLATE is None or \
           '%(user)s' in AUTH_LDAP_USER_DN_TEMPLATE, \
           "AUTH_LDAP_USER_DN_TEMPLATE must contain %(user)s"

    AUTH_LDAP_USER_ATTR_MAP = config.get('AUTH_LDAP_USER_ATTR_MAP',
        { "first_name": "givenName", "last_name": "sn" })

    # Get groups from ldap
    AUTH_LDAP_FIND_GROUP_PERMS = config.get('AUTH_LDAP_FIND_GROUP_PERMS', False)
    if AUTH_LDAP_FIND_GROUP_PERMS:
        AUTH_LDAP_GROUP_SEARCH_DN = config.get('AUTH_LDAP_GROUP_SEARCH_DN')
        assert AUTH_LDAP_GROUP_SEARCH_DN, \
               "Need AUTH_LDAP_GROUP_SEARCH_DN to find groups"

        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
            AUTH_LDAP_GROUP_SEARCH_DN,
            ldap.SCOPE_ONELEVEL,
            "(objectClass=groupOfNames)")
        # set ldap groups type to GroupOfNames
        AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

        # map groups to permissions
        AUTH_LDAP_USER_FLAGS_BY_GROUP = config.get(
            'AUTH_LDAP_USER_FLAGS_BY_GROUP',
            {})

    AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = config.get(
        'AUTH_LDAP_PROFILE_FLAGS_BY_GROUP',
        {})

    # update permissions on every login
    AUTH_LDAP_ALWAYS_UPDATE_USER = config.get('AUTH_LDAP_ALWAYS_UPDATE_USER',
                                              True)

    # cache groups for 5 minutes by default
    AUTH_LDAP_CACHE_GROUPS = config.get('AUTH_LDAP_CACHE_GROUPS', True)
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = config.get('AUTH_LDAP_GROUP_CACHE_TIMEOUT',
                                               300)

