from django_dynamic_fixture import G
from datetime import date

from ..models import Event

i = 0

def create_event(**kwargs):
    global i
    i = i + 1
    # event = G(Event, ignore_fields=['activity', 'training_course'])
    kwargs.setdefault('start_date', date.today())
    kwargs.setdefault('title', 'something %d' % i)
    event = Event.objects.create(**kwargs)
    return event
