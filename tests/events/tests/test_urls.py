from django.contrib import admin
from django.conf.urls import url, patterns, include
import urls as base_urls

urlpatterns = patterns('',
    url(r'^events/', include('djangocms_events.urls')),
) + base_urls.urlpatterns
