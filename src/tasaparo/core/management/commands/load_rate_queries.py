# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db.models import Q, Count
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

    def load_ratequeries_sql(self, sql):
        subprocess.Popen(['psql', '-f', sql, '-U', 'tasaparo', 'tasaparo']).communicate()

    def load_rate_queries_from_scratch(self):

        age_map = datamaps.age_map()
        sex_map = datamaps.sex_map()
        education_map = datamaps.education_map()

        rqs = models.RateQuery.objects.all()
        for rq in rqs:
            rq.delete()

        ages = list(models.Age.objects.values_list('ine_id', flat=True))
        ages.append(None)
        sexes = list(models.Sex.objects.values_list('ine_id', flat=True))
        sexes.append(None)
        provinces = list(models.Province.objects.values_list('ine_id', flat=True))
        provinces.append(None)
        educations = list(models.Education.objects.values_list('inner_id', flat=True))
        educations.append(None)
        cycles = models.Microdata.objects.distinct('cycle').values_list('cycle', flat=True)

        combs = itertools.product(ages, sexes, provinces, educations, cycles)

        buffer = []
        counter = 0
        for c in combs:
            #sys.stdout.write("\r{0}".format(counter))
            counter += 1
            if counter%100==0:
                print 'VAMOS ==>', counter

            c_age, c_sex, c_province, c_education, c_cycle = c

            age = c_age and str(c_age) or None
            sex = c_sex and str(c_sex) or None
            province = c_province and str(c_province) or None
            education = c_education and str(c_education) or None
            cycle = str(c_cycle)

            data = {
                'age':age,
                'sex':sex,
                'province':province,
                'education':education,
                'cycle':cycle
            }

            age = age and age_map[age] or None
            sex = sex and sex_map[sex] or None
            education = education and education_map[education] or None
            province = province and self.get_lazy_province(province) or None

            obj = models.RateQuery(
                query_hash = generate_hash(data),
                cycle = c_cycle,
                age = age,
                sex = sex,
                education = education,
                province = province,
            )
            obj.rate = self.calculate_rate({
                'age_id': obj.age and obj.age.id or None,
                'sex_id': obj.sex and obj.sex.id or None,
                'education_id': obj.education and obj.education.id or None,
                'province_id': obj.province and obj.province.id or None,
                'cycle':obj.cycle
            })
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
        models.RateQuery.objects.bulk_create(data)

    def calculate_rate(self, data):
        results = models.Microdata.objects.all()
        if 'sex_id' in data and data['sex_id'] != None:
            results = results.filter(sex__pk=data['sex_id'])
        if 'age_id' in data and data['age_id'] != None:
            results = results.filter(age__pk=data['age_id'])
        if 'education_id' in data and data['education_id'] != None:
            results = results.filter(education__pk=data['education_id'])
        if 'province_id' in data and data['province_id'] != None:
            results = results.filter(province__pk=data['province_id'])
        if 'cycle' in data:
            results = results.filter(cycle=data['cycle'])
        else:
            latest_cycle = results.aggregate(Max('cycle'))
            results = results.filter(cycle=latest_cycle)

        values = list(results.values_list('aoi__inner_id', 'factorel'))
        total_unemployed = sum(map(lambda x: x[1], filter(lambda x: x[0]=='p' , values)))
        total = sum(map(lambda x: x[1], values))
        try:
            return int(round(total_unemployed / total * 100))
        except ZeroDivisionError:
            return 0

