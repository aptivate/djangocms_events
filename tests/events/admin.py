from __future__ import unicode_literals, absolute_import

from django.db.models.fields import TextField
from django.contrib.admin import site, ModelAdmin

from . import models


class EventAdmin(ModelAdmin):
    list_display = ('__unicode__', 'location', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    # form = TrainingActivitiesForm  # only link to activities

    fields = ('title', 'description', 'additional_information',
        'location', 'attendees', 'event_url', 'contact_name', 'contact_email',
        'contact_phone', 'start_date', 'end_date',)

    class Media:
        css = {
            'all': ('css/ckeditor_overrides.css',)
        }
        js = ('js/rewire_jquery.js',
              'cms/js/libs/classy.min.js',
              'cms/js/plugins/cms.setup.js',
              'cms/js/plugins/cms.base.js',
              'ckeditor/ckeditor.js',
              'js/cms.ckeditor.js', )

site.register(models.Event, EventAdmin)
