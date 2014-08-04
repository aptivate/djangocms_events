from datetime import timedelta

from django.contrib.sites.models import Site
from django.template.defaultfilters import date as print_date
from django.test.utils import override_settings
from django.utils.datetime_safe import date

from cms.models.pagemodel import Page
from cms.models.placeholdermodel import Placeholder
from cms.models.titlemodels import Title
from cms.test_utils.testcases import CMSTestCase
from cms.plugin_rendering import render_plugin
from django_dynamic_fixture import G
from djangocms_events.cms_plugins import EventDetailListPlugin
from djangocms_events.models import EventPluginModel

from .helper import create_event
from .base import EventPluginTestBase, EventPluginCommonTestsMixin

class EventDetailListPluginTests(EventPluginCommonTestsMixin,
    EventPluginTestBase):

    plugin_class = EventDetailListPlugin

    def setUp(self):
        super(EventDetailListPluginTests, self).setUp()

    def test_event_list_contains_events(self):
        expected_events = [create_event(),
                           create_event(),
                           create_event(),
                           create_event(),
                           create_event()]
        rendered_html = self.instance.render_plugin()
        for event in expected_events:
            self.assertIn(event.title, rendered_html)

    def test_event_title_in_details_page(self):
        event = create_event()
        rendered_html = self.instance.render_plugin()
        self.assertIn(event.title, rendered_html)

    def test_location_in_details_page(self):
        event = create_event(location='Australia')
        rendered_html = self.instance.render_plugin()
        self.assertIn('Australia', rendered_html)

    def test_start_date_in_event_list_page(self):
        d = date.today() + timedelta(days=2)
        event = create_event(start_date=d)
        rendered_html = self.instance.render_plugin()
        self.assertIn(print_date(d, "N j, Y"), rendered_html)

    def test_end_date_in_event_list_page(self):
        d = date.today() + timedelta(days=4)
        event = create_event(end_date=d)
        rendered_html = self.instance.render_plugin()
        self.assertIn(print_date(d, "N j, Y"), rendered_html)

    def test_description_displayed_by_plugin(self):
        info = "it's Awesome"
        event = create_event(description=info)
        rendered_html = self.instance.render_plugin()
        self.assertIn(info, rendered_html)

    def test_additional_information_not_displayed_by_plugin(self):
        info = "Wondeful things here"
        event = create_event(additional_information=info)
        rendered_html = self.instance.render_plugin()
        self.assertNotIn(info, rendered_html)

