# -*- coding: utf-8 -*-
from django.conf import settings

def use_google_analytics(request):
    return {'USE_GOOGLE_ANALYTICS' : settings.USE_GOOGLE_ANALYTICS}
