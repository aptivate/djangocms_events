from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import EventMenu


class DjangoCmsEventDetailsApp(CMSApp):
    """
    This app displays details of individual events, and serves the RSS feed.
    
    Attach it to the page below which you want all your events to appear. It
    doesn't take over that page, so you can put whatever plugins you want on it,
    but it does take over some URLs below that page (those starting with
    details/ and feed/).
    """
    name = _("Event Details App")
    urls = ["djangocms_events.details_app_urls"]

apphook_pool.register(DjangoCmsEventDetailsApp)

class DjangoCmsEventSearchApp(CMSApp):
    name = _("Event Search App")
    urls = ["djangocms_events.search_app_urls"]

apphook_pool.register(DjangoCmsEventSearchApp)



