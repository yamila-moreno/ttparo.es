# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from tasaparo.core import models as core
from tasaparo.core.forms import FilterForm

class HomeView(SuperView):
    def get(self, request, query_hash=None):
        template = 'home.html'
        context = {}
        context['form'] = FilterForm()
        if query_hash:
            context['calculated_query'] = core.RateQuery.objects.get_rate(query_hash=query_hash)
            initial = {
                'age':context['calculated_query'].age and context['calculated_query'].age.id or None,
                'education':context['calculated_query'].education and context['calculated_query'].education.id or None,
                'sex':context['calculated_query'].sex and context['calculated_query'].sex.id or None,
                'province':context['calculated_query'].province and context['calculated_query'].province.id or None,
                'cycle':context['calculated_query'].cycle
            }
            context['form'] = FilterForm(initial=initial)
        context['general_rate'] = core.RateQuery.objects.get_rate()
        context['get_profile_rate_url'] = reverse('api:profile-rate')
        context['get_lastest_queries_url'] = reverse('api:latest-queries')
        context['get_compare_rates_url'] = reverse('api:compare-rates')

        return self.render_to_response(template, context)
