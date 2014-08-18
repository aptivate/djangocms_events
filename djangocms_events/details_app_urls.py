from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url

from .feeds import EventFeed
from .forms import EventSearchForm
from .views import EventDetailView, EventListView, EventSearchView

urlpatterns = patterns('',
    url(r'^details/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name="event_detail"),

    url(r'^feed/$', EventFeed(), name='event_feed'),
)
