from django.core.urlresolvers import reverse, clear_url_caches
from django.dispatch import receiver
from django.template.defaultfilters import date
from django_dynamic_fixture import G
from django.test.utils import override_settings

import cms.api
from cms.test_utils.testcases import CMSTestCase
from django_harness.app_testing import AppTestMixin, cms_app_urls_changed
from django_harness.fast_dispatch import FastDispatchMixin

from .helper import create_event
from ..models import Event


# Do not override settings to change ROOT_URLCONF in this test!
# We need to test that the app is attached to the CMS properly
class AppTests(AppTestMixin, FastDispatchMixin, CMSTestCase):
    def tearDown(self):
        # Clear the Django-CMS URL patterns and the root urlconf, which
        # have URLs from the apphook still attached to them, which will
        # break future tests.
        # No signal was fired because the page was deleted by rolling back
        # a transaction, not with Page.objects.delete()
        cms_app_urls_changed()
                     
    def test_reverse_urls(self):
        home_page = cms.api.create_page('Home', 'base.html', 'en', 
            published=True)
        events_page = cms.api.create_page('Events', 'base.html', 'en', 
            published=True, slug="events", apphook='EventsApp')
        #reverse('djangocms_events:event_list')
        #reverse('djangocms_events:event_detail')
        #reverse('djangocms_events:event_search')
        #reverse('djangocms_events:event_feed')

    def test_reverse_urls_for_named_app(self):
        pass
