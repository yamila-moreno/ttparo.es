# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db.models import Q, Count
from django.db import transaction

from tasaparo.core import models
import datamaps

import random, sys, subprocess, uuid
import io

from optparse import make_option

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        #make_option('--no-initial-data', action='store_true', dest='no_initial_data', default=False,
                    #help="Syncronizes models without loading any data"),
        make_option('--csv', dest='csv', default=None,
                    help="Microdata CSV input file"),
        make_option('--sql', dest='sql', default=None,
                    help="Microdata SQL input file"),
    )
    help = 'Used to reset DB, load fixtures and CSV file with microdata.'

    province_cache = {}

    def handle(self, *args, **options):
        try:
            subprocess.Popen(['dropdb', '-U', 'tasaparo', 'tasaparo']).communicate()
            subprocess.Popen(['createdb', '-U', 'tasaparo', 'tasaparo']).communicate()
        except:
            pass

        management.call_command('syncdb', interactive=False)

        #TODO: confirmar que no se recibe csv y sql, no son compatibles
        sql = options['sql']
        if sql:
            self.load_microdata_sql(sql)

        csv = options['csv']
        if csv:
            self.load_micdrodata_csv(csv)


    def load_microdata_sql(self, sql):
        subprocess.Popen(['psql', '-f', sql, 'tasaparo']).communicate()

    @transaction.commit_on_success
    def load_micdrodata_csv(self, csv):
        #The expected format is:
        #ciclo	edad	sexo	nforma	prov	aoi	factorel

        age_map = datamaps.age_map()
        sex_map = datamaps.sex_map()
        education_map = datamaps.education_map()
        aoi_map = datamaps.aoi_map()

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

    def get_lazy_province(self, province):
        if province not in self.province_cache:
            self.province_cache[province] = models.Province.objects.get(ine_id=province)
        return self.province_cache[province]

    def bulk_insert(self, data):
        models.Microdata.objects.bulk_create(data)
