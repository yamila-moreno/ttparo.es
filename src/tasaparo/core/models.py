from django.db import models

# Create your models here.

class Age(models.Model):
    name = models.CharField(max_length=100)
    ine_id = models.IntegerField()

    def __unicode__(self):
        return self.name

class Sex(models.Model):
    name = models.CharField(max_length=100)
    ine_id = models.IntegerField()

    def __unicode__(self):
            return self.name

class Education(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    ine_id = models.IntegerField()

    def __unicode__(self):
        return self.name

class Aoi(models.Model):
    name = models.CharField(max_length=100)

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
