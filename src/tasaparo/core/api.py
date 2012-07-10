# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from tasaparo.core import models as core

class ProfileRateView(SuperView):
    def post(self, request):
        data = request.POST

        query_hash = core.Microdata.objects.create_hash(data)
        query = core.Microdata.objects.rate_query(query_hash, data)

        context = {}
        context['tasaparo'] = query.rate
        return self.render_json(context, True)

