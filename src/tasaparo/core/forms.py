# -*- coding: utf-8 -*-

from django import forms
from tasaparo.core import models


class FilterForm(forms.Form):
    age = models.IntegerField(required=False)
    cicle = models.IntegerField(required=False)
    education = models.IntegerField(required=False)
    province = models.IntegerField(required=False)
    sex = models.IntegerField(required=False)
