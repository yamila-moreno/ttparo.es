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
    help = 'Used to reset DB, load fixtures and CSV file with microdata.'

    province_cache = {}

    def handle(self, *args, **options):
        try:
            subprocess.Popen(['dropdb', 'tasaparo']).communicate()
            subprocess.Popen(['createdb', 'tasaparo']).communicate()
        except:
            pass

        management.call_command('syncdb', interactive=False)
        self.load_csv(options)

    @transaction.commit_on_success
    def load_csv(self, options):
        #The expected format is:
        #ciclo	edad	sexo	nforma	prov	aoi	factorel
        csv = options['csv']

        if not csv:
            return

        age_map = {
            '1': models.Age.objects.get(ine_id=16),
            '2': models.Age.objects.get(ine_id=20),
            '3': models.Age.objects.get(ine_id=25),
            '4': models.Age.objects.get(ine_id=30),
            '5': models.Age.objects.get(ine_id=35),
            '6': models.Age.objects.get(ine_id=40),
            '7': models.Age.objects.get(ine_id=45),
            '8': models.Age.objects.get(ine_id=50),
            '9': models.Age.objects.get(ine_id=55),
            '10': models.Age.objects.get(ine_id=60),
            '11': models.Age.objects.get(ine_id=65),
            '12': models.Age.objects.get(ine_id=0),
            '13': models.Age.objects.get(ine_id=5),

        }

        sex_map = {
            'H': models.Sex.objects.get(ine_id=1),
            'M': models.Sex.objects.get(ine_id=6)
        }

        education_map = {
            'o': models.Education.objects.get(inner_id='o'),
            'p': models.Education.objects.get(inner_id='p'),
            'fp': models.Education.objects.get(inner_id='fp'),
            'b': models.Education.objects.get(inner_id='b'),
            'u': models.Education.objects.get(inner_id='u'),
        }

        aoi_map = {
            "o": models.Aoi.objects.get(inner_id='o'),
            "p": models.Aoi.objects.get(inner_id='p'),
        }

        buffer = []

        with io.open(csv, 'r') as f:
            counter = 0
            for line in f:
                try:
                    cycle, age, sex, education, province, aoi, factorel = line.split('\t')
                except ValueError:
                    continue

                sys.stdout.write("\r{0}".format(counter))
                counter += 1

                age = age_map[age]
                sex = sex_map[sex]
                education = education_map[education]
                province = self.get_lazy_province(province)
                aoi = aoi_map[aoi]

                obj = models.Microdata(
                    cycle = cycle,
                    age = age,
                    sex = sex,
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


        print 'Finished'

    def get_lazy_province(self, province):
        if province not in self.province_cache:
            self.province_cache[province] = models.Province.objects.get(ine_id=province)
        return self.province_cache[province]

    def bulk_insert(self, data):
        models.Microdata.objects.bulk_create(data)
