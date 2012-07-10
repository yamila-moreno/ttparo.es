# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class HomeView(SuperView):
    def get(self, request):
        template = 'home.html'
        return self.render_to_response(template)

