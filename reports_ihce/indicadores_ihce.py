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


class resultados_ihce(osv.Model):
    _name = 'resultados.ihce'

    _columns = {

    }

    def asesorias_emprendimiento(self, cr, uid, ids, fecha, context=None):
        cr.execute("SELECT id FROM asesorias_ihce WHERE name = 'emprendimiento' AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        asesoria_ids = cr.fetchall()

        return len(asesoria_ids)
        
    def cursos_emprendimiento(self, cr, uid, ids, fecha, context=None):
        cr.execute("SELECT id FROM date_courses WHERE services = 'emprendimiento' AND type != 'consultoria' AND state = 'done' AND dependence = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        cursos_ids = cr.fetchall()

        asistentes = 0
        for row in cursos_ids:
            cur = self.pool.get('date.courses').browse(cr, SUPERUSER_ID, row[0], context=context)
            asistentes += cur.number_attendees

        return len(cursos_ids), asistentes


    def servicios(self, cr, uid, ids, fecha, context=None):
        cr.execute("SELECT id FROM register_trademark WHERE servicio = True AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        register_ids = cr.fetchall()
        
        cr.execute("SELECT id FROM bar_code WHERE servicio = True AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        bar_ids = cr.fetchall()
        
        cr.execute("SELECT id FROM fda_ihce WHERE servicio = True AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        fda_ids = cr.fetchall()
        
        cr.execute("SELECT id FROM patent_ihce WHERE servicio = True AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        patente_ids = cr.fetchall()
        

        servicios = len(register_ids) + len(bar_ids) + len(fda_ids) + len(patente_ids)

        return servicios

    def asesorias(self, cr, uid, ids, fecha, context=None):
        cr.execute("SELECT id FROM asesorias_ihce WHERE name IN ('marca','patente','codigo','adecuacion','normatividad','tabla') AND option = 'ihce' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) +"';")
        asesoria_ids = cr.fetchall()

        mujeres = 0
        hombres = 0
        companies = []
        
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

    def consultorias(self, cr, uid, ids, fecha, context=None):
        cr.execute("SELECT id FROM date_courses WHERE type = 'consultoria' AND dependence = 'ihce' AND state = 'done' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        consul_ids = cr.fetchall()
        
        horasCon = 0
        for row in consul_ids:
            cur = self.pool.get('date.courses').browse(cr, SUPERUSER_ID, row[0], context=context)
            horasCon += cur.hours_training

        return len(consul_ids), horasCon

    def cursos(self, cr, uid, ids, fecha, context=None):

        cr.execute("SELECT id FROM date_courses WHERE type != 'consultoria' AND dependence = 'ihce' AND services = 'formacion' AND state = 'done' AND to_char(date, 'YYYY-MM') = '"+ str(fecha) + "';")
        courses_ids = cr.fetchall()

        asistentes = 0
        horas = 0
        mujeres = 0
        hombres = 0
        for row in courses_ids:
            cur = self.pool.get('date.courses').browse(cr, SUPERUSER_ID, row[0], context=context)
            asistentes += cur.number_attendees
            horas += cur.hours_training
            for li in cur.line:
                if li.company_id.sexo == 'F':
                    mujeres = mujeres + 1
                else:
                    if li.company_id.sexo == 'M':
                        hombres = hombres + 1
            
            for lis in cur.list_lines:
                if lis.sexo == 'F':
                    mujeres = mujeres + 1
                else:
                    if lis.sexo == 'M':
                        hombres = hombres + 1
            

        return len(courses_ids), asistentes, horas, mujeres, hombres

class indicador_emprendimiento(osv.Model):
    _name = "indicador.emprendimiento"
    
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.ihce')
        metas_ids = res_obj.search(cr, uid, [('anio_ihce', '=', str(fecha.year)), ('activo','=', True)])
        
        emprendedores_alto_impacto = 0
        cursos = 0
        asistentes = 0
        asesorias = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            emprendedores_alto_impacto = metas.emprendedores_alto_impacto
            cursos = metas.cursos_emprendimiento
            asistentes = metas.asistentes_emprendimiento
            asesorias = metas.asesoria_emprendedores
        
        res = {1: emprendedores_alto_impacto, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res


    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-01', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-02', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-03', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-04', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-05', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-06', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-07', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-08', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-09', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-10', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-11', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ ASESORIAS
        asesorias = res_obj.asesorias_emprendimiento(cr, uid, ids, str(fecha.year) + '-12', context=context)

        #~ CURSOS
        cursos_ol = res_obj.cursos_emprendimiento(cr, uid, ids, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]

        res = {1: 0, 2: asesorias, 3: cursos, 4: asistentes}
        
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

class indicador_servicios_empresariales(osv.Model):
    _name = "indicador.servicios.empresariales"
    
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.ihce')
        metas_ids = res_obj.search(cr, uid, [('anio_ihce', '=', str(fecha.year)), ('activo','=', True)])

        servicios = 0
        asesorias = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            asesorias = metas.asesorias
            servicios = metas.servicios
        
        res = {1: servicios, 2:asesorias, 3:0, 4:0}
        
        return res

    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-01', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-01', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-02', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-02', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-03', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-03', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-04', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-04', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-05', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-05', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-06', context=context)

        #~ ASESORIAS
        asesorias_ol = []
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-06', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-07', context=context)

        #~ ASESORIAS
        asesorias_ol = []
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-07', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-08', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-08', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-09', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-09', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-10', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-10', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-11', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-11', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        #~ SERVICIOS EMPRESARIALES
        servicios = res_obj.servicios(cr, uid, ids, str(fecha.year) + '-12', context=context)

        #~ ASESORIAS
        asesorias_ol = res_obj.asesorias(cr, uid, ids, str(fecha.year) + '-12', context=context)
        asesorias = asesorias_ol[0]
        mujeres = asesorias_ol[1]
        hombres = asesorias_ol[2]
        
        res = {1: servicios, 2:asesorias, 3:mujeres, 4:hombres}
        
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

class indicador_aceleracion(osv.Model):
    _name = "indicador.aceleracion"
    
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.ihce')
        metas_ids = res_obj.search(cr, uid, [('anio_ihce', '=', str(fecha.year)), ('activo','=', True)])

        consultoria_especializada = 0
        cursos_aceleracion = 0
        asistentes_aceleracion = 0
        empresas_certificadas = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            consultoria_especializada = metas.consultoria_especializada
            cursos_aceleracion = metas.cursos_aceleracion
            asistentes_aceleracion = metas.asistentes_aceleracion
            empresas_certificadas = metas.empresas_certificadas
        
        #~ res = {1: servicios, 2:asesorias, 3:0, 4:0}
        
        return res

    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
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
        'meta_anual': fields.integer("Meta Anual"),
        'enero': fields.integer("Ene"),
        'febrero': fields.integer("Feb"),
        'marzo': fields.integer("Mar"),
        'trim1': fields.function(_get_trim1, type='integer', string="Trim1"),
        'abril': fields.integer('Abr'),
        'mayo': fields.integer("May"),
        'junio': fields.integer("Jun"),
        'trim2': fields.function(_get_trim2, type='integer', string="Trim2"),
        'julio': fields.integer("Jul"),
        'agosto': fields.integer("Ago"),
        'septiembre': fields.integer("Sep"),
        'trim3': fields.function(_get_trim3, type='integer', string="Trim3"),
        'octubre': fields.integer("Oct"),
        'noviembre': fields.integer("Nov"),
        'diciembre': fields.integer("Dic"),
        'trim4': fields.function(_get_trim4, type='integer', string="Trim4"),
        'total': fields.function(_get_total, type='integer', string="Total"),
        'porcentaje': fields.function(_get_percent, type='integer', string="%"),
    }
    
    
class indicador_capital_humano(osv.Model):
    _name = "indicador.capital.humano"
    
    
    def _get_meta(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('meta.anual.ihce')
        metas_ids = res_obj.search(cr, uid, [('anio_ihce', '=', str(fecha.year)), ('activo','=', True)])

        consultoria = 0
        horasCon = 0
        cursos = 0
        horas = 0
        asistentes = 0

        if metas_ids:
            metas = res_obj.browse(cr, uid, metas_ids[0])
            consultoria = metas.consultoria_servicios_empresariales
            horasCon = metas.horas
            cursos = metas.cursos_fch
            horas = metas.horas_cursos
            asistentes = metas.asistentes_fch
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:0, 7: 0}

        return res

    def _get_enero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-01', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-01', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_febrero(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-02', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-02', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_marzo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-03', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-03', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res
    
    def _get_trim1(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.enero + row.febrero + row.marzo
        return res

    def _get_abril(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-04', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-04', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_mayo(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-05', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-05', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_junio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-06', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-06', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res
    
    def _get_trim2(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.abril + row.mayo + row.junio
        return res

    def _get_julio(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-07', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-07', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_agosto(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-08', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-08', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_septiembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-09', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-09', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res
    
    def _get_trim3(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = row.julio + row.agosto + row.septiembre
        return res

    def _get_octubre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-10', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-10', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_noviembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-11', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-11', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
        return res

    def _get_diciembre(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fecha = datetime.now()
        res_obj = self.pool.get('resultados.ihce')

        consultoria_ol = res_obj.consultorias(cr, uid, ids, str(fecha.year) + '-12', context=context)
        consultoria = consultoria_ol[0]
        horasCon = consultoria_ol[1]

        cursos_ol = res_obj.cursos(cr, uid, ids, str(fecha.year) + '-12', context=context)
        cursos = cursos_ol[0]
        asistentes = cursos_ol[1]
        horas = cursos_ol[2]
        mujeres = cursos_ol[3]
        hombres = cursos_ol[4]
        
        res = {1: consultoria, 2:horasCon, 3:cursos, 4:horas, 5: asistentes, 6:mujeres, 7: hombres}
        
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
