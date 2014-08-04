"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django_dynamic_fixture import G
from django_harness.fast_dispatch import FastDispatchMixin


class EventsAdminTest(FastDispatchMixin, TestCase):
    def setUp(self):
        super(EventsAdminTest, self).setUp()
        from django.contrib.auth.models import User
        self.user = G(User, email="liam@example.com", is_active=True,
            is_staff=True, is_superuser=True)

    def test_load_admin_interface(self):
        response = self.fast_dispatch('admin:events_event_changelist',
            request_extras=dict(user=self.user))
        # no exception should be thrown

    def test_admin_create_event_page(self):
        response = self.fast_dispatch('admin:events_event_add', 
            method='get', 
            request_extras=dict(user=self.user, csrf_processing_done=True))
        # no exception should be thrown

    """
    def test_create_category_using_admin_interface(self):
        response = self.fast_dispatch('admin:categories_category_add',
            method='post', post_params=dict(name='Hello', _save="Save"),
            request_extras=dict(user=self.user, csrf_processing_done=True))
        # no exception should be thrown
        print response.content
        self.assertEqual(200, response.status_code)
        response.render()
    """
        
