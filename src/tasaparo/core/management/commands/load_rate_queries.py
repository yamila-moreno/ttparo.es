# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db.models import Q, Count, Max
from django.db import transaction
from django.forms.models import model_to_dict

from tasaparo.core import models
from tasaparo.core.models import generate_hash

import random, sys, subprocess, uuid
import io, itertools
import datamaps

from optparse import make_option


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--sql', dest='sql', default=None,
                    help="RateQuery SQL input file"),
    )

    help = 'Used to generate all ratequeries from all data'
    province_cache = {}

    def handle(self, *args, **options):

        sql = options['sql']
        if sql:
            self.load_ratequeries_sql(sql)
        else:
            self.load_rate_queries_from_scratch()

    def load_ratequeries_sql(self, sql):
        subprocess.Popen(['psql', '-f', sql, '-U', 'tasaparo', 'tasaparo']).communicate()

    def load_rate_queries_from_scratch(self):

        age_map = datamaps.age_map()
        sex_map = datamaps.sex_map()
        education_map = datamaps.education_map()

        rqs = models.RateQuery.objects.all()
        for rq in rqs:
            rq.delete()

        # TODO: se hace solo con unos pocos datos, hay que meter todos!!
        #age_ids = list(models.Age.objects.values_list('pk', flat=True))
        age_ids = [7,8,9]
        age_ids.append(None)
        sex_ids = list(models.Sex.objects.values_list('pk', flat=True))
        sex_ids.append(None)
        #province_ids = list(models.Province.objects.values_list('pk', flat=True))
        province_ids = [27, 28, 29]
        province_ids.append(None)
        education_ids = list(models.Education.objects.values_list('pk', flat=True))
        education_ids.append(None)
        #cycles = models.Microdata.objects.order_by('cycle').distinct('cycle').values_list('cycle', flat=True)
        cycles = [100, 125, 158]

        combs = itertools.product(age_ids, sex_ids, province_ids, education_ids, cycles)

        buffer = []
        counter = 0
        for c in combs:
            #sys.stdout.write("\r{0}".format(counter))
            counter += 1
            if counter%200==0:
                print 'VAMOS ==>', counter

            c_age, c_sex, c_province, c_education, c_cycle = c

            age = c_age and age_map[c_age] or None
            sex = c_sex and sex_map[c_sex] or None
            education = c_education and c_education and education_map[c_education] or None
            province = c_province and self.get_lazy_province(c_province) or None

            obj = models.RateQuery(
                query_hash = generate_hash(age=c_age, cycle=c_cycle, education=c_education, province=c_province, sex=c_sex),
                cycle = c_cycle,
                age = age,
                sex = sex,
                education = education,
                province = province,
            )
            obj.rate = self.calculate_rate(
                age and age.id or None,
                c_cycle,
                education and education.id or None,
                province and province.id or None,
                sex and sex.id or None
            )

            buffer.append(obj)

            if len(buffer) >= 200:
                self.bulk_insert(buffer)
                buffer = []

        if len(buffer) > 0:
            self.bulk_insert(buffer)

    def get_lazy_province(self, province):
        if province not in self.province_cache:
            self.province_cache[province] = models.Province.objects.get(id=province)
        return self.province_cache[province]

    def bulk_insert(self, data):
        models.RateQuery.objects.bulk_create(data)

    def calculate_rate(self, age=None, cycle=None, education=None, province=None, sex=None):
        results = models.Microdata.objects.all()
        latest_cycle = results.aggregate(Max('cycle'))

        if sex:
            results = results.filter(sex__pk=sex)
        if age:
            results = results.filter(age__pk=age)
        if education:
            results = results.filter(education__pk=education)
        if province:
            results = results.filter(province__pk=province)
        if cycle:
            results = results.filter(cycle=cycle)
        else:
            results = results.filter(cycle=latest_cycle)

        values = list(results.values_list('aoi__inner_id', 'factorel'))
        total_unemployed = sum(map(lambda x: x[1], filter(lambda x: x[0]=='p' , values)))
        total = sum(map(lambda x: x[1], values))
        try:
            return int(round(total_unemployed / total * 100))
        except ZeroDivisionError:
            return 0

