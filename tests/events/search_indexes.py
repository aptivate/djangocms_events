from __future__ import absolute_import, unicode_literals

from haystack import indexes
from haystack.fields import DateField, CharField, MultiValueField

from .models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    def get_model(self):
        return Event

    text = CharField(document=True, use_template=True)
    title = CharField()
    description = CharField()
    additional_information = CharField()
    categories = MultiValueField()
    location = CharField(model_attr='location', null=True)
    attendees = CharField(model_attr='attendees', null=True)
    # event_url = models.CharField(max_length=255, null=True, blank=True)
    contact_name = CharField(model_attr='contact_name', null=True)
    contact_email = CharField(model_attr='contact_email', null=True)
    contact_phone = CharField(model_attr='contact_phone', null=True)
    start_date = DateField(model_attr='start_date')
    end_date = DateField(model_attr='end_date', indexed=False, null=True)

    def prepare_categories(self, obj):
        return [unicode(obj.event_type)]

    def prepare_activity(self, obj):
        if obj.activity is None:
            return ''
        else:
            return obj.activity.get_title()

