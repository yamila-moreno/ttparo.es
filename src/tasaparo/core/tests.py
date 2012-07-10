"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson


class MicroDataTest(TestCase):

    fixtures = ['initial_data']

    def test_show_microdata(self):
        url = reverse('api:show-microdata')
        post_data = {}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)

        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])

        self.assertIsInstance(json_parsed['tasaparo'], int)


