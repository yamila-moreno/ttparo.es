# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class MicroDataShowView(SuperView):
    def post(self, request):

        context = {}
        context['tasaparo'] = 100
        return self.render_json(context, True)

