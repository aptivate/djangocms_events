from __future__ import absolute_import, unicode_literals

from cms.test_utils.testcases import CMSTestCase
import cms.api
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date

from django_dynamic_fixture import G
from django_harness.app_testing import AppTestMixin, cms_app_urls_changed
from django_harness.fast_dispatch import FastDispatchMixin

from .helper import create_event
from ..models import Event


class EventListTests(FastDispatchMixin, CMSTestCase):
    def setUp(self):
        home_page = cms.api.create_page('Home', 'base.html', 'en', 
            published=True)
        events_page = cms.api.create_page('Events', 'base.html', 'en', 
            published=True, slug="events", apphook='DjangoCmsEventsListApp')

    def create_event(self, **kwargs):
        return create_event(**kwargs)

    def test_event_list_contains_events(self):
        expected_events = [
            self.create_event(),
            self.create_event(),
            self.create_event(),
            self.create_event(),
            self.create_event(),
        ]
        response = self.client.get(reverse('event_list'))
        for event in expected_events:
            self.assertContains(response, event.title)

    def test_event_list_view_contains_publication_date(self):
        event = self.create_event()
        response = self.client.get(reverse('event_list'))
        self.assertContains(response,
                        date(event.start_date, "N j, Y"))

    def test_event_list_view_contains_title(self):
        event = self.create_event(title="Hello")
        response = self.client.get(reverse('event_list'))
        self.assertContains(response, event.title)

    def test_first_page_of_events_list_contains_first_ten_items(self):
        expected_events = [create_event() for _ in range(0, 20)]
        for event in expected_events:
            event.title = "Event {0}".format(event.title)
            event.save()

        response = self.client.get(reverse('event_list'))

        for event in expected_events[:10]:
            self.assertContains(response, event.title)
        for event in expected_events[10:]:
            self.assertNotContains(response, event.title)
    
    def test_second_page_of_events_list_contains_last_ten_items(self):
        expected_events = [create_event() for _ in range(0, 20)]
        for event in expected_events:
            event.title = "Event {0}".format(event.title)
            event.save()
        response = self.fast_dispatch('event_list', get_params={'page': '2'})
        for event in expected_events[10:]:
            self.assertContains(response, event.title)
        for event in expected_events[:10]:
            self.assertNotContains(response, event.title)
