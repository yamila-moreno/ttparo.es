# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from tasaparo.core import models as core
from tasaparo.core import api
from tasaparo.core.forms import FilterForm

class HomeView(SuperView):
    def get(self, request, query_hash=None):
        template = 'home.html'
        context = {}
        context['form'] = FilterForm()
        if query_hash:
            context['calculated_query'] = core.RateQuery.objects.get_rate(query_hash=query_hash)
            if not context['calculated_query']:
                return HttpResponseRedirect(reverse('home'))
            initial = {
                'age':context['calculated_query'].age and context['calculated_query'].age.id or None,
                'education':context['calculated_query'].education and context['calculated_query'].education.id or None,
                'sex':context['calculated_query'].sex and context['calculated_query'].sex.id or None,
                'province':context['calculated_query'].province and context['calculated_query'].province.id or None,
                'cycle':context['calculated_query'].cycle
            }
            context['form'] = FilterForm(initial=initial)

        context['query_hash'] = query_hash
        context['general_rate'] = core.RateQuery.objects.get_general_rate()
        context['get_profile_rate_url'] = reverse('api:profile-rate')
        context['EPA_URL'] = settings.EPA_URL
        context['EPA_DATE'] = settings.EPA_DATE

        latest_queries = core.RateQuery.objects.latest_queries()
        list_json_dict = []
        for l in latest_queries:
            list_json_dict.append(l.to_json_dict())

        context['latest_queries'] = list_json_dict

        return self.render_to_response(template, context)

class MapView(SuperView):
    def get(self, request, query_hash=None):
        template = 'map.html'
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

        context['query_hash'] = query_hash
        context['get_province_rates_url'] = reverse('api:map')

        return self.render_to_response(template, context)

class CompareView(SuperView):
    def get(self, request, query_hash):
        template = 'compare.html'

        context = {}
        context['form'] = FilterForm()
        context['calculated_query'] = core.RateQuery.objects.get_rate(query_hash=query_hash)

        initial = {
            'age':context['calculated_query'].age and context['calculated_query'].age.id or None,
            'education':context['calculated_query'].education and context['calculated_query'].education.id or None,
            'sex':context['calculated_query'].sex and context['calculated_query'].sex.id or None,
            'province':context['calculated_query'].province and context['calculated_query'].province.id or None,
            'cycle':context['calculated_query'].cycle
        }
        context['form'] = FilterForm(initial=initial)
        context['query_hash'] = query_hash

        context['get_compare_sex_url'] = reverse('api:compare-rates', args=['sex'])
        context['get_compare_age_url'] = reverse('api:compare-rates', args=['age'])
        context['get_compare_education_url'] = reverse('api:compare-rates', args=['education'])

        return self.render_to_response(template, context)

class ProfileView(SuperView):
    def get(self, request, query_hash=None):
        template = 'profile.html'
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

        context['query_hash'] = query_hash
        context['get_profile_chart_url'] = reverse('api:profile-chart')

        return self.render_to_response(template, context)


class AboutView(SuperView):
    template = 'about.html'
    menu = ['about']

    def get(self, request):
        context = {}
        return self.render_to_response(self.template, context)

class WidgetView(SuperView):
    template = 'widget.html'
    menu = ['widget']

    def get(self, request):
        context = {}
        context['form'] = FilterForm()
        context['get_widget_html'] = reverse('api:get-widget-html')
        return self.render_to_response(self.template, context)

class MoreInfoView(SuperView):
    template = 'moreinfo.html'
    menu = ['moreinfo']

    def get(self, request):
        context = {}
        context['form'] = FilterForm()
        context['get_widget_html'] = reverse('api:get-widget-html')
        return self.render_to_response(self.template, context)
