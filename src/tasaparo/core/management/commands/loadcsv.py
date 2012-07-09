# -*- coding: utf-8 -*-

from tasaparo.core import models
from django.core.management.base import BaseCommand, CommandError
from django.core import management
from optparse import make_option
import random, sys, subprocess, uuid

from django.db.models import Q, Count

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        #make_option('--no-initial-data', action='store_true', dest='no_initial_data', default=False,
                    #help="Syncronizes models without loading any data"),
        make_option('--csv', dest='csv', default=None,
                    help="CSV input file"),
    )
    help = 'Used to load a CSV file.'

    def handle(self, *args, **options):
        csv = options.get('csv', None)

        #try:
            #subprocess.Popen(['dropdb', 'gemmed']).communicate()
            #subprocess.Popen(['createdb', 'gemmed']).communicate()
        #except:
            #pass

        if csv:
            f = open(csv, 'r')
            for line in f:
                line = line.replace('"','')
                list_data = line.split('\t')
                age = models.Age.objects.get(name=list_data[3])
                sex = models.Sex.objects.get(name='Varón')
                if list_data[5] == 'M':
                    sex = models.Sex.objects.get(name='Mujer')
                education = models.Education.objects.get(name='Analfabetos')
                province = models.Province.objects.get(name=list_data[2])
                aoi = models.Aoi.objects.get(name='Ocupados')
                if list_data[7] == 'p':
                    aoi = models.Aoi.objects.get(name='Parados')
                models.Microdata.objects.create(
                    cycle = list_data[0],
                    age = age,
                    sex = sex,
                    education = education,
                    province = province,
                    aoi = aoi,
                    factorel = list_data[10],
                )
