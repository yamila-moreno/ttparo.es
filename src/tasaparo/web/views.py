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
        if query_hash:
            context['rate_query'] = core.RateQuery.objects.get_rate(query_hash=query_hash)
        context['form'] = FilterForm()
        context['general_rate'] = core.RateQuery.objects.get_rate()
        context['get_profile_rate_url'] = reverse('api:profile-rate')
        context['get_lastest_queries_url'] = reverse('api:latest-queries')
        return self.render_to_response(template, context)
