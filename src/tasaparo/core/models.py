from django.db import models
from django.db.models import Sum

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
        print '*'*20
        print "total ", results.count()
        if 'sex' in data:
            results = results.filter(sex__ine_id=2)
        if 'age' in data:
            results = results.filter(age__ine_id=20)
        if 'education' in data:
            results = results.filter(education__inner_id='fp')
        if 'province' in data:
            results = results.filter(province__ine_id=1)

        print "hay ", len(results)

        results = results.filter(cycle=157)

        print "hay en el ciclo ", len(results)

        count_todos = results.aggregate(Sum('factorel'))

        print count_todos

        return 15

    def create_hash(self, data):
        sex = data['sex']
        age = data['age']
        province = data['province']
        education = data['education']
        return sex+age+province+education

    def rate_query(self, query_hash, data):
        try:
            query = RateQuery.objects.get(query_hash=query_hash)
        except:
            query = RateQuery(
                query_hash = query_hash,
                rate = self.calculate_rate(data)
            )
            query.save()
        return query


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


class RateQuery(models.Model):
    query_hash = models.CharField(max_length=100, db_index=True)
    rate = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
