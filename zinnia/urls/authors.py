"""Urls for the Zinnia authors"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

from zinnia.models import Author

author_conf = {'queryset': Author.published.all()}

urlpatterns = patterns('zinnia.views.authors',
                       url(r'^$', 'author_list',
                           author_conf, 'zinnia_author_list'),
                       url(r'^(?P<username>[.+-@\w]+)/$', 'author_detail',
                           name='zinnia_author_detail'),
                       url(r'^(?P<username>[.+-@\w]+)/page/(?P<page>\d+)/$',
                           'author_detail',
                           name='zinnia_author_detail_paginated'),
                       )
