from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import EventMenu


class EventsApp(CMSApp):
    name = _("Events App")  # give your app a name, this is required
    urls = ["djangocms_events.urls"]  # link your app to url configuration(s)
    menus = [EventMenu]

apphook_pool.register(EventsApp)
