# -*- coding: utf-8 -*-

from django.views.generic import View

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.cache import cache_page

from superview.views import SuperView
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

        rate_query = core.RateQuery.objects.get_rate(**form.cleaned_data)
        if rate_query:
            context = {'rate_query': rate_query.to_json_dict()}
            return self.render_json(context, True)

        return self.render_json({},False)

class LatestQueriesView(SuperView):
    def get(self, request):
        latest_queries = core.RateQuery.objects.latest_queries()
        list_json_dict = []
        for l in latest_queries:
            list_json_dict.append(l.to_json_dict())
        context = {'latest_queries':list_json_dict}
        return self.render_json(context, True)

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
    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rates = core.RateQuery.objects.compare_rates(**form.cleaned_data)
        if rates:
            list_json_dict = []
            for r in rates:
                list_json_dict.append(r.to_json_dict())

            profile_rates = core.RateQuery.objects.get_profile_rates(**form.cleaned_data)

            if profile_rates:
                list_json_dict_profile = []
                for r in profile_rates:
                    list_json_dict_profile.append(r.to_json_dict())

                context = {'rates': list_json_dict, 'profile_rates': list_json_dict_profile}
                return self.render_json(context, True)

            context = {'rates': list_json_dict}
            return self.render_json(context, True)

        return self.render_json({}, False)


class ProfileChartView(SuperView):
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rates = core.RateQuery.objects.get_profile_rates(**form.cleaned_data)
        if rates:
            list_json_dict = []
            for r in rates:
                list_json_dict.append(r.to_json_dict())

            context = {'rates': list_json_dict}
            return self.render_json(context, True)

        return self.render_json({}, False)


class WidgetJSView(SuperView):

    template = "widget.js"

    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rate_query = core.RateQuery.objects.get_rate(**form.cleaned_data)
        if rate_query:
            context = rate_query.to_json_dict()

        return  self.render_to_response(self.template, context)


class WidgetHTMLView(SuperView):

    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        province = form.cleaned_data['province'] or ''
        sex = form.cleaned_data['sex'] or ''
        age = form.cleaned_data['age'] or ''
        education = form.cleaned_data['education'] or ''

        context = {}
        context['widget_html'] = u"""
                <div id="kaleidos-tasaparo"></div>
                <script src="http://127.0.0.1:8000/api/widgetjs/?province={0}&sex={1}&age={2}&education={3}"></script>
            """.format(province, sex, age, education)

        return self.render_json(context, True)

class MapView(SuperView):
    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        form = FilterForm(request.GET)
        if not form.is_valid():
            return self.render_json({}, False)

        rts = core.RateQuery.objects.get_province_rates(**form.cleaned_data)
        if rts:
            list_json_dict = []
            for r in rts:
                list_json_dict.append(r.to_json_dict())

            context = {'rates': list_json_dict}
            return self.render_json(context, True)

        return self.render_json({}, False)

