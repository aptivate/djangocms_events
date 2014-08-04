from __future__ import unicode_literals, absolute_import

from datetime import datetime

from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class EventFeed(Feed):
    title = _("Latest Events")
    link = "/events/"
    description = _('The latest events from AuthorAID')

    def items(self):
        return settings.DJANGOCMS_EVENTS_MODEL.objects.order_by('-start_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.

    def item_pubdate(self, item):
        # this needs to be datetime
        return datetime.combine(item.start_date, datetime.min.time())

    def item_categories(self, item):
        return [unicode(item.event_type)]
