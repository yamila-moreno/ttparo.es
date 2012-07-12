# -*- coding: utf-8 -*-

from django import forms
from tasaparo.core import models


class FilterForm(forms.Form):

    AGE_CHOICES = list(models.Age.objects.all().values_list('id','name'))
    CYCLE_CHOICES = models.Microdata.objects.all().order_by('cycle').distinct('cycle').values_list('cycle', 'cycle')
    EDUCATION_CHOICES = list(models.Education.objects.all().values_list('id','name'))
    PROVINCE_CHOICES = list(models.Province.objects.all().values_list('id','name'))
    SEX_CHOICES = list(models.Sex.objects.all().values_list('id','name'))

    age = forms.TypedChoiceField(required=False, choices=AGE_CHOICES)
    cycle = forms.TypedChoiceField(required=False, choices=CYCLE_CHOICES)
    education = forms.TypedChoiceField(required=False, choices=EDUCATION_CHOICES)
    province = forms.TypedChoiceField(required=False, choices=PROVINCE_CHOICES)
    sex = forms.TypedChoiceField(required=False, choices=SEX_CHOICES)


