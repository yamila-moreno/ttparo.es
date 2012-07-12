# -*- coding: utf-8 -*-

from tasaparo.core import models

def age_map():
    ages = models.Age.objects.all()
    age_map = {}
    for a in ages:
        age_map[a.id] = a
    return age_map

def sex_map():
    sexes = models.Sex.objects.all()
    sex_map = {}
    for a in sexes:
        sex_map[a.id] = a
    return sex_map

def education_map():
    educations = models.Education.objects.all()
    education_map = {}
    for a in educations:
        education_map[a.id] = a
    return education_map

def aoi_map():
    aois = models.Aoi.objects.all()
    aoi_map = {}
    for a in aois:
        aoi_map[a.id] = a
    return aoi_map
