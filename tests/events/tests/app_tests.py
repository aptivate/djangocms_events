from django.core.urlresolvers import reverse, clear_url_caches
from django.dispatch import receiver
from django.template.defaultfilters import date
from django_dynamic_fixture import G
from django.test.utils import override_settings

import cms.api
from cms.signals import urls_need_reloading
from cms.test_utils.testcases import CMSTestCase
from django_harness.fast_dispatch import FastDispatchMixin

from .helper import create_event
from ..models import Event


# Fix URL cache not being cleared between tests
@receiver(urls_need_reloading)
def cms_app_urls_changed(**kwargs):
    # Clear the Django-CMS URL patterns and the root urlconf, which
    # have URLs from the apphook still attached to them, which will
    # break future tests.
    from cms.views import invalidate_cms_page_cache
    invalidate_cms_page_cache()
    clear_url_caches()
    import cms.urls
    reload(cms.urls)
    import urls
    reload(urls)


# Do not override settings to change ROOT_URLCONF in this test!
# We need to test that the app is attached to the CMS properly
class AppTests(FastDispatchMixin, CMSTestCase):
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
