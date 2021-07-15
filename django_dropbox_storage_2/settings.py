from django.conf import settings

DEFAULT_ROOT_FOLDER = '/'

CONSUMER_KEY = getattr(settings, 'DROPBOX_CONSUMER_KEY', None)

CONSUMER_SECRET = getattr(settings, 'DROPBOX_CONSUMER_SECRET', None)

ACCESS_TOKEN = getattr(settings, 'DROPBOX_ACCESS_TOKEN', None)

ROOT_FOLDER = getattr(settings, 'DROPBOX_ROOT_FOLDER', DEFAULT_ROOT_FOLDER)
