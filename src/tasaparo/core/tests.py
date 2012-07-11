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
        self.assertIsInstance(json_parsed['rate_query']['rate'], int)
        self.assertEqual(json_parsed['rate_query']['rate'], 0)

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
        self.assertIsInstance(json_parsed['rate_query']['rate'], int)
        self.assertEqual(json_parsed['rate_query']['rate'], 38)

    def test_national_rate(self):
        url = reverse('api:national-rate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertIsInstance(json_parsed['rate_query']['rate'], int)
        self.assertEqual(json_parsed['rate_query']['rate'], 25)

    def test_latest_queries(self):
        core.RateQuery.objects.create(query_hash='aaa',rate=25)
        core.RateQuery.objects.create(query_hash='bbb',rate=39)

        url = reverse('api:latest-queries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])
        self.assertEqual(len(json_parsed['latest_queries']),2)

    def test_profile_rate_by_hash_call(self):
        core.RateQuery.objects.create(query_hash='test',rate=25)
        url = reverse('api:profile-rate-by-hash',args=['test'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])

    def test_profile_rate_by_hash_data_fail(self):
        url = reverse('api:profile-rate-by-hash',args=['not_found'])
        response = self.client.get(url)
        json_parsed = simplejson.loads(response.content)
        self.assertFalse(json_parsed['success'])

    def test_form_data_call(self):
        url = reverse('api:form-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_parsed = simplejson.loads(response.content)
        self.assertTrue(json_parsed['success'])

    def test_form_data_correct(self):
        url = reverse('api:form-data')
        response = self.client.get(url)
        json_parsed = simplejson.loads(response.content)
        self.assertEqual(len(json_parsed['sexes']),2)
        self.assertEqual(len(json_parsed['ages']),14)
        self.assertEqual(len(json_parsed['educations']),5)
        self.assertEqual(len(json_parsed['provinces']),52)
        self.assertGreater(len(json_parsed['cycles']),28)

