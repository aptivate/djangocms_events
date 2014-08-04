from __future__ import absolute_import, unicode_literals

import sys

from django.utils.importlib import import_module

from appconf import AppConf


class EventsAppConf(AppConf):
    MODEL = None

    class Meta:
        required = ['MODEL']

    def configure_model(self, value):
        module_name, dot, class_name = value.rpartition('.')

        try:
            module = import_module(module_name)
        except ImportError as e:
            raise ImportError, "Failed to import %s: %s" % (module_name, e), sys.exc_info()[2]
            
        return getattr(module, class_name)
