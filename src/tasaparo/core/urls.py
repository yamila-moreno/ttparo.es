from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from tasaparo.core.api import *

urlpatterns = patterns('',
    url(r'^profile/rate/$',
        ProfileRateView.as_view(),
        name = 'profile-rate',
    ),
)
