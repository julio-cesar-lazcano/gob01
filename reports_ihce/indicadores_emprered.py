#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    CopyLeft 2012 - http://www.grupoaltegra.com
#    You are free to share, copy, distribute, transmit, adapt and use for commercial purpose
#    More information about license: http://www.gnu.org/licenses/agpl.html
#    info Grupo Altegra (openerp@grupoaltegra.com)
#
#############################################################################
#
#    Coded by: Karen Morales (karen.morales@grupoaltegra.com)
#
#############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, date, timedelta
import time
from openerp import SUPERUSER_ID


class resultados_emprered(osv.Model):
    _name = 'resultados.emprered'

    _columns = {

    }

    def servicios(self, cr, uid, ids, emprered, fecha, context=None):
        cr.execute("SELECT id FROM register_trademark WHERE servicio = True AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        register_ids = cr.fetchall()
        
        cr.execute("SELECT id FROM bar_code WHERE servicio = True AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        bar_ids = cr.fetchall()
       
        
        cr.execute("SELECT id FROM servicios_ihce WHERE name = 'manos' AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        manos_ids = cr.fetchall()
        
        cr.execute("SELECT id FROM servicios_ihce WHERE name = 'adecuacion' AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        ade_ids = cr.fetchall()

        servicios = len(register_ids) + len(bar_ids) + len(manos_ids) + len(ade_ids)

        return servicios
        
    def financiamiento(self, cr, uid, ids, emprered, fecha, context=None):
        
        cr.execute("SELECT id FROM servicios_ihce WHERE name = 'financiamiento' AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        fin_ids = cr.fetchall()
        
        servicios = len(fin_ids)

        return servicios

    def cursos(self, cr, uid, ids, emprered, fecha, context=None):

        cr.execute("SELECT id FROM date_courses WHERE type != 'consultoria' AND emprered = '" + str(emprered) + "' AND state = 'done' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        courses_ids = cr.fetchall()

        asistentes = 0
        horas = 0
        for row in courses_ids:
            cur = self.pool.get('date.courses').browse(cr, SUPERUSER_ID, row[0], context=context)
            asistentes += cur.number_attendees
            horas += cur.hours_training

        return len(courses_ids), asistentes, horas

    def asesorias(self, cr, uid, ids, emprered, fecha, context=None):
        cr.execute("SELECT id FROM asesorias_ihce WHERE name IN ('asesoria','marca','patente','codigo','imagen','financiamiento','emprendimiento','shcp','capital','aie','manos','aceleracion','adecuacion') AND emprered = '" + str(emprered) + "' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        asesoria_ids = cr.fetchall()
        companies = []
        mujeres = 0
        hombres = 0
        
        for ro in asesoria_ids:
            ase = self.pool.get('asesorias.ihce').browse(cr, uid, ro[0], context=context)
            company = self.pool.get('companies.ihce').browse(cr, uid, ase.company_id.id)
            
            ban = False
            for li in companies:
                if li == company.id:
                    ban = True
                    break 
            if not ban:
                companies.append(company.id)
                
                if company.sexo == 'F':
                    mujeres = mujeres + 1
                else:
                    if company.sexo == 'M':
                        hombres = hombres + 1

        return len(asesoria_ids), mujeres, hombres

    def consultorias(self, cr, uid, ids, emprered, fecha, context=None):
        cr.execute("SELECT id FROM date_courses WHERE type = 'consultoria' AND emprered = '" + str(emprered) + "' AND state = 'done' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        consul_ids = cr.fetchall()
        
        horasCon = 0
        empresas = 0
        
        for row in consul_ids:
            cur = self.pool.get('date.courses').browse(cr, uid, row[0], context=context)
            empresas += cur.number_attendees
            horasCon += cur.hours_training

        return empresas, horasCon

    def diagnosticos(self, cr, uid, ids, emprered, fecha, context=None):
        cr.execute("SELECT id FROM companies_ihce WHERE company = True AND emprered = '" + str(emprered) + "' AND state = 'done' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        company_ids = cr.fetchall()

        return len(company_ids)


    def eventos(self, cr, uid, ids, emprered, fecha, context=None):
        cr.execute("SELECT id FROM crm_project_ihce WHERE emprered = '" + str(emprered) + "' AND state = 'd-done' AND priority = '1' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        evento_ids = cr.fetchall()

        return len(evento_ids)



class indicador_emprered_apan(osv.Model):
    _name = "indicador.emprered.apan"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',7),('anio_emprered', '=', str(fecha.year)),('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
            #~ fina = metas.financiamiento
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        
        
        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-01', context=context)
        
        
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        
        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 7, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

class indicador_emprered_atotonilco(osv.Model):
    _name = "indicador.emprered.atotonilco"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',16), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 16, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }


class indicador_emprered_huejutla(osv.Model):
    _name = "indicador.emprered.huejutla"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',8), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 8, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

class indicador_emprered_huichapan(osv.Model):
    _name = "indicador.emprered.huichapan"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',5), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 5, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

    
    
class indicador_emprered_ixmiquilpan(osv.Model):
    _name = "indicador.emprered.ixmiquilpan"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',9), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)

        #~ FINACIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 9, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }


class indicador_emprered_otomi(osv.Model):
    _name = "indicador.emprered.otomi"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',17), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)

        #~ FINANCIMAIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO 
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 17, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

class indicador_emprered_mixquiahuala(osv.Model):
    _name = "indicador.emprered.mixquiahuala"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',4), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 4, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }


class indicador_emprered_pachuca(osv.Model):
    _name = "indicador.emprered.pachuca"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',10), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMINETO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMINETO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 10, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

class indicador_emprered_tizayuca(osv.Model):
    _name = "indicador.emprered.tizayuca"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',2), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)

        #~ FINANCIMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 2, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

    
class indicador_emprered_tula(osv.Model):
    _name = "indicador.emprered.tula"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',1), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)

        #~ FINANCIMAIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 1, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }


class indicador_emprered_tulancingo(osv.Model):
    _name = "indicador.emprered.tulancingo"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',13), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 13, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }

    

class indicador_emprered_zacualtipan(osv.Model):
    _name = "indicador.emprered.zacualtipan"
    
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')

        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',11), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIEMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 11, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }



class indicador_emprered_molango(osv.Model):
    _name = "indicador.emprered.molango"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')
        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',18), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 18, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }
    
    
class indicador_emprered_metztitlan(osv.Model):
    _name = "indicador.emprered.metztitlan"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')
        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',19), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 19, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }




class indicador_emprered_jacala(osv.Model):
    _name = "indicador.emprered.jacala"
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.emprered')
        metas_ids = res_obj.search(cr, uid, [('emprered_meta','=',20), ('anio_emprered', '=', str(fecha.year)), ('activo','=', True)])
        servicios = 0
        cursos = 0
        asistentes = 0
        horas = 0
        asesorias = 0
        consul = 0
        horasCon = 0
        eventos = 0
        company = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            servicios = metas.servicios_empresariales
            cursos = metas.cursos
            asistentes = metas.asistentes
            horas = metas.horas
            asesorias = metas.total_asesorias
            consul = metas.consultoria_especializada
            horasCon = metas.horas_consultoria
            eventos = metas.eventos
            company = metas.diagnosticos_empresariales
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:0, 7:0, 8:consul, 9:horasCon, 10:0, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-01', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-02', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-03', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-04', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-05', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-06', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-07', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-08', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-09', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-10', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-11', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.emprered')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)

        #~ FINANCIAMIENTO
        fina = res_obj.financiamiento(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]

        #~ CONSULTORIAS
        consul_ol = res_obj.consultorias(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)
        consul = consul_ol[0]
        horasCon = consul_ol[1]

        #~ DIAGNOSTICOS
        company = res_obj.diagnosticos(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)
        
        #~ eventos
        eventos = res_obj.eventos(cr, uid, ids, 20, str(fecha.year) + '-12', context=context)
        
        res = {1: servicios, 2:cursos, 3:asistentes, 4:horas, 5:asesorias, 6:mujeres, 7:hombres, 8:consul, 9:horasCon, 10:fina, 11:0, 12:eventos, 13:company}
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
        
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_meta, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }



class indicador_total_emprered(osv.Model):
    _name = "indicador.total.emprered"
    
    
    def _get_metas(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] =  apan.meta_anual + atotonilco.meta_anual + huejutla.meta_anual + huichapan.meta_anual + ixmiquilpan.meta_anual +  otomi.meta_anual + mixquiahuala.meta_anual + pachuca.meta_anual + tizayuca.meta_anual + tula.meta_anual + tulancingo.meta_anual + zacualtipan.meta_anual + molango.meta_anual + meztitlan.meta_anual + jacala.meta_anual
        
        return res
    
    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.enero + atotonilco.enero + huejutla.enero + huichapan.enero + ixmiquilpan.enero + otomi.enero + mixquiahuala.enero + pachuca.enero + tizayuca.enero + tula.enero + tulancingo.enero + zacualtipan.enero + molango.enero + meztitlan.enero + jacala.enero
        
        return res
    
    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.febrero + atotonilco.febrero + huejutla.febrero + huichapan.febrero + ixmiquilpan.febrero +  otomi.febrero + mixquiahuala.febrero + pachuca.febrero + tizayuca.febrero + tula.febrero + tulancingo.febrero + zacualtipan.febrero + molango.febrero + meztitlan.febrero + jacala.febrero
        
        return res
    
    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.marzo + atotonilco.marzo + huejutla.marzo + huichapan.marzo + ixmiquilpan.marzo + otomi.marzo + mixquiahuala.marzo + pachuca.marzo + tizayuca.marzo + tula.marzo + tulancingo.marzo + zacualtipan.marzo + molango.marzo + meztitlan.marzo + jacala.marzo
        
        return res

    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res
    
    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.abril + atotonilco.abril + huejutla.abril + huichapan.abril + ixmiquilpan.abril + otomi.abril + mixquiahuala.abril + pachuca.abril + tizayuca.abril + tula.abril + tulancingo.abril + zacualtipan.abril + molango.abril + meztitlan.abril + jacala.abril
        
        return res
    
    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.mayo + atotonilco.mayo + huejutla.mayo + huichapan.mayo + ixmiquilpan.mayo + otomi.mayo + mixquiahuala.mayo + pachuca.mayo + tizayuca.mayo + tula.mayo + tulancingo.mayo + zacualtipan.mayo + molango.mayo + meztitlan.mayo + jacala.mayo
        
        return res
    
    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.junio + atotonilco.junio + huejutla.junio + huichapan.junio + ixmiquilpan.junio + otomi.junio + mixquiahuala.junio + pachuca.junio + tizayuca.junio + tula.junio + tulancingo.junio + zacualtipan.junio + molango.junio + meztitlan.junio  + jacala.junio
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res
    
    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
           
            res[row.id] = apan.julio +  atotonilco.julio + huejutla.julio + huichapan.julio + ixmiquilpan.julio + otomi.julio + mixquiahuala.julio + pachuca.julio + tizayuca.julio + tula.julio + tulancingo.julio + zacualtipan.julio + molango.julio + meztitlan.julio + jacala.julio
        
        return res
    
    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.agosto + atotonilco.agosto + huejutla.agosto + huichapan.agosto + ixmiquilpan.agosto +  otomi.agosto + mixquiahuala.agosto + pachuca.agosto + tizayuca.agosto + tula.agosto + tulancingo.agosto + zacualtipan.agosto + molango.agosto + meztitlan.agosto + jacala.agosto
        
        return res
    
    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.septiembre + atotonilco.septiembre + huejutla.septiembre + huichapan.septiembre + ixmiquilpan.septiembre + otomi.septiembre + mixquiahuala.septiembre + pachuca.septiembre +  tizayuca.septiembre + tula.septiembre + tulancingo.septiembre + zacualtipan.septiembre + molango.septiembre + meztitlan.septiembre + jacala.septiembre
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res
    
    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, uid, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.octubre + atotonilco.octubre + huejutla.octubre + huichapan.octubre + ixmiquilpan.octubre +  otomi.octubre + mixquiahuala.octubre + pachuca.octubre + tizayuca.octubre + tula.octubre + tulancingo.octubre + zacualtipan.octubre + molango.octubre + meztitlan.octubre + jacala.octubre
        
        return res
    
    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.noviembre + atotonilco.noviembre + huejutla.noviembre + huichapan.noviembre + ixmiquilpan.noviembre +  otomi.noviembre + mixquiahuala.noviembre + pachuca.noviembre + tizayuca.noviembre + tula.noviembre + tulancingo.noviembre + zacualtipan.noviembre + molango.noviembre + meztitlan.noviembre + jacala.noviembre
        
        return res
    
    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            apan = self.pool.get('indicador.emprered.apan').browse(cr, SUPERUSER_ID, row.id)
            atotonilco = self.pool.get('indicador.emprered.atotonilco').browse(cr, SUPERUSER_ID, row.id)
            huejutla = self.pool.get('indicador.emprered.huejutla').browse(cr, SUPERUSER_ID, row.id)
            huichapan = self.pool.get('indicador.emprered.huichapan').browse(cr, SUPERUSER_ID, row.id)
            ixmiquilpan = self.pool.get('indicador.emprered.ixmiquilpan').browse(cr, SUPERUSER_ID, row.id)
            otomi = self.pool.get('indicador.emprered.otomi').browse(cr, SUPERUSER_ID, row.id)
            mixquiahuala = self.pool.get('indicador.emprered.mixquiahuala').browse(cr, SUPERUSER_ID, row.id)
            pachuca = self.pool.get('indicador.emprered.pachuca').browse(cr, SUPERUSER_ID, row.id)
            tizayuca = self.pool.get('indicador.emprered.tizayuca').browse(cr, SUPERUSER_ID, row.id)
            tula = self.pool.get('indicador.emprered.tula').browse(cr, SUPERUSER_ID, row.id)
            tulancingo = self.pool.get('indicador.emprered.tulancingo').browse(cr, SUPERUSER_ID, row.id)
            zacualtipan = self.pool.get('indicador.emprered.zacualtipan').browse(cr, SUPERUSER_ID, row.id)
            molango = self.pool.get('indicador.emprered.molango').browse(cr, SUPERUSER_ID, row.id)
            meztitlan = self.pool.get('indicador.emprered.metztitlan').browse(cr, SUPERUSER_ID, row.id)
            jacala = self.pool.get('indicador.emprered.jacala').browse(cr, SUPERUSER_ID, row.id)
            
            res[row.id] = apan.diciembre +  atotonilco.diciembre + huejutla.diciembre + huichapan.diciembre + ixmiquilpan.diciembre +  otomi.diciembre + mixquiahuala.diciembre + pachuca.diciembre + tizayuca.diciembre + tula.diciembre + tulancingo.diciembre + zacualtipan.diciembre + molango.diciembre + meztitlan.diciembre + jacala.diciembre
        
        return res
    
    def _get_trim4(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.octubre + row.noviembre + row.diciembre
        return res
    
    def _get_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.trim1 + row.trim2 + row.trim3 + row.trim4
        return res
        
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.meta_anual != 0:
                res[row.id] = (row.total * 100) / row.meta_anual
            else:
                res[row.id] = 0
                
        return res
    
    _columns = {
        'name':fields.char('Descripción'),
        'meta_anual': fields.function(_get_metas, type='integer', string="Meta Anual"),
        'enero': fields.function(_get_enero, type='integer', string="Ene"),
        'febrero': fields.function(_get_febrero, type='integer', string="Feb"),
        'marzo': fields.function(_get_marzo, type='integer', string="Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.function(_get_abril, type='integer', string="Abr"),
        'mayo': fields.function(_get_mayo, type='integer', string="May"),
        'junio': fields.function(_get_junio, type='integer', string="Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.function(_get_julio, type='integer', string="Jul"),
        'agosto': fields.function(_get_agosto, type='integer', string="Ago"),
        'septiembre': fields.function(_get_septiembre, type='integer', string="Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.function(_get_octubre, type='integer', string="Oct"),
        'noviembre': fields.function(_get_noviembre, type='integer', string="Nov"),
        'diciembre': fields.function(_get_diciembre, type='integer', string="Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }
