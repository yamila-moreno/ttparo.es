# -*- coding: utf-8 -*-

from django import forms
from tasaparo.core import models


class FilterForm(forms.Form):

    AGE_CHOICES = [('',u'Todas las edades')] + list(models.Age.objects.all().values_list('id','name'))
    CYCLE_CHOICES = models.Microdata.objects.all().order_by('cycle').distinct('cycle').values_list('cycle', 'cycle')
    EDUCATION_CHOICES = [('',u'Formación indiferente')] + list(models.Education.objects.all().values_list('id','name'))
    PROVINCE_CHOICES = [('',u'Todas las provincias')] + list(models.Province.objects.all().order_by('name').values_list('id','name'))
    SEX_CHOICES = [('',u'Ambos')] + list(models.Sex.objects.all().values_list('id','name'))

    age = forms.TypedChoiceField(required=False, choices=AGE_CHOICES, widget=forms.Select(attrs={'class':'default'}))
    cycle = forms.TypedChoiceField(required=False, choices=CYCLE_CHOICES, widget=forms.Select(attrs={'class':'default'}))
    education = forms.TypedChoiceField(required=False, choices=EDUCATION_CHOICES, widget=forms.Select(attrs={'class':'default'}))
    province = forms.TypedChoiceField(required=False, choices=PROVINCE_CHOICES, widget=forms.Select(attrs={'class':'default'}))
    sex = forms.TypedChoiceField(required=False, choices=SEX_CHOICES, widget=forms.Select(attrs={'class':'default'}))


