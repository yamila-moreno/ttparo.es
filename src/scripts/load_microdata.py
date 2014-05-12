# -*- coding: utf-8 -*-

import psycopg2
from psycogreen.gevent import gevent_wait_callback
from gevent.pool import Group
from gevent.event import Event
from gevent.queue import JoinableQueue, Empty
import gevent

from psycopg2 import extensions
extensions.set_wait_callback(gevent_wait_callback)


from optparse import make_option

import random, sys, subprocess, uuid
import io

from datamaps import (province_map, aoi_map, education_map,
                       sex_map, age_map)


def create_postgresql_connection():
    connection = psycopg2.connect(database="ttdp", async=False)
    return connection


counter = 0

def worker(queue, event):
    global counter
    connection = create_postgresql_connection()

    _age_map = age_map(connection)
    _sex_map = sex_map(connection)
    _aoi_map = aoi_map(connection)
    _education_map = education_map(connection)
    _province_map = province_map(connection)

    cursor = connection.cursor()
    cursor.execute("BEGIN;")

    while not event.is_set():
        greenlet = gevent.getcurrent()
        try:
            line = queue.get(block=True, timeout=1)
        except Empty:
            continue

        counter +=1
        sys.stdout.write("\r{0}".format(counter))

        try:
            cycle, age, sex, education, province, aoi, factorel = line.split('\t')
        except ValueError:
            continue

        age = _age_map[age]
        sex = _sex_map[sex]
        aoi = _aoi_map[aoi]

        education = _education_map[education]
        province = _province_map[province]

        params = [cycle, age, sex, education, province, aoi, factorel]

        cursor.execute("INSERT INTO core_microdata (cycle,age_id,sex_id,education_id,province_id,aoi_id,factorel)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s);", params)
        queue.task_done()

    cursor.execute("COMMIT;")
    cursor.close()


def handle():
    #The expected format is:
    #ciclo	edad	sexo	nforma	prov	aoi	factorel
    csv_path = sys.argv[1]

    queue = JoinableQueue()
    event = Event()

    greenlets = []

    for i in range(90):
        gv = gevent.spawn(worker, queue, event)
        greenlets.append(gv)

    with io.open(csv_path, 'r') as f:
        for line in f:
            queue.put(line)

    queue.join()
    event.set()
    gevent.joinall(greenlets)


if __name__ == '__main__':
    handle()
