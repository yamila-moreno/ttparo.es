# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db.models import Q, Count
from django.db import transaction

from tasaparo.core import models

import random, sys, subprocess, uuid
import io

from optparse import make_option

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        #make_option('--no-initial-data', action='store_true', dest='no_initial_data', default=False,
                    #help="Syncronizes models without loading any data"),
        make_option('--csv', dest='csv', default=None,
                    help="CSV input file"),
    )
    help = 'Used to load a CSV file.'

    age_cache = {}
    education_cache = {}
    sex_cache = {}
    province_cache = {}
    aoi_cache = {}

    def handle(self, *args, **options):
        try:
            subprocess.Popen(['dropdb', 'tasaparo']).communicate()
            subprocess.Popen(['createdb', 'tasaparo']).communicate()
        except:
            pass

        management.call_command('syncdb', interactive=False)
        self.load_csv(options)

    def get_lazy_age(self, edad):
        if edad not in self.age_cache:
            self.age_cache[edad] = models.Age.objects.get(name=edad)
        return self.age_cache[edad]

    def get_lazy_province(self, province):
        if province not in self.province_cache:
            self.province_cache[province] = models.Province.objects.get(name=province)
        return self.province_cache[province]

    @transaction.commit_on_success
    def load_csv(self, options):
        #The expected format is:
        #ciclo	edad	sexo	nforma	prov	aoi	factorel
        csv = options['csv']

        if not csv:
            return


        sex_m = models.Sex.objects.get(name=u'Mujer')
        sex_h = models.Sex.objects.get(name=u'Varón')

        education_map = {
            "p": models.Education.objects.get(name=u'ESO / EGB'),
            "o": models.Education.objects.get(name=u'Nada Completado'),
            "fp": models.Education.objects.get(name=u'FP (Grado Medio o Grado Superior)'),
            "b": models.Education.objects.get(name=u'Bachiller / BUP'),
            "u": models.Education.objects.get(name=u'Universidad (Licenciatura o Diplomatura)'),
        }

        aoi_map = {
            "o": models.Aoi.objects.get(name='Ocupados'),
            "p": models.Aoi.objects.get(name='Parados'),
        }

        buffer = []

        with io.open(csv, 'r') as f:
            counter = 0
            for line in f:
                try:
                    ciclo, edad, sexo, education, province, aoi, factorel = line.split('\t')
                except ValueError:
                    continue

                sys.stdout.write("\r{0}".format(counter))
                counter += 1

                age = self.get_lazy_age(edad)

                if sexo == 'M':
                    sexo = sex_m
                else:
                    sexo = sex_h

                education = education_map[education]
                province = self.get_lazy_province(province)
                aoi = aoi_map[aoi]

                obj = models.Microdata(
                    cycle = ciclo,
                    age = age,
                    sex = sexo,
                    education = education,
                    province = province,
                    aoi = aoi,
                    factorel = factorel,
                )
                buffer.append(obj)

                if len(buffer) >= 200:
                    self.bulk_insert(buffer)
                    buffer = []

            if len(buffer) > 0:
                self.bulk_insert(buffer)

    def bulk_insert(self, data):
        models.Microdata.objects.bulk_create(data)
