from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from cms.models.pluginmodel import CMSPlugin


class Wossname(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(ContentType)

    def __unicode__(self):
        return unicode(self.name)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    additional_information = models.TextField(null=True, blank=True)
    event_type = models.ForeignKey(Wossname, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    attendees = models.CharField(max_length=512, null=True, blank=True)
    event_url = models.URLField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=255, null=True, blank=True)

    # tags = TagAutocompleteField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])
