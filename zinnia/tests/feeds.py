"""Test cases for Zinnia's feeds"""
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from tagging.models import Tag

from zinnia.models import Entry
from zinnia.models import Category
from zinnia.managers import PUBLISHED
from zinnia.feeds import ImgParser
from zinnia.feeds import EntryFeed
from zinnia.feeds import LatestEntries
from zinnia.feeds import CategoryEntries
from zinnia.feeds import AuthorEntries
from zinnia.feeds import TagEntries
from zinnia.feeds import SearchEntries
from zinnia.feeds import EntryDiscussions
from zinnia.feeds import EntryComments
from zinnia.feeds import EntryPingbacks
from zinnia.feeds import EntryTrackbacks


class ZinniaFeedsTestCase(TestCase):
    """Test cases for the Feed classes provided"""
    urls = 'zinnia.tests.urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.author = User.objects.create(username='admin',
                                          email='admin@example.com')
        self.category = Category.objects.create(title='Tests', slug='tests')
        self.entry_ct_id = ContentType.objects.get_for_model(Entry).pk

    def test_img_parser(self):
        parser = ImgParser()
        parser.feed('')
        self.assertEquals(len(parser.img_locations), 0)
        parser.feed('<img title="image title" />')
        self.assertEquals(len(parser.img_locations), 0)
        parser.feed('<img src="image.jpg" />' \
                    '<img src="image2.jpg" />')
        self.assertEquals(len(parser.img_locations), 2)

    def create_published_entry(self):
        params = {'title': 'My test entry',
                  'content': 'My test content with image <img src="/image.jpg" />',
                  'slug': 'my-test-entry',
                  'tags': 'tests',
                  'creation_date': datetime(2010, 1, 1),
                  'status': PUBLISHED}
        entry = Entry.objects.create(**params)
        entry.sites.add(self.site)
        entry.categories.add(self.category)
        entry.authors.add(self.author)
        return entry

    def create_discussions(self, entry):
        comment = Comment.objects.create(comment='My Comment',
                                         user=self.author,
                                         content_object=entry,
                                         site=self.site)
        pingback = Comment.objects.create(comment='My Pingback',
                                          user=self.author,
                                          content_object=entry,
                                          site=self.site)
        pingback.flags.create(user=self.author, flag='pingback')
        trackback = Comment.objects.create(comment='My Trackback',
                                           user=self.author,
                                           content_object=entry,
                                           site=self.site)
        trackback.flags.create(user=self.author, flag='trackback')
        return [comment, pingback, trackback]

    def test_feed_entry(self):
        entry = self.create_published_entry()
        feed = EntryFeed()
        self.assertEquals(feed.item_pubdate(entry), entry.creation_date)
        self.assertEquals(feed.item_categories(entry), [self.category.title])
        self.assertEquals(feed.item_author_name(entry), self.author.username)
        self.assertEquals(feed.item_author_email(entry), self.author.email)
        self.assertEquals(feed.item_author_link(entry),
                          'http://example.com/authors/%s/' % self.author.username)
        self.assertEquals(feed.item_enclosure_url(entry), 'http://example.com/image.jpg')
        self.assertEquals(feed.item_enclosure_length(entry), '100000')
        self.assertEquals(feed.item_enclosure_mime_type(entry), 'image/jpeg')

    def test_latest_entries(self):
        self.create_published_entry()
        feed = LatestEntries()
        self.assertEquals(feed.link(), '/')
        self.assertEquals(len(feed.items()), 1)

    def test_category_entries(self):
        self.create_published_entry()
        feed = CategoryEntries()
        self.assertEquals(feed.get_object('request', '/tests/'), self.category)
        self.assertEquals(len(feed.items(self.category)), 1)
        self.assertEquals(feed.link(self.category), '/categories/tests/')

    def test_author_entries(self):
        self.create_published_entry()
        feed = AuthorEntries()
        self.assertEquals(feed.get_object('request', 'admin'), self.author)
        self.assertEquals(len(feed.items(self.author)), 1)
        self.assertEquals(feed.link(self.author), '/authors/admin/')

    def test_tag_entries(self):
        self.create_published_entry()
        feed = TagEntries()
        self.assertEquals(feed.get_object('request', 'tests').name, 'tests')
        self.assertEquals(len(feed.items('tests')), 1)
        self.assertEquals(feed.link(Tag(name='tests')), '/tags/tests/')

    def test_search_entries(self):
        self.create_published_entry()
        feed = SearchEntries()
        self.assertEquals(feed.get_object('request', 'test'), 'test')
        self.assertEquals(len(feed.items('test')), 1)
        self.assertEquals(feed.link('test'), '/search/?pattern=test')

    def test_entry_discussions(self):
        entry = self.create_published_entry()
        comments = self.create_discussions(entry)
        feed = EntryDiscussions()
        self.assertEquals(feed.get_object('request', entry.slug), entry)
        self.assertEquals(feed.link(entry), '/2010/01/01/my-test-entry/')
        self.assertEquals(len(feed.items(entry)), 3)
        self.assertEquals(feed.item_pubdate(comments[0]), comments[0].submit_date)
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#c1' % self.entry_ct_id)
        self.assertEquals(feed.item_author_name(comments[0]), 'admin')
        self.assertEquals(feed.item_author_email(comments[0]), 'admin@example.com')
        self.assertEquals(feed.item_author_link(comments[0]), '')

    def test_entry_comments(self):
        entry = self.create_published_entry()
        comments = self.create_discussions(entry)
        feed = EntryComments()
        self.assertEquals(list(feed.items(entry)), [comments[0]])
        self.assertEquals(feed.item_link(comments[0]),
                          '/comments/cr/%i/1/#comment_1' % self.entry_ct_id)

    def test_entry_pingbacks(self):
        entry = self.create_published_entry()
        comments = self.create_discussions(entry)
        feed = EntryPingbacks()
        self.assertEquals(list(feed.items(entry)), [comments[1]])
        self.assertEquals(feed.item_link(comments[1]),
                          '/comments/cr/%i/1/#pingback_2' % self.entry_ct_id)

    def test_entry_trackbacks(self):
        entry = self.create_published_entry()
        comments = self.create_discussions(entry)
        feed = EntryTrackbacks()
        self.assertEquals(list(feed.items(entry)), [comments[2]])
        self.assertEquals(feed.item_link(comments[2]),
                          '/comments/cr/%i/1/#trackback_3' % self.entry_ct_id)
