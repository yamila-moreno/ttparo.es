# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from tasaparo.core import models as core

class ProfileRateView(SuperView):
    def get(self, request):
        data = request.GET
        context = {}
        rate_query = core.Microdata.objects.get_rate(data)
        context['rate'], context['share'] = rate_query.rate, rate_query.query_hash
        return self.render_json(context, True)

class NationalRateView(SuperView):
    def get(self, request):
        data = {}
        context = {}
        rate_query = core.Microdata.objects.get_rate(data)
        context['rate'], context['share'] = rate_query.rate, rate_query.query_hash
        return self.render_json(context, True)


class LatestQueriesView(SuperView):
    def get(self, request):
        latest_queries = core.RateQuery.objects.latest_queries().values('query_hash','rate')
        context = {'latest_queries':list(latest_queries)}
        return self.render_json(context, True)
