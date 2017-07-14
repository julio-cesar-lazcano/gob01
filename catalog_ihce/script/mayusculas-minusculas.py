#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import psycopg2
import os
import csv
import xmlrpclib

conn = psycopg2.connect("dbname='ihce_demo' user='openerp' password='ihc3d3m0' host='45.55.147.4'")
mark = conn.cursor()


def pg_query(sql,cur):
    cur.execute(sql)
    res = cur.fetchall()
    return res

res = pg_query("""SELECT id, name FROM responsible_area;""", mark)
 
for row in res:
    sql = "UPDATE responsible_area SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM escolaridad;""", mark)
 
for row in res:
    sql = "UPDATE escolaridad SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM caracteristica_poblacional;""", mark)
 
for row in res:
    sql = "UPDATE caracteristica_poblacional SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM tamano_actividad_economica;""", mark)
 
for row in res:
    sql = "UPDATE tamano_actividad_economica SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM sector_actividad_economica;""", mark)
 
for row in res:
    sql = "UPDATE sector_actividad_economica SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM ventas_anuales_actividad_economica;""", mark)
 
for row in res:
    sql = "UPDATE ventas_anuales_actividad_economica SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM emprendedor_actividad_economica;""", mark)
 
for row in res:
    sql = "UPDATE emprendedor_actividad_economica SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM financiamiento;""", mark)
 
for row in res:
    sql = "UPDATE financiamiento SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()

res = pg_query("""SELECT id, name FROM puntos_equilibrio;""", mark)
 
for row in res:
    sql = "UPDATE puntos_equilibrio SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
res = pg_query("""SELECT id, name FROM nivel_deuda;""", mark)
 
for row in res:
    sql = "UPDATE nivel_deuda SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
res = pg_query("""SELECT id, name FROM frecuencia_capacitacion;""", mark)
 
for row in res:
    sql = "UPDATE frecuencia_capacitacion SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
res = pg_query("""SELECT id, name FROM states_mexico;""", mark)
 
for row in res:
    sql = "UPDATE states_mexico SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
res = pg_query("""SELECT id, name FROM town_hidalgo;""", mark)
 
for row in res:
    sql = "UPDATE town_hidalgo SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
res = pg_query("""SELECT id, name FROM colony_hidalgo;""", mark)
 
for row in res:
    sql = "UPDATE colony_hidalgo SET name = '"+str(row[1]).capitalize()+"' WHERE id = '"+str(row[0])+"';"
    print sql
    mark.execute(sql)
    conn.commit()
    
