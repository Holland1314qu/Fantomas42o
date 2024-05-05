"""Settings of Zinnia"""
import os
from django.conf import settings

PING_DIRECTORIES = getattr(settings, 'ZINNIA_PING_DIRECTORIES',
                           ('http://django-blog-zinnia.com/xmlrpc/',))
SAVE_PING_DIRECTORIES = getattr(settings, 'ZINNIA_SAVE_PING_DIRECTORIES',
                                bool(PING_DIRECTORIES))
SAVE_PING_EXTERNAL_URLS = getattr(settings, 'ZINNIA_PING_EXTERNAL_URLS', True)

COPYRIGHT = getattr(settings, 'ZINNIA_COPYRIGHT', 'Zinnia')

PAGINATION = getattr(settings, 'ZINNIA_PAGINATION', 10)
ALLOW_EMPTY = getattr(settings, 'ZINNIA_ALLOW_EMPTY', True)
ALLOW_FUTURE = getattr(settings, 'ZINNIA_ALLOW_FUTURE', True)

ENTRY_TEMPLATES = getattr(settings, 'ZINNIA_ENTRY_TEMPLATES', [])
ENTRY_BASE_MODEL = getattr(settings, 'ZINNIA_ENTRY_BASE_MODEL', '')

WYSIWYG = getattr(settings, 'ZINNIA_WYSIWYG',
                  'tinymce' in settings.INSTALLED_APPS \
                  and 'tinymce' or 'wymeditor')

MAIL_COMMENT = getattr(settings, 'ZINNIA_MAIL_COMMENT', True)
MAIL_COMMENT_REPLY = getattr(settings, 'ZINNIA_MAIL_COMMENT_REPLY', False)
AKISMET_COMMENT = getattr(settings, 'ZINNIA_AKISMET_COMMENT', True)

UPLOAD_TO = getattr(settings, 'ZINNIA_UPLOAD_TO', 'uploads')

PROTOCOL = getattr(settings, 'ZINNIA_PROTOCOL', 'http')
MEDIA_URL = getattr(settings, 'ZINNIA_MEDIA_URL',
                    os.path.join(settings.MEDIA_URL, 'zinnia/'))

FEEDS_FORMAT = getattr(settings, 'ZINNIA_FEEDS_FORMAT', 'rss')
FEEDS_MAX_ITEMS = getattr(settings, 'ZINNIA_FEEDS_MAX_ITEMS', 15)

PINGBACK_CONTENT_LENGTH = getattr(settings,
                                  'ZINNIA_PINGBACK_CONTENT_LENGTH', 300)

F_MIN = getattr(settings, 'ZINNIA_F_MIN', 0.1)
F_MAX = getattr(settings, 'ZINNIA_F_MAX', 1.0)

USE_BITLY = getattr(settings, 'ZINNIA_USE_BITLY',
                    'django_bitly' in settings.INSTALLED_APPS)

try:
    import tweepy
    USE_TWITTER = getattr(settings, 'ZINNIA_USE_TWITTER', True)
except ImportError:
    USE_TWITTER = False

TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')
TWITTER_ACCESS_KEY = getattr(settings, 'TWITTER_ACCESS_KEY', '')
TWITTER_ACCESS_SECRET = getattr(settings, 'TWITTER_ACCESS_SECRET', '')
