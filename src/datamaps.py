# -*- coding: utf-8 -*-

def age_map(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, ine_id FROM core_age;")
        return dict((str(row[1]), row[0]) for  row in cursor)
    finally:
        cursor.close()

def sex_map(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, ine_id FROM core_sex;")
        return dict((str(row[1]), row[0]) for  row in cursor)
    finally:
        cursor.close()


def education_map(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, inner_id FROM core_education;")
        return dict((str(row[1]), row[0]) for  row in cursor)
    finally:
        cursor.close()


def aoi_map(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, inner_id FROM core_aoi;")
        return dict((str(row[1]), row[0]) for  row in cursor)
    finally:
        cursor.close()


def province_map(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, ine_id FROM core_province;")
        return dict((str(row[1]), row[0]) for  row in cursor)
    finally:
        cursor.close()
