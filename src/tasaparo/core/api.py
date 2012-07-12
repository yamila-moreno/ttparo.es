# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from tasaparo.core import models as core
from tasaparo.core.forms import FilterForm

class ProfileRateView(SuperView):
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rate_query = core.RateQuery.objects.get_rate(**form.cleaned_data)
        if rate_query:
            context = {'rate_query': rate_query.to_json_dict()}
            return self.render_json(context, True)

        return self.render_json({},False)

class NationalRateView(SuperView):
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rate_query = core.RateQuery.objects.get_rate(**form.cleaned_date)
        if rate_query:
            context = {'rate_query': rate_query.to_json_dict()}
            return self.render_json(context, True)

        return self.render_json({},False)

class LatestQueriesView(SuperView):
    def get(self, request):
        latest_queries = core.RateQuery.objects.latest_queries().values('query_hash','rate')
        context = {'latest_queries':list(latest_queries)}
        return self.render_json(context, True)

class ProfileRateByHashView(SuperView):
    def get(self, request, query_hash):
        context = {}
        try:
            rate_query = core.RateQuery.objects.get_rate(query_hash=query_hash)
            context = {'rate_query': rate_query.to_json_dict()}
            return self.render_json(context, True)
        except:
            return self.render_json(context,False)

class FormDataView(SuperView):
    def get(self, request):
        context = {}
        context['ages'] = list(core.Age.objects.values('id','name'))
        context['sexes'] = list(core.Sex.objects.values('id','name'))
        context['educations'] = list(core.Education.objects.values('id','name'))
        context['provinces'] = list(core.Province.objects.values('id','name'))
        context['cycles'] = list(core.Microdata.objects.distinct('cycle').values('cycle'))
        return self.render_json(context, True)

class CompareRatesView(SuperView):
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rates = core.RateQuery.objects.get_rates(**form.cleaned_data).values()
        if rates:
            context = {'rates': list(rates)}
            return self.render_json(context, True)

        return self.render_json({}, False)
