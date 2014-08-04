from django.test.utils import override_settings

from cms.models.placeholdermodel import Placeholder
from cms.test_utils.testcases import CMSTestCase

from django_harness.plugin_testing import PluginTestMixin
from djangocms_events.models import EventPluginModel

from .helper import create_event
from ..models import Wossname


@override_settings(ROOT_URLCONF="events.tests.test_urls")
class EventPluginTestBase(PluginTestMixin, CMSTestCase):
    plugin_defaults = {'limit': 5}


class EventPluginCommonTestsMixin(object):
    def test_event_title_appears_in_page(self):
        event = create_event(title="Black magic")

        rendered_html = self.instance.render_plugin()
        self.assertIn("Black magic", rendered_html)

    def test_plugin_limits_number_of_events_returned(self):
        expected_news_items = [create_event(), create_event(), create_event()]
        create_event()
        self.instance.limit = 3
        plugin_context = self.plugin.render({}, self.instance, None)
        actual_news_items = plugin_context["events"]
        self.assertSequenceEqual(expected_news_items, actual_news_items)

    def test_event_icon_links_to_event_details(self):
        event = create_event(title="Black magic")

        from django.core.urlresolvers import reverse
        expected_html = ('<a href="%s"><span class="icon icon-event" '
            'aria-hidden="true"></span></a>') % reverse("event_detail",
            args=[event.id])

        rendered_html = self.instance.render_plugin()
        self.assertIn(expected_html, rendered_html)

    def test_plugin_future_and_past_events_list(self):
        from datetime import date, timedelta
        today = date.today()

        old1 = create_event(start_date=today - timedelta(days=1))
        old2 = create_event(start_date=today - timedelta(days=2))
        new1 = create_event(start_date=today + timedelta(days=2))
        new2 = create_event(start_date=today + timedelta(days=1))
        new3 = create_event(start_date=today)
        running = create_event(start_date=today - timedelta(days=3),
            end_date=today)
        
        # Also checks that the events are in the correct order:
        # ascending for future events, descending for past events

        directions = {
            'future': [running, new3, new2, new1],
            'past':   [old1, old2]
        }

        for direction, expected_events in directions.iteritems():
            self.instance.direction = direction
            self.instance.save()
            # force reload to work around model's broken __setattr__
            self.instance = EventPluginModel.objects.get(pk=self.instance.pk)

            context = self.plugin.render({}, self.instance, 
                self.placeholder.slot)
            self.assertEqual(expected_events, list(context['events']))

    def test_plugin_title_shown_on_page(self):
        self.instance.title = 'Funky Happenings'
        self.instance.save()
        # force reload to work around model's broken __setattr__
        self.instance = EventPluginModel.objects.get(pk=self.instance.pk)

        # without any events
        rendered_html = self.instance.render_plugin()
        self.assertIn('<h2 class="latest_title">Funky Happenings</h2>',
            rendered_html)
   
        dummy = create_event()

        # with events
        rendered_html = self.instance.render_plugin()
        self.assertIn('<h2 class="latest_title">Funky Happenings</h2>',
            rendered_html)

