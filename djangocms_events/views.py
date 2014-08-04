from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext as _
from haystack.views import SearchView
from cms.models.pagemodel import Page


class EventDetailView(DetailView):
    model = settings.DJANGOCMS_EVENTS_MODEL


class EventListView(ListView):
    model = settings.DJANGOCMS_EVENTS_MODEL
    paginate_by = 10


class EventSearchView(SearchView):
    def __name__(self):
        return "EventSearchView"

    def extra_context(self):
        extra = super(EventSearchView, self).extra_context()
        # make the results available to tests, via the context
        extra['results'] = self.results
        return extra

