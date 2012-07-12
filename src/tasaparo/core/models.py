# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Max
import hashlib
from django.core.urlresolvers import reverse

# Create your models here.

class Age(models.Model):
    name = models.CharField(max_length=100)
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


class MicrodataManager(models.Manager):

    def calculate_rate(self, age=None, cycle=None, education=None, province=None, sex=None):
        results = Microdata.objects.all()
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
            latest_cycle = results.aggregate(Max('cycle'))
            results = results.filter(cycle=latest_cycle)

        values = list(results.values_list('aoi__inner_id', 'factorel'))
        total_unemployed = sum(map(lambda x: x[1], filter(lambda x: x[0]=='p' , values)))
        total = sum(map(lambda x: x[1], values))
        try:
            return int(round(total_unemployed / total * 100))
        except ZeroDivisionError:
            return 0

class Microdata(models.Model):
    cycle = models.IntegerField()
    age = models.ForeignKey(Age)
    sex = models.ForeignKey(Sex)
    education = models.ForeignKey(Education)
    province = models.ForeignKey(Province)
    aoi = models.ForeignKey(Aoi)
    factorel = models.FloatField()
    objects = MicrodataManager()

    def __unicode__(self):
        return u'%(id)s' % {'id':self.id}

def generate_hash(age=None, cycle=None, education=None, province=None, sex=None):
    data_normalized = {}
    data_normalized['age'] = age or ''
    data_normalized['cycle'] = cycle or Microdata.objects.all().aggregate(Max('cycle'))
    data_normalized['education'] = education or ''
    data_normalized['province'] = province or ''
    data_normalized['sex'] = sex or ''
    return hashlib.md5(str(data_normalized)).hexdigest()

class RateQueryManager(models.Manager):

    def get_rate(self, query_hash=None, age=None, cycle=None, education=None, province=None, sex=None):
        if not query_hash:
            query_hash = generate_hash(age,cycle,education,province,sex)

        try:
            return RateQuery.objects.get(query_hash=query_hash)
        except:
            return None

    def latest_queries(self):
        return RateQuery.objects.filter(rate__isnull=False).order_by('-date')[:4]

    def get_rates(self, age=None, cycle=None, education=None, province=None, sex=None):
        results = RateQuery.objects.all()

        if cycle:
            results = results.filter(cycle=cycle)
        else:
            latest_cycle = results.aggregate(Max('cycle'))
            results = results.filter(cycle=latest_cycle['cycle__max'])
        if sex:
            results = results.filter(sex__pk=sex)
        if age:
            results = results.filter(age__pk=age)
        if education:
            results = results.filter(education__pk=education)
        if province:
            results = results.filter(province__pk=province)

        return results

class RateQuery(models.Model):
    query_hash = models.CharField(max_length=100, db_index=True)
    rate = models.IntegerField(null=True, default=None)
    date = models.DateTimeField(auto_now=True)

    cycle = models.IntegerField(null=True)
    age = models.ForeignKey(Age, null=True)
    sex = models.ForeignKey(Sex, null=True)
    education = models.ForeignKey(Education, null=True)
    province = models.ForeignKey(Province, null=True)

    objects = RateQueryManager()

    def __unicode__(self):
        return u'%(cycle)s %(age)s %(sex)s %(education)s %(province)s %(rate)s' % \
            {'cycle':self.cycle, 'age':self.age, 'sex':self.sex, 'education':self.education, 'province':self.province, 'rate':self.rate}

    class Meta:
        ordering = ['date']

    def get_sharing_url(self):
        return reverse('api:profile-rate-by-hash',args=[self.query_hash])
