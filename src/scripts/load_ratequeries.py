# -*- coding: utf-8 -*-

import psycopg2
from psycogreen.gevent import gevent_wait_callback
from gevent.pool import Group
from gevent.event import Event
from gevent.queue import JoinableQueue, Empty
import gevent

from psycopg2 import extensions
extensions.set_wait_callback(gevent_wait_callback)

import random, sys, subprocess, uuid
import io, itertools, hashlib

from optparse import make_option

from datamaps import (province_map, aoi_map, education_map,
                       sex_map, age_map)

def create_postgresql_connection():
    connection = psycopg2.connect(database="tasaparo", async=False)
    return connection


_max_cycle = None

def get_max_cycle(connection):
    global _max_cycle
    if _max_cycle is None:
        cursor = connection.cursor()
        cursor.execute("select max(cycle) from core_microdata")
        _max_cycle = cursor.fetchone()[0]
        cursor.close()

    return _max_cycle


def generate_hash(connection, age=None, cycle=None, education=None, province=None, sex=None):
    data_normalized = {}
    data_normalized['age'] = age and str(age) or ''

    if cycle:
        data_normalized['cycle'] = str(cycle)
    else:
        data_normalized['cycle'] = str(get_max_cycle(connection))

    data_normalized['education'] = education and str(education) or ''
    data_normalized['province'] = province and str(province) or ''
    data_normalized['sex'] = sex and str(sex) or ''
    return hashlib.md5(str(data_normalized)).hexdigest()


def calculate_rate(connection, age=None, cycle=None, education=None, province=None, sex=None):
    latest_cycle = get_max_cycle(connection)

    sql = ("SELECT core_aoi.inner_id, factorel FROM core_microdata "
           "   INNER JOIN core_aoi ON (core_microdata.aoi_id = core_aoi.id) WHERE {0};")

    where_sentences = []
    where_params = []

    if sex:
        where_sentences.append("core_microdata.sex_id = %s")
        where_params.append(sex)

    if age:
        where_sentences.append("core_microdata.age_id = %s")
        where_params.append(age)

    if education:
        where_sentences.append("core_microdata.education_id = %s")
        where_params.append(education)

    if province:
        where_sentences.append("core_microdata.province_id = %s")
        where_params.append(province)

    where_sentences.append("core_microdata.cycle = %s")
    where_params.append(cycle or latest_cycle)

    final_sql = sql.format(" AND ".join(where_sentences))

    cursor = connection.cursor()
    cursor.execute(final_sql, where_params)

    values = [(row[0], row[1]) for row in cursor]

    total_unemployed = sum(map(lambda x: x[1], filter(lambda x: x[0]=='p' , values)))
    total = sum(map(lambda x: x[1], values))
    try:
        return int(round(total_unemployed / total * 100))
    except ZeroDivisionError:
        return 0


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
            c = queue.get(block=True, timeout=1)
        except Empty:
            continue

        counter +=1
        sys.stdout.write("\r{0}".format(counter))

        c_age, c_sex, c_province, c_education, c_cycle = c

        rate = calculate_rate(connection, c_age, c_cycle, c_education, c_province, c_sex)
        hash = generate_hash(connection, age=c_age, cycle=c_cycle,
                education=c_education, province=c_province, sex=c_sex),

        params = [hash, rate, c_cycle, c_age, c_sex, c_education, c_province]
        cursor.execute("INSERT INTO core_ratequery (query_hash, rate, cycle, age_id, sex_id, education_id, province_id, date) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, now())", params)

        queue.task_done()

    cursor.execute("COMMIT;")
    cursor.close()


def handle():
    connection = create_postgresql_connection()

    cursor = connection.cursor()
    cursor.execute("BEGIN;")
    cursor.execute("DELETE FROM core_ratequery;")
    cursor.execute("COMMIT;")
    cursor.close()

    queue = JoinableQueue()
    event = Event()

    age_ids = age_map(connection).values() + [None]
    sex_ids = sex_map(connection).values() + [None]
    education_ids = education_map(connection).values() + [None]
    province_ids = province_map(connection).values() + [None]

    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT cycle FROM core_microdata;");
    cycles = [row[0] for row in cursor]
    cursor.close()

    greenlets = []

    for i in range(50):
        gv = gevent.spawn(worker, queue, event)
        greenlets.append(gv)

    combs = itertools.product(age_ids, sex_ids, province_ids, education_ids, cycles)
    for c in combs:
        queue.put(c)

    queue.join()
    event.set()
    gevent.joinall(greenlets)

if __name__ == '__main__':
    handle()
