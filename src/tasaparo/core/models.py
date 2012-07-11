from django.db import models
from django.db.models import Sum, Max
import hashlib

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
        results = Microdata.objects.all()
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

        total_unemployed = results.filter(aoi__inner_id='p').aggregate(Sum('factorel'))
        if total_unemployed['factorel__sum'] == None:
            return 0

        total = results.aggregate(Sum('factorel'))
        rate = int(round(total_unemployed["factorel__sum"] / total["factorel__sum"] * 100))
        return rate


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

    def get_rate(self,data):
        query_hash = generate_hash(data)
        rate_query = RateQuery.objects.rate_query(query_hash, data)
        if not rate_query.rate:
            rate_query.rate = Microdata.objects.calculate_rate(data)
            rate_query.save()
        return rate_query

    def latest_queries(self):
        return RateQuery.objects.filter(rate__isnull=False).order_by('-date')[:4]

    def rate_query(self, query_hash, data={}):
        try:
            query = RateQuery.objects.get(query_hash=query_hash)
        except:
            age = Age.objects.get(ine_id=data['age']) if 'age' in data else None
            sex = Sex.objects.get(ine_id=data['sex']) if 'sex' in data else None
            province = Province.objects.get(ine_id=data['province']) if 'province' in data else None
            education = Education.objects.get(inner_id=data['education']) if 'education' in data else None
            cycle = 'cycle' in data and data['cycle'] or None

            query = RateQuery(
                query_hash = query_hash,
                cycle = cycle,
                age = age,
                sex = sex,
                province = province,
                education = education
            )
            query.save()
        return query

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

    class Meta:
        ordering = ['date']
