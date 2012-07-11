# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from tasaparo.core import models as core

class ProfileRateView(SuperView):
    def get(self, request):
        data = request.GET
        rate_query = core.RateQuery.objects.get_rate(data)
        context = {'rate_query': model_to_dict(rate_query)}
        return self.render_json(context, True)

class NationalRateView(SuperView):
    def get(self, request):
        data = {}
        rate_query = core.RateQuery.objects.get_rate(data)
        context = {'rate_query': model_to_dict(rate_query)}
        return self.render_json(context, True)


class LatestQueriesView(SuperView):
    def get(self, request):
        latest_queries = core.RateQuery.objects.latest_queries().values('query_hash','rate')
        context = {'latest_queries':list(latest_queries)}
        return self.render_json(context, True)

class ProfileRateByHashView(SuperView):
    def get(self, request, query_hash):
        context = {}
        try:
            rate_query = core.RateQuery.objects.get(query_hash=query_hash)
            context = {'rate_query': model_to_dict(rate_query)}
            return self.render_json(context, True)
        except:
            return self.render_json(context,False)

class FormDataView(SuperView):
    def get(self, request):
        context = {}
        context['ages'] = list(core.Age.objects.values('ine_id','name'))
        context['sexes'] = list(core.Sex.objects.values('ine_id','name'))
        context['educations'] = list(core.Education.objects.values('inner_id','name'))
        context['provinces'] = list(core.Province.objects.values('ine_id','name'))
        context['cycles'] = list(core.Microdata.objects.distinct('cycle').values('cycle'))
        return self.render_json(context, True)

