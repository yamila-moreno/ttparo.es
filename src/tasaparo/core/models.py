# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Max
import hashlib
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

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
            results = results.filter(cycle=latest_cycle['cycle__max'])

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
            rq = RateQuery.objects.get(query_hash=query_hash)
            rq.save()
            return rq
        except RateQuery.DoesNotExist:
            return None

    def latest_queries(self):
        latest_cycle = Microdata.objects.all().aggregate(Max('cycle'))['cycle__max']
        return RateQuery.objects.filter(rate__isnull=False).\
            exclude(age__isnull=True,sex__isnull=True,education__isnull=True,province__isnull=True,cycle=latest_cycle).\
            order_by('-date')[:4]

    def get_rates(self, age=None, cycle=None, education=None, province=None, sex=None):
        results = RateQuery.objects.all()
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
            results = results.filter(cycle=latest_cycle['cycle__max'])

        return results

class RateQuery(models.Model):
    query_hash = models.CharField(max_length=100, db_index=True)
    rate = models.IntegerField(null=True, default=None)
    date = models.DateTimeField(auto_now=True)

    age = models.ForeignKey(Age, null=True)
    cycle = models.IntegerField(null=True)
    education = models.ForeignKey(Education, null=True)
    province = models.ForeignKey(Province, null=True)
    sex = models.ForeignKey(Sex, null=True)

    objects = RateQueryManager()

    def __unicode__(self):
        return u'%(age)s %(cycle)s %(education)s %(province)s %(sex)s: %(rate)s' % \
            {'age':self.age, 'cycle':self.cycle, 'education':self.education, 'province':self.province, 'sex':self.sex, 'rate':self.rate}

    class Meta:
        ordering = ['date']
        unique_together = ['age','cycle','education','province','sex']

    @models.permalink
    def get_sharing_url(self):
        return ('api:profile-rate-by-hash', (), {'query_hash': self.query_hash})

    def to_json_dict(self):
        json_dict = {
            'age': self.age and self.age.name or 'edad indiferente',
            'sex': self.sex and self.sex.name or 'género indiferente',
            'province': self.province and self.province.name or 'provincia indiferente',
            'education': self.education and self.education.name or 'formación indiferente',
            'rate':self.rate,
            'level':self.compare_to_general[0],
            'levelText':self.compare_to_general[1]
        }
        return json_dict

    @property
    def compare_to_general(self):
        general_hash = generate_hash()
        general_qr = RateQuery.objects.get_rate(query_hash=general_hash)
        general_rate = general_qr.rate
        percent = general_rate * 20 / 100
        if self.rate > (general_rate + percent):
            return '1', 'nivel alto'
        elif self.rate < (general_rate - percent):
            return '3', 'nivel bajo'
        else:
            return '2', 'nivel medio'
