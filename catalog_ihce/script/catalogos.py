#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import psycopg2
import os
import csv
import xmlrpclib

conn = psycopg2.connect("dbname='ihce' user='openerp' password='ihc3,.-#$' host='45.55.147.4'")
mark = conn.cursor()



conn8 = psycopg2.connect("dbname='ihce_demo' user='openerp' password='ihc3d3m0' host='45.55.147.4'")
mark8 = conn8.cursor()

def pg_query(sql,cur):
    cur.execute(sql)
    res = cur.fetchall()
    return res

res = pg_query("""SELECT name,town_id FROM colony_hidalgo;""", mark8)
 
for row in res:
    sql = "INSERT INTO colony_hidalgo (name,town_id) VALUES ('"+str(row[0])+"','"+str(row[1])+"');"
    print sql
    mark.execute(sql)
    conn.commit()

