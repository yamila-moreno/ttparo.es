from django.db import models

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

class Microdata(models.Model):
    cycle = models.IntegerField()
    age = models.ForeignKey(Age)
    sex = models.ForeignKey(Sex)
    education = models.ForeignKey(Education)
    province = models.ForeignKey(Province)
    aoi = models.ForeignKey(Aoi)
    factorel = models.FloatField()

    def __unicode__(self):
        return u'%(id)s %(rate)s' % {'id':self.id, 'rate':self.rate()}

    def rate(self):
        return 15
