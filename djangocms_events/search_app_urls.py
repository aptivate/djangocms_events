from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from .forms import EventSearchForm
from .views import EventSearchView

sqs = SearchQuerySet().models(settings.DJANGOCMS_EVENTS_MODEL)

urlpatterns = patterns('',
    url(r'^$', search_view_factory(
            view_class=EventSearchView,
            template='events/search.html',
            searchqueryset=sqs,
            form_class=EventSearchForm),
        name='event_search'),
)
