# -*- coding: utf-8 -*-

from tasaparo.core import models
from django.contrib import admin
import os


admin.site.register(models.Age, admin.ModelAdmin)
admin.site.register(models.Sex, admin.ModelAdmin)
admin.site.register(models.Education, admin.ModelAdmin)
admin.site.register(models.Province, admin.ModelAdmin)
admin.site.register(models.Aoi, admin.ModelAdmin)
admin.site.register(models.Microdata, admin.ModelAdmin)
admin.site.register(models.RateQuery, admin.ModelAdmin)
