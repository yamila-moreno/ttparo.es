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

    def calculate_rate(self, data):

        qr_data = {
            'age_id': data['age'] and data['age'].id or None,
            'sex_id': data['sex'] and data['sex'].id or None,
            'education_id': data['education'] and data['education'].id or None,
            'province_id': data['province'] and data['province'].id or None,
            'cycle':data['cycle']
        }
        results = Microdata.objects.all()
        if 'sex_id' in qr_data and qr_data['sex_id'] != None:
            results = results.filter(sex__pk=data['sex_id'])
        if 'age_id' in qr_data and qr_data['age_id'] != None:
            results = results.filter(age__pk=data['age_id'])
        if 'education_id' in qr_data and qr_data['education_id'] != None:
            results = results.filter(education__pk=data['education_id'])
        if 'province_id' in qr_data and qr_data['province_id'] != None:
            results = results.filter(province__pk=data['province_id'])
        if 'cycle' in qr_data:
            results = results.filter(cycle=qr_data['cycle'])
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

def generate_hash(data):
    return hashlib.md5(str(data)).hexdigest()

class RateQueryManager(models.Manager):

    def get_rate(self,data=None, query_hash=None):
        if not query_hash:
            query_hash = generate_hash(data)
        try:
            return RateQuery.objects.rate_query(query_hash, data)
        except:
            return None

    def latest_queries(self):
        return RateQuery.objects.filter(rate__isnull=False).order_by('-date')[:4]

    def get_rates(self,data):
        results = RateQuery.objects.all()
        if 'cycle' in data:
            results = results.filter(cycle=data['cycle'])
        else:
            latest_cycle = results.aggregate(Max('cycle'))
            results = results.filter(cycle=latest_cycle['cycle__max'])
        if 'sex' in data:
            results = results.filter(sex__ine_id=data['sex'])
        if 'age' in data:
            results = results.filter(age__ine_id=data['age'])
        if 'education' in data:
            results = results.filter(education__inner_id=data['education'])
        if 'province' in data:
            results = results.filter(province__ine_id=data['province'])

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
