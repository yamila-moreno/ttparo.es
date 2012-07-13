# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from tasaparo.core import models as core
from tasaparo.core.forms import FilterForm

class HomeView(SuperView):
    def get(self, request):
        template = 'home.html'

        context = {}
        context['form'] = FilterForm()
        context['general_rate'] = core.RateQuery.objects.get_rate()
        context['get_profile_rate_url'] = reverse('api:profile-rate')
        context['get_lastest_queries_url'] = reverse('api:latest-queries')
        context['get_compare_rates_url'] = reverse('api:compare-rates')



        """
        context = {}
        context['ages'] = list(core.Age.objects.values('ine_id','name'))
        context['sexes'] = list(core.Sex.objects.values('ine_id','name'))
        context['educations'] = list(core.Education.objects.values('inner_id','name'))
        context['provinces'] = list(core.Province.objects.values('ine_id','name'))
        context['cycles'] = list(core.Microdata.objects.distinct('cycle').values('cycle'))
        """
        return self.render_to_response(template, context)

