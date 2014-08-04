from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from cms.models.pluginmodel import CMSPlugin
from extended_choices import Choices

# Force loading of app config
from . import conf


class EventPluginModel(CMSPlugin):
    limit = models.PositiveIntegerField(_('Number of events to show'),
            help_text=_('Limits the number of events that will be displayed'))

    Directions = Choices(
        ('FUTURE',  'future', _('Future')),
        ('PAST',    'past',   _('Past')),
    )

    direction = models.CharField(max_length=6, choices=Directions.CHOICES,
        default=Directions.FUTURE)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return _("%(title)s (%(limit)d %(direction)s events)") % {
            'title': self.title,
            'limit': self.limit,
            'direction': self.direction
        }
