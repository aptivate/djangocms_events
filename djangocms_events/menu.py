from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _


class EventMenu(CMSAttachMenu):
    name = _('Event Menu')

    def get_nodes(self, request):
        nodes = []

        try:
            nodes.append(
                NavigationNode(
                    _('All Events'),
                    reverse('event_list'),
                    2,
                ))
        except NoReverseMatch:
            pass

        try:
            nodes.append(
                NavigationNode(
                    _('Search Events'),
                    reverse('event_search'),
                    4,
                ))
        except NoReverseMatch:
            pass
        
        return nodes

menu_pool.register_menu(EventMenu)
