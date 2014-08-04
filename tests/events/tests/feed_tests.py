from __future__ import unicode_literals, absolute_import

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.utils import override_settings

from django_harness.fast_dispatch import FastDispatchMixin
import feedparser

from .helper import create_event
from ..models import Event


@override_settings(ROOT_URLCONF="events.tests.test_urls")
class EventFeedTests(FastDispatchMixin, TestCase):

    def get_parsed_feed(self):
        response = self.fast_dispatch('event_feed')
        return feedparser.parse(response.content)

    def assert_feed_contains(self, key, value):
        feed = self.get_parsed_feed()
        self.assertEqual(feed['entries'][0][key], value)

    def test_feed_contains_title(self):
        event = create_event(title="Hello")
        self.assert_feed_contains('title', event.title)

    def test_feed_contains_summary(self):
        event = create_event(description="Goodbye")
        self.assert_feed_contains('description', event.description)

    # categories
    def test_feed_contains_categories(self):
        from ..models import Wossname
        spiders = Wossname.objects.create(name="spiders",
            owner=ContentType.objects.get_for_model(Event))
        create_event(event_type=spiders)
        feed = self.get_parsed_feed()
        self.assertEqual(feed['entries'][0]['tags'][0]['term'], 'spiders')
