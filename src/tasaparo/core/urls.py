# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from tasaparo.core.api import *

urlpatterns = patterns('',
    url(r'^profile/rate/$', ProfileRateView.as_view(), name = 'profile-rate'),
    url(r'^national/rate/$', NationalRateView.as_view(), name = 'national-rate'),
    url(r'^latest/queries/$', LatestQueriesView.as_view(), name = 'latest-queries'),
    url(r'^form/data/$', FormDataView.as_view(), name = 'form-data'),
    url(r'^compare/rates/$', CompareRatesView.as_view(), name = 'compare-rates'),
    url(r'^profile/chart/$', ProfileChartView.as_view(), name = 'profile-chart'),

    url(r'^provinces/rates/$', MapView.as_view(), name = 'map'),

    url(r'^widgethtml/$', WidgetHTMLView.as_view(), name = 'get-widget-html'),
    url(r'^widgetjs/$', WidgetJSView.as_view(), name = 'get-widget-js'),
)
