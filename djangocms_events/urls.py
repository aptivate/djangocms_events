from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from .feeds import EventFeed
from .forms import EventSearchForm
from .views import EventDetailView, EventListView, EventSearchView

sqs = SearchQuerySet().models(settings.DJANGOCMS_EVENTS_MODEL)

urlpatterns = patterns('',
    url(r'^list/$',
        EventListView.as_view(),
        name="event_list"),

    url(r'^details/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name="event_detail"),

    url(r'^search/$', search_view_factory(
            view_class=EventSearchView,
            template='events/search.html',
            searchqueryset=sqs,
            form_class=EventSearchForm),
        name='event_search'),

    url(r'^feed/$', EventFeed(), name='event_feed'),
)
