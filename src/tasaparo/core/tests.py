"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson

from tasaparo.core import models as core

class MicroDataTest(TestCase):

    fixtures = ['initial_data','microdata_test']
    #fixtures = ['initial_data']

    def test_calculate_zero_rate(self):
        url = reverse('api:profile-rate')
        get_data = {
            'age': '20',
            'sex': '6',
            'province': '52',
            'education': 'fp'
        }
        response = self.client.get(url, get_data)
        self.assertEqual(response.status_code, 200)

        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertIsInstance(json_parsed['rate'], int)
        self.assertEqual(json_parsed['rate'], 0)

    def test_calculate_positive_rate(self):
        url = reverse('api:profile-rate')
        get_data = {
            'sex': '6',
            'province': '52',
        }
        response = self.client.get(url, get_data)
        self.assertEqual(response.status_code, 200)

        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertIsInstance(json_parsed['rate'], int)
        self.assertEqual(json_parsed['rate'], 38)

    def test_national_rate(self):
        url = reverse('api:national-rate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertIsInstance(json_parsed['rate'], int)
        self.assertEqual(json_parsed['rate'], 25)

    def test_latest_queries(self):
        core.RateQuery.objects.create(query_hash='aaa',rate=25)
        core.RateQuery.objects.create(query_hash='bbb',rate=39)

        url = reverse('api:latest-queries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertEqual(len(json_parsed['latest_queries']),2)

    def test_profile_rate_by_hash_fail(self):
#        url = reverse('api:profile-rate-by-hash',args=['4d186321c1a7f0f354b297e8914ab240'])
        url = reverse('api:profile-rate-by-hash',args=['4567'])
        print 'url es', url

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        print response

        json_parsed = simplejson.loads(response.content)
        self.assertFalse(json_parsed['success'])
#        self.assertIsInstance(json_parsed['rate'], int)
#        self.assertEqual(json_parsed['rate'], 38)

