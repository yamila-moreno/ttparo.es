# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Max
import hashlib
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from django.core.cache import cache

# Create your models here.

class Age(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    ine_id = models.IntegerField(db_index=True)

    def __unicode__(self):
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=100)
    ine_id = models.IntegerField(db_index=True)

    def __unicode__(self):
            return self.name


class Education(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    inner_id = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    ine_id = models.IntegerField(db_index=True)

    def __unicode__(self):
        return self.name

class Aoi(models.Model):
    name = models.CharField(max_length=100)
    inner_id = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.name

class Microdata(models.Model):
    cycle = models.IntegerField()
    age = models.ForeignKey(Age)
    sex = models.ForeignKey(Sex)
    education = models.ForeignKey(Education)
    province = models.ForeignKey(Province)
    aoi = models.ForeignKey(Aoi)
    factorel = models.FloatField()

    def __unicode__(self):
        return u'%(id)s' % {'id':self.id}

    class Meta:
        unique_together = ['age','cycle','education','province','sex', 'aoi']

def generate_hash(age=None, cycle=None, education=None, province=None, sex=None):
    data_normalized = {}
    data_normalized['age'] = age and str(age) or ''
    data_normalized['cycle'] = cycle and str(cycle) or str(Microdata.objects.all().aggregate(Max('cycle'))['cycle__max'])
    data_normalized['education'] = education and str(education) or ''
    data_normalized['province'] = province and str(province) or ''
    data_normalized['sex'] = sex and str(sex) or ''

    return hashlib.md5(str(data_normalized)).hexdigest()

class RateQueryManager(models.Manager):

    def get_rate(self, query_hash=None, age=None, cycle=None, education=None, province=None, sex=None):
        if not query_hash:
            query_hash = generate_hash(age=age,cycle=cycle,education=education,province=province,sex=sex)

        try:
            return RateQuery.objects.get(query_hash=query_hash)

        except RateQuery.DoesNotExist:
            return None

    def get_general_rate(self):
        rate = self.get_rate()
        return rate

    def latest_queries(self):
        latest_cycle = Microdata.objects.all().aggregate(Max('cycle'))['cycle__max']
        # TODO. ¿por qué excluimos las RQ que tienen algún criterio a null? ¿qué más da?
        latest_queries = RateQuery.objects.filter(rate__isnull=False)\
            .exclude(age__isnull=True,sex__isnull=True,education__isnull=True,province__isnull=True,cycle=latest_cycle)\
            .order_by('-date')[:4]
        return latest_queries

    def compare_rates_by_sex(self, age=None, cycle=None, education=None, province=None, sex=None, compared_by=None):
        latest_cycle = RateQuery.objects.all().aggregate(Max('cycle'))

        rq = RateQuery.objects.filter(
            cycle=latest_cycle['cycle__max'],
            age__pk=age or None,
            education__pk=education or None,
            province__pk=province or None)\
            .exclude(sex__isnull=True)\
            .order_by('-sex')
        return rq

    def compare_rates_by_age(self, age=None, cycle=None, education=None, province=None, sex=None, compared_by=None):
        latest_cycle = RateQuery.objects.all().aggregate(Max('cycle'))

        rq = RateQuery.objects.filter(
            cycle=latest_cycle['cycle__max'],
            sex__pk=sex or None,
            education__pk=education or None,
            province__pk=province or None)\
            .exclude(age__isnull=True)\
            .order_by('-age')
        return rq

    def compare_rates_by_education(self, age=None, cycle=None, education=None, province=None, sex=None, compared_by=None):
        latest_cycle = RateQuery.objects.all().aggregate(Max('cycle'))

        rq = RateQuery.objects.filter(
            cycle=latest_cycle['cycle__max'],
            sex__pk=sex or None,
            age__pk=age or None,
            province__pk=province or None)\
            .exclude(education__isnull=True)\
            .order_by('-education')
        return rq

    def get_profile_rates(self, age=None, cycle=None, education=None, province=None, sex=None):
        rq = RateQuery.objects.filter(
            age__pk = age or None,
            education__pk = education or None,
            province__pk = province or None,
            sex__pk = sex or None).order_by('cycle')
        return rq

    def get_province_rates(self, age=None, cycle=None, education=None, province=None, sex=None):
        latest_cycle = RateQuery.objects.all().aggregate(Max('cycle'))

        rq = RateQuery.objects.filter(
            cycle=latest_cycle['cycle__max'],
            age__pk=age or None,
            education__pk=education or None,
            sex__pk=sex or None)

        rq = rq.select_related('age', 'sex', 'province', 'education')
        rq = rq.exclude(province__isnull=True)
        return rq

class RateQuery(models.Model):
    query_hash = models.CharField(max_length=100, db_index=True)
    rate = models.FloatField(null=True, default=None)
    date = models.DateTimeField(auto_now=True)

    age = models.ForeignKey(Age, null=True)
    cycle = models.IntegerField(null=True)
    education = models.ForeignKey(Education, null=True)
    province = models.ForeignKey(Province, null=True)
    sex = models.ForeignKey(Sex, null=True)
    compared = models.SmallIntegerField()
    objects = RateQueryManager()

    def __unicode__(self):
        return u'%(age)s %(cycle)s %(education)s %(province)s %(sex)s: %(rate)s' % \
            {'age':self.age, 'cycle':self.cycle, 'education':self.education, 'province':self.province, 'sex':self.sex, 'rate':self.rate}

    class Meta:
        ordering = ['date']
        unique_together = ['age','cycle','education','province','sex']

    @models.permalink
    def get_absolute_url(self):
        return ('profile-rate-by-hash', (), {'query_hash': self.query_hash})

    def to_json_dict(self):
        json_dict = {
            'age': self.age and self.age.name or u'edad indiferente',
            'sex': self.sex and self.sex.name or u'género indiferente',
            'province': self.province and self.province.name or u'provincia indiferente',
            'province_id': self.province and self.province.ine_id or None,
            'education': self.education and self.education.name or u'formación indiferente',
            'rate':self.rate,
            'frate':self.frate,
            'level':self.compared,
            'leveltxt':self.compared_text,
            'absolute_url':self.get_absolute_url(),
        }
        return json_dict

    @property
    def frate(self):
        if not self.rate or self.rate == 0.0:
            self.compared = 0
            self.save()
            return ''
        if self.rate > 10:
            return int(round(self.rate))
        return '{0:g}'.format(self.rate)

    @property
    def compared_text(self):
        if self.compared == 0:
            return 'sin datos'
        elif self.compared == 1:
            return '' #'estás por encima de la media'
        elif self.compared == 2:
            return '' # estás en la media
        else: # 3
            return '' # estás por debajo de la media

