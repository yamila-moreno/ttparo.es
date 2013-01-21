# -*- coding: utf-8 -*-
from django.conf import settings

def use_google_analytics(request):
    import pdb; pdb.set_trace()
    return {'USE_GOOGLE_ANALYTICS' : settings.USE_GOOGLE_ANALYTICS}
