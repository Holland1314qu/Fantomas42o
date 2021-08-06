"""Models of Zinnia"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import linebreaks
from django.contrib.comments.moderation import moderator
from django.utils.translation import ugettext, ugettext_lazy as _

from tagging.fields import TagField

from zinnia.moderator import EntryCommentModerator
from zinnia.managers import entries_published
from zinnia.managers import EntryPublishedManager
from zinnia.managers import DRAFT, HIDDEN, PUBLISHED
from zinnia.settings import USE_BITLY
from zinnia.settings import UPLOAD_TO


class Category(models.Model):
    """Category object for Entry"""

    title = models.CharField(_('title'), max_length=50)
    slug = models.SlugField(help_text=_('used for publication'))
    description = models.TextField(_('description'), blank=True)

    def entries_published_set(self):
        """Return only the entries published"""
        return entries_published(self.entry_set)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('zinnia_category_detail', (self.slug, ))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['title']


class Entry(models.Model):
    """Base design for publishing entry"""
    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    title = models.CharField(_('title'), max_length=100)

    image = models.ImageField(_('image'), upload_to=UPLOAD_TO,
                              blank=True, help_text=_('used for illustration'))
    content = models.TextField(_('content'))
    excerpt = models.TextField(_('excerpt'), blank=True,
                                help_text=_('optional element'))

    tags = TagField()
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))
    related = models.ManyToManyField('self', verbose_name=_('related entries'),
                                     blank=True, null=True)

    slug = models.SlugField(help_text=_('used for publication'))
    authors = models.ManyToManyField(User, verbose_name=_('authors'),
                                     blank=True, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    comment_enabled = models.BooleanField(_('comment enabled'), default=True)

    creation_date = models.DateTimeField(_('creation date'), default=datetime.now)
    last_update = models.DateTimeField(_('last update'), default=datetime.now)
    start_publication = models.DateTimeField(_('start publication'),
                                             help_text=_('date start publish'),
                                             default=datetime.now)
    end_publication = models.DateTimeField(_('end publication'),
                                           help_text=_('date end publish'),
                                           default=datetime(2042, 3, 15))

    sites = models.ManyToManyField(Site, verbose_name=_('sites publication'))

    objects = models.Manager()
    published = EntryPublishedManager()

    def get_content(self):
        """Return the content correctly formatted"""
        if not '</p>' in self.content:
            return linebreaks(self.content)
        return self.content

    def get_comments(self):
        """Return published comments"""
        from django.contrib.comments.models import Comment
        return Comment.objects.for_model(self).filter(is_public=True)

    def is_actual(self):
        """Define is an entry is between the date of publication"""
        now = datetime.now()
        return now >= self.start_publication and now < self.end_publication
    is_actual.boolean = True
    is_actual.short_description = _('is actual')

    def is_visible(self):
        """Define if an entry is visible on site"""
        return self.is_actual() and self.status == PUBLISHED
    is_visible.boolean = True
    is_visible.short_description = _('is visible')

    def related_published_set(self):
        """Return only related entries published"""
        return entries_published(self.related)

    def get_short_url(self):
        if not USE_BITLY:
            return False

        from django_bitly.models import Bittle
        
        bittle = Bittle.objects.bitlify(self)
        url = bittle and bittle.shortUrl or self.get_absolute_url()
        return url
    get_short_url.short_description = _('short url')

    def __unicode__(self):
        return '%s: %s' % (self.title, self.get_status_display())

    @models.permalink
    def get_absolute_url(self):
        return ('zinnia_entry_detail', (), {
            'year': self.creation_date.strftime('%Y'),
            'month': self.creation_date.strftime('%m'),
            'day': self.creation_date.strftime('%d'),
            'slug': self.slug})

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        permissions = (('can_view_all', 'Can view all'),
                       ('can_change_author', 'Can change author'), )

moderator.register(Entry, EntryCommentModerator)
