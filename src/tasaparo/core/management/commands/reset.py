# -*- coding: utf-8 -*-

from tasaparo.core import models
from django.core.management.base import BaseCommand, CommandError
from django.core import management
from optparse import make_option
import random, sys, subprocess, uuid
import io
from django.db.models import Q, Count

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        #make_option('--no-initial-data', action='store_true', dest='no_initial_data', default=False,
                    #help="Syncronizes models without loading any data"),
        make_option('--csv', dest='csv', default=None,
                    help="CSV input file"),
    )
    help = 'Used to load a CSV file.'

    def handle(self, *args, **options):
        csv = options.get('csv', None)

        try:
            subprocess.Popen(['dropdb', 'tasaparo']).communicate()
            subprocess.Popen(['createdb', 'tasaparo']).communicate()
        except:
            pass

        management.call_command('syncdb', interactive=False)

        #The expected format is:
        #ciclo	edad	sexo	nforma	prov	aoi	factorel
        if csv:
            with io.open(csv, 'r') as f:
                for line in f:
                    list_data = line.split('\t')
                    # age
                    age = models.Age.objects.get(name=list_data[1])
                    # sex
                    sex = models.Sex.objects.get(name='Varón')
                    if list_data[2] == 'M':
                        sex = models.Sex.objects.get(name='Mujer')
                    # education
                    education = models.Education.objects.get(name='Nada Completado')
                    if list_data[3] == 'p':
                        education = models.Education.objects.get(name='ESO / EGB')
                    elif list_data[3] == 'fp':
                        education = models.Education.objects.get(name='FP (Grado Medio o Grado Superior)')
                    elif list_data[3] == 'b':
                        education = models.Education.objects.get(name='Bachiller / BUP')
                    elif list_data[3] == 'u':
                        education = models.Education.objects.get(name='Universidad (Licenciatura o Diplomatura)')
                    # province
                    province = models.Province.objects.get(name=list_data[4])
                    #aoi
                    aoi = models.Aoi.objects.get(name='Ocupados')
                    if list_data[5] == 'p':
                        aoi = models.Aoi.objects.get(name='Parados')

                    models.Microdata.objects.create(
                        cycle = list_data[0],
                        age = age,
                        sex = sex,
                        education = education,
                        province = province,
                        aoi = aoi,
                        factorel = list_data[6],
                    )
