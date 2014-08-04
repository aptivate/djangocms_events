from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.template.defaultfilters import date

import cms.api
from cms.test_utils.testcases import CMSTestCase
from django_dynamic_fixture import G
from django_harness.fast_dispatch import FastDispatchMixin
from django_harness.override_settings import override_settings

from .helper import create_event
from ..models import Event


@override_settings(ROOT_URLCONF="events.tests.test_urls", LANGUAGE_CODE='en')
class EventDetailsTests(FastDispatchMixin, CMSTestCase):
    def setUp(self):
        super(EventDetailsTests, self).setUp()
        # needed for reverse lookups on pages to work properly
        self.root_page = cms.api.create_page('Home', 'base.html', 'en', 
            published=True)
        self.events_page = cms.api.create_page('Events', 'base.html', 'en', 
            reverse_id='events', slug='event', published=True)
            # apphook='EventsApp')

    def request_hook(self, request):
        super(EventDetailsTests, self).request_hook(request)
        request.current_page = self.events_page

    def test_event_details_view_has_event_as_object_in_context(self):
        event = create_event()
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertEqual(200, response.status_code)
        self.assertEqual(event, response.context_data["object"])

    def test_event_details_view_contains_additional_information(self):
        event = create_event(additional_information="Hello")
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, "Hello")

    def test_event_details_view_contains_start_date(self):
        event = create_event()
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, date(event.start_date, "N j, Y"))

    def test_event_details_view_contains_title(self):
        event = create_event(title="Hello")
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, event.title)

    def test_event_details_view_contains_host_country(self):
        event = create_event(location="Spain")
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, "Spain")

    def test_event_details_view_contains_summary(self):
        event = create_event(description="It is hot!")
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, "It is hot!")

    def test_event_details_view_contains_additional_information(self):
        event = create_event(additional_information="Damn hot!")
        response = self.fast_dispatch('event_detail', url_args=[event.id])
        self.assertContains(response, "Damn hot!")
