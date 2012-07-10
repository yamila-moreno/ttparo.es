from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from tasaparo.core.api import *

urlpatterns = patterns('',
    url(r'^microdata/show/$',
        MicroDataShowView.as_view(),
        name = 'show-microdata',
    ),
)
