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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta
import time
#import pdb

class meta_anual_ihce(osv.Model):
    _name = "meta.anual.ihce"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'anio_ihce': fields.char("Año"),
        'activo': fields.boolean("Activo"),
        'emprendedores_alto_impacto': fields.integer("Emprendedores de Alto Impacto"),
        'asesoria_emprendedores': fields.integer("Asesoría a Emprendedores"),
        'cursos_emprendimiento': fields.integer("Cursos, Taller, Diplomados, Platicas etc."),
        'asistentes_emprendimiento': fields.integer("Asistentes"),
        'asesorias': fields.integer("Asesorías"),
        'servicios': fields.integer("Servicios"),
        'consultoria_especializada': fields.integer('Consultoría Especializada'),
        'cursos_aceleracion': fields.integer("Cursos, talleres, diplomados, etc"),
        'asistentes_aceleracion': fields.integer("Asistentes"),
        'empresas_certificadas': fields.integer("Empresas Certificadas"),
        'consultoria_servicios_empresariales': fields.integer("Empresas que recibieron consultoría individual para resolver problemas empresariales especificos"),
        'horas': fields.integer("Horas"),
        'cursos_fch': fields.integer("Cursos, talleres, diplomados, etc"),
        'horas_cursos': fields.integer("Horas"),
        'asistentes_fch': fields.integer("Asistentes"),
    }
    
    _rec_name = 'anio_ihce'
    
    
    _defaults = {
        'anio_ihce': lambda *a: datetime.now().year
    }
    
    def create(self, cr, uid, vals, context=None):
        anio = datetime.now().year
        data_ids = self.search(cr, uid, [])
        data = self.search(cr, uid, [('anio_ihce','=',anio),('activo','=',True)])
        
        if not data:
            #~ Recorremos los registros anteriores y los desactivamos
            for row in data_ids:
                self.write(cr, uid, row, {'activo': False})
            
            vals.update({'activo': True})
            
            self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('emprendedores_alto_impacto'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('asesoria_emprendedores'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('cursos_emprendimiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('asistentes_emprendimiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            
            self.pool.get('indicador.servicios.empresariales').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.servicios.empresariales').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('servicios'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('empresas_certificadas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            
            self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('consultoria_servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('cursos_fch'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas_cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('asistentes_fch'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})

            return super(meta_anual_ihce, self).create(cr, uid, vals, context)
        else:
            raise osv.except_osv(_('Acción Inválida!'), _('Ya existe un registro de metas anuales para este año.'))
    
    def write(self, cr, uid, ids, vals, context=None):

        #pdb.set_trace()

        row = self.browse(cr, uid, ids, context=context)
        
        self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('emprendedores_alto_impacto') or row.emprendedores_alto_impacto})
        self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('asesoria_emprendedores') or row.asesoria_emprendedores})
        self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('cursos_emprendimiento') or row.cursos_emprendimiento})
        self.pool.get('indicador.emprendimiento').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('asistentes_emprendimiento') or row.asistentes_emprendimiento})
        
        
        #self.pool.get('indicador.servicios.empresariales').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('asesorias') or row.asesoria_registro_marca}) Cambio realizado por Julio Lazcano 22 de marzo del 2017
        #self.pool.get('indicador.servicios.empresariales').write(cr, SUPERUSER_ID, 7, {'meta_anual': vals.get('servicios') or row.servicio_registro_marca})
        
        self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('consultoria_especializada') or row.consultoria_especializada})
        self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos_aceleracion') or row.cursos_aceleracion})
        self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes_aceleracion') or row.asistentes_aceleracion})
        self.pool.get('indicador.aceleracion').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('empresas_certificadas') or row.empresas_certificadas})
        
        
        self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('consultoria_servicios_empresariales') or row.consultoria_servicios_empresariales})
        self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('horas') or row.horas})
        self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('cursos_fch') or row.cursos_fch})
        self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas_cursos') or row.horas_cursos})
        self.pool.get('indicador.capital.humano').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('asistentes_fch') or row.asistentes_fch})
        
        return super(meta_anual_ihce,self).write(cr, uid, ids, vals, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['activo'], context=context)
        unlink_ids = []
        for row in data:
            if row['activo'] == False:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Inválida!'), _('No puede eliminar un registro de metas anuales activo!'))

        return super(meta_anual_ihce, self).unlink(cr, uid, unlink_ids, context=context)



class meta_anual_emprered(osv.Model):
    _name = "meta.anual.emprered"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'emprered_meta': fields.many2one('emprereds', 'Emprered'),
        'anio_emprered': fields.char("Año"),
        'activo': fields.boolean("Activo"),
        'servicios_empresariales': fields.integer("Servicios Empresariales"),
        'cursos': fields.integer("Cursos"),
        'asistentes': fields.integer("Asistentes"),
        'horas': fields.integer("Horas"),
        'total_asesorias': fields.integer("Total Asesorías"),
        'consultoria_especializada': fields.integer("Consultoría Especializada"),
        'horas_consultoria': fields.integer("Horas de consultoría"),
        'expediente_financiamiento': fields.integer("Expedientes Financiamiento"),
        'empresas_proyecto_aceleracion': fields.integer("Empresas en proyecto de aceleración empresarial"),
        'eventos': fields.integer("Eventos"),
        'diagnosticos_empresariales': fields.integer("Diagnósticos Empresariales"),
    }
    
    _rec_name = 'emprered_meta'
    
    _defaults = {
        'anio_emprered': lambda *a: datetime.now().year
    }
    
    def create(self, cr, uid, vals, context=None):
        
        anio = datetime.now().year
        data_ids = self.search(cr, uid, [])
        ban = True
        #~ Recorremos los registros anteriores y los desactivamos
        for row in data_ids:
            data = self.browse(cr, uid, row, context=context)
            if vals.get('emprered_meta') == data.emprered_meta.id:
                if vals.get('anio_emprered') != data.anio_emprered:
                    self.write(cr, uid, row, {'activo': False})
                else:
                    ban = False
        
        if ban:
            #~ Se crean resultados para emprereds
            if vals.get('emprered_meta') == 7:
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.apan').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})

            if vals.get('emprered_meta') == 16:
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.atotonilco').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                
                
            if vals.get('emprered_meta') == 8:
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huejutla').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 5:
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.huichapan').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 9:
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.ixmiquilpan').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 17:
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.otomi').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 4:
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.mixquiahuala').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 10:
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.pachuca').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 2:
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tizayuca').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 1:
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tula').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 13:
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.tulancingo').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 11:
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.zacualtipan').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 18:
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.molango').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 19:
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.metztitlan').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            if vals.get('emprered_meta') == 20:
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 1, {'meta_anual': vals.get('servicios_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 2, {'meta_anual': vals.get('cursos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 3, {'meta_anual': vals.get('asistentes'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 4, {'meta_anual': vals.get('horas'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 5, {'meta_anual': vals.get('total_asesorias'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 8, {'meta_anual': vals.get('consultoria_especializada'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 9, {'meta_anual': vals.get('horas_consultoria'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 10, {'meta_anual': vals.get('expediente_financiamiento'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 11, {'meta_anual': vals.get('empresas_proyecto_aceleracion'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 12, {'meta_anual': vals.get('eventos'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
                self.pool.get('indicador.emprered.jacala').write(cr, SUPERUSER_ID, 13, {'meta_anual': vals.get('diagnosticos_empresariales'), 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'noviembre': 0, 'diciembre': 0})
            
            vals.update({'activo': True})
            return super(meta_anual_emprered, self).create(cr, uid, vals, context)
        else:
            return False
            raise osv.except_osv(_('Acción Inválida!'), _('Ya existe un registro de metas anuales del emprered para este año'))
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['activo'], context=context)
        unlink_ids = []
        for row in data:
            if row['activo'] == False:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Inválida!'), _('No puede eliminar un registro de metas anuales activo!'))

        return super(meta_anual_emprered, self).unlink(cr, uid, unlink_ids, context=context)



class meta_anual_ejecutivo(osv.Model):
    _name = "meta.anual.ejecutivo"

    _columns = {
        'anio_ihce': fields.char("Año"),
        'activo': fields.boolean("Activo"),
        'lines': fields.one2many("meta.mensual.ejecutivo", 'meta_id', "Meses"),
    }
    
    _rec_name = 'anio_ihce'
    
    
    _defaults = {
        'anio_ihce': lambda *a: datetime.now().year
    }

    def generar_meses(self, cr, uid, ids, context=None):
        anio = datetime.now().year
        data_ids = self.search(cr, uid, [])
        data = self.search(cr, uid, [('anio_ihce','=',anio),('activo','=',True)])

        if not data:
            for row in data_ids:
                self.write(cr, uid, row, {'activo': False})
                
            self.write(cr, uid, ids, {'activo': True})
            j = 1
            for i in ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']:
                self.pool.get('meta.mensual.ejecutivo').create(cr, uid, {'meta_id': ids[0], 'mes': j, 'name_mes': i})
                j = j + 1

        else:
            self.write(cr, uid, ids, {'activo': False})
            raise osv.except_osv(_('Acción Inválida!'), _('Ya existe un registro de metas anuales ejecutivas para este año.'))

        return True
    


class meta_mensual_ejecutivo(osv.Model):
    _name = "meta.mensual.ejecutivo"

    _columns = {
        'meta_id': fields.many2one("meta.anual.ejecutivo", "Meta Anual"),
        'mes': fields.integer("No."),
        'name_mes': fields.char("Mes"),
        'servicios_empresariales': fields.integer("Servicios Empresariales"),
        'asesoria_empresarial': fields.integer("Asesorías"),
        'mujeres_empresarial': fields.integer("Mujeres Asesorías Empresariales"),
        'hombres_empresarial': fields.integer("Hombres Asesorías Empresariales"),
        'eventos': fields.integer("Eventos"),
        'asistentes': fields.integer("Asistentes"),
        'mujeres_cursos': fields.integer("Mujeres Eventos"),
        'hombres_cursos': fields.integer("Hombres Eventos"),
        'emprereds': fields.integer("Emprered en operación"),
        'asesoria_emprered': fields.integer("Asesorías"),
        'mujeres_emprered': fields.integer("Mujeres Asesorías Emprered"),
        'hombres_emprered': fields.integer("Hombres Asesorías Emprered"),
    }
    
    _rec_name = 'meta_id'

    
