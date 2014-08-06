from __future__ import unicode_literals, absolute_import

from datetime import date

from django.contrib import admin
from django.test import TestCase

from django_dynamic_fixture import G
from django_harness.fast_dispatch import FastDispatchMixin
from django_harness.html_parsing import HtmlParsingMixin
from django_harness.override_settings import override_settings
from django_harness.plugin_testing import PluginTestMixin
from mock import patch

from djangocms_events.models import EventPluginModel
from djangocms_events.cms_plugins import EventDetailListPlugin
from ..models import Event


class EventListPluginTests(FastDispatchMixin, HtmlParsingMixin,
        PluginTestMixin, TestCase):

    plugin_model = EventPluginModel
    plugin_class = EventDetailListPlugin
    plugin_defaults = {'limit': 5}
    maxDiff = None

    def test_event_type_admin_change_view_works(self):
        """
        If the admin change view is broken, then we can't edit the plugin settings.
        """
        from django.contrib.auth.models import User
        staff_user = G(User, is_staff=True, is_superuser=True)
        self.instance.save()

        event = G(Event)

        # Plugins are actually mini-admin-sites, so the CMS calls change_view
        # on them to configure them.
        request = self.get_fake_request('/admin/cms/page/edit-plugin/%d/' %
            self.instance.id, 'get', get_params={}, post_params={},
            request_extras=dict(user=staff_user, csrf_processing_done=True))

        with patch.object(self.plugin, 'get_event_queryset',
                return_value=Event.objects.all()) as patched_method:
            self.plugin.cms_plugin_instance = self.instance
            self.plugin.admin_site = admin.site
            response = self.plugin.change_view(request, str(self.instance.id))

        self.assertFalse(patched_method.called, "get_event_queryset should not have been called")

        response.render()
        # no exception should be thrown
