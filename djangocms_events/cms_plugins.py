from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import EventPluginModel


class EventFilterMixin(object):
    def get_filtered_events(self, context, instance, placeholder):
        events = settings.DJANGOCMS_EVENTS_MODEL.objects.all()

        from django.db.models import Q
        from datetime import date

        if instance.direction == EventPluginModel.Directions.FUTURE:
            query = Q(end_date=None, start_date__gte=date.today()) \
                | Q(end_date__gte=date.today())
            events = events.order_by('start_date')

        elif instance.direction == EventPluginModel.Directions.PAST:
            query = Q(end_date=None, start_date__lt=date.today()) \
                | Q(end_date__lt=date.today())
            events = events.order_by('-start_date')

        else:
            raise Exception("Unknown direction %s" % instance.direction)

        return events.filter(query)[:instance.limit]


class EventSummaryListPlugin(EventFilterMixin, CMSPluginBase):
    model = EventPluginModel
    name = _("Event Summary List")
    render_template = "events/event_summary_plugin.html"

    def render(self, context, instance, placeholder):
        context["title"] = instance.title
        context["events"] = self.get_filtered_events(context, instance,
            placeholder)
        return context


class EventDetailListPlugin(EventFilterMixin, CMSPluginBase):
    model = EventPluginModel
    name = _("Event Detail List")
    render_template = "events/event_detail_plugin.html"

    def render(self, context, instance, placeholder):
        context["title"] = instance.title
        context["events"] = self.get_filtered_events(context, instance,
            placeholder)
        return context


plugin_pool.register_plugin(EventSummaryListPlugin)
plugin_pool.register_plugin(EventDetailListPlugin)
