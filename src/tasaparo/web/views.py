# -*- coding: utf-8 -*-

from django.views.generic import View

from superview.views import SuperView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from tasaparo.core import models as core

class HomeView(SuperView):
    def get(self, request):
        template = 'home.html'
        """
        context = {}
        context['ages'] = list(core.Age.objects.values('ine_id','name'))
        context['sexes'] = list(core.Sex.objects.values('ine_id','name'))
        context['educations'] = list(core.Education.objects.values('inner_id','name'))
        context['provinces'] = list(core.Province.objects.values('ine_id','name'))
        context['cycles'] = list(core.Microdata.objects.distinct('cycle').values('cycle'))
        """
        return self.render_to_response(template)

