from __future__ import unicode_literals, absolute_import

from django.template.defaultfilters import striptags
from django.test.testcases import TestCase
from django.utils.datetime_safe import date
from django.utils.translation import ugettext as _

from django_dynamic_fixture import G
from django_harness.fast_dispatch import FastDispatchMixin
from django_harness.whoosh_testing import WhooshTestMixin
from mock import patch

from .helper import create_event


from django.test.utils import override_settings
@override_settings(ROOT_URLCONF="events.tests.test_urls")
class SearchMethodTests(WhooshTestMixin, FastDispatchMixin, TestCase):

    """
     There are some methods on the event model that exist solely to squeeze it
     in to the search template. This class tests them.
    """

    longMessage = True

    def search(self, **kwargs):
        # no direct access to the rendered context, so get the arguments
        # passed to render_to_string() by mocking it instead.
        with patch('django.shortcuts.loader.render_to_string') as patched_render:
            response = self.fast_dispatch('event_search', get_params=kwargs)
        self.assertEqual(200, response.status_code)

        context = patched_render.call_args[0][1]
        objects = [r.object for r in context['results']]
        return sorted(objects, key=lambda object: object.id)

    def test_search_form_includes_date_fields(self):
        response = self.fast_dispatch('event_search')
        self.assertContains(response, 
            '<select class="month_selector" id="id_from_month" name="from_month">')
        self.assertContains(response, 
            '<select class="year_selector" id="id_from_year" name="from_year">')
        self.assertContains(response, 
            '<select class="month_selector" id="id_to_month" name="to_month">')
        self.assertContains(response, 
            '<select class="year_selector" id="id_to_year" name="to_year">')

    def test_search_by_date(self):
        from datetime import date
        fool   = create_event(title="April Fools", start_date=date(2013,04,01))
        may    = create_event(title="Month of May", start_date=date(2013,05,01), 
            end_date=date(2013,05,31))
        spring = create_event(title="Spring", start_date=date(2013,03,01), 
            end_date=date(2013,05,31))

        self.assertEqual([], 
            self.search(from_month='6', from_year='2013'),
            "No events end on or after 1/6/2013")
        self.assertEqual([may, spring], 
            self.search(from_month='5', from_year='2013'),
            "Two events end on or after 1/5/2013")
        self.assertEqual([fool, may, spring], 
            self.search(from_month='4', from_year='2013'),
            "All three events end on or after 1/4/2013")

        self.assertEqual([spring], 
            self.search(from_month='3', from_year='2013',
                to_month='3', to_year='2013'),
            "One event is running during March 2013")
        self.assertEqual([fool, spring], 
            self.search(from_month='4', from_year='2013',
                to_month='4', to_year='2013'),
            "Two events are running during April 2013")
        self.assertEqual([may, spring], 
            self.search(from_month='5', from_year='2013',
                to_month='5', to_year='2013'),
            "Two events are running during May 2013")

        self.assertEqual([], 
            self.search(to_month='2', to_year='2013'),
            "No events start before or in February 2013")
        self.assertEqual([spring], 
            self.search(to_month='3', to_year='2013'),
            "One event starts before or in March 2013")
        self.assertEqual([fool, spring], 
            self.search(to_month='4', to_year='2013'),
            "Two events start before or in April 2013")
        self.assertEqual([fool, may, spring], 
            self.search(to_month='5', to_year='2013'),
            "Two events start before or in May 2013")

    def test_event_details_in_text_field(self):
        from datetime import date
        event = create_event(title="whee", description="Halloween!",
            additional_information="Time to go trick or treating",
            location="Everywhere", attendees="Small children",
            contact_name="All parents", contact_email="email@example.com",
            contact_phone="1234567890", start_date=date(2013,10,31),
            end_date=date(2013,11,01))

        from ..models import Event
        index = self.get_search_index(Event)
        keys = index.prepare(event)
        text = keys['text']

        self.assertIn("whee", text)
        self.assertIn("Halloween!", text)
        self.assertIn("Time to go trick or treating", text)
        self.assertIn("Everywhere", text)
        self.assertIn("Small children", text)
        self.assertIn("All parents", text)
        self.assertIn("email@example.com", text)
        self.assertIn("1234567890", text)
        self.assertIn("2013-10-31", text)
        self.assertIn("2013-11-01", text)
