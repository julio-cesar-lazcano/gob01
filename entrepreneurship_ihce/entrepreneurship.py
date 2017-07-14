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
#    Coded by: Karen Morales(karen.morales@grupoaltegra.com)
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
############################################################################  

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from datetime import datetime, date, timedelta
import time

class entrepreneurship_ihce(osv.Model):
    _name = 'entrepreneurship.ihce'

    _columns = {
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'date': fields.date("Fecha"),
        'advice_high': fields.boolean("Asesoría para Acta Constitutiva"),
        'high_sat': fields.boolean("Registro de Acta Constitutiva"),
        'canvas': fields.boolean("Canvas"),
        'lean_start_up': fields.boolean("Lean Start Up"),
        'elevator_pitch': fields.boolean("Elevator pitch"),
        'fuckup': fields.boolean("Fuckup Nights"),
        'incubation_line': fields.boolean("Linea de Incubación"),
        'incubators_list': fields.one2many('incubators.ihce', 'entrepreneurship_id', "Lista de Incubadoras"),
        'emprendimiento': fields.boolean("Emprendimiento"),
        'emprendimiento_text': fields.text("Notas"),
        'formacion_capital_humano': fields.boolean("Formación de Capital Humano"),
        'formacion_capital_humano_text': fields.text("Notas"),
        'desarrollo_empresarial': fields.boolean("Desarrollo Empresarial"),
        'desarrollo_empresarial_text': fields.text("Notas"),
        'laboratorio': fields.boolean("Laboratorio de Diseño"),
        'laboratorio_text': fields.text("Notas"),
        'aceleracion_empresarial': fields.boolean("Aceleración Empresarial"),
        'aceleracion_empresarial_text': fields.text("Notas"),
        'notes': fields.text("Observación General"),
        'servicio': fields.integer("Servicio"),
        'asesoria': fields.integer("Asesoría"),
        'servicio_read': fields.integer("Servicio"),
        'asesoria_read': fields.integer("Asesoría"),
        'crm_id': fields.many2one('crm.project.ihce',"Proyecto crm"),
        'task_id': fields.integer("Tarea crm"),
        'percent': fields.integer("Porcentaje"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'services_de': fields.many2one('services.development.bussines', "Servicio"),
        'services_lab': fields.many2one('services.laboratory', "Servicio"),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
    }
    
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'servicio': 0,
        'asesoria': 0,
        'servicio_read': 0,
        'asesoria_read': 0,
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
    }
    
    _order = "date asc"
    
    _rec_name = 'company_id'
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('asesoria_read'):
            vals.update({'asesoria': vals.get('asesoria_read')})
        if vals.get('servicio_read'):
            vals.update({'servicio': vals.get('servicio_read')})
        
        return super(entrepreneurship_ihce, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('asesoria_read'):
            vals.update({'asesoria': vals.get('asesoria_read')})
        if vals.get('servicio_read'):
            vals.update({'servicio': vals.get('servicio_read')})
            
        return super(entrepreneurship_ihce,self).write(cr, uid, ids, vals, context=context)
    
    def onchange_asesoria_sat(self, cr, uid, ids, valor, asesoria, company_id, percent, opcion, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        anio = fecha_actual.year
        
        if valor == True:
            result['value'].update({'advice_high': valor, 'asesoria': asesoria + 1, 'asesoria_read': asesoria + 1, 'percent': percent + 50})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se le dío Asesoría para alta en el SAT', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        else:
            if asesoria > 0:
                result['value'].update({'advice_high': valor, 'asesoria': asesoria - 1, 'asesoria_read': (asesoria-1), 'percent': percent - 50})

        return result
    
    def onchange_servicio_sat(self, cr, uid, ids, valor, servicio, company_id, percent, opcion, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        anio = fecha_actual.year
        
        if valor == True:
            result['value'].update({'high_sat': valor, 'servicio': servicio + 1, 'servicio_read': servicio + 1, 'percent': percent + 50})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se dio de alta en el SAT', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        else:
            if servicio > 0:
                result['value'].update({'high_sat': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1), 'percent': percent - 50})

        return result
        
    def onchange_canvas(self, cr, uid, ids, valor, servicio, company_id, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if valor == True:
            result['value'].update({'canvas': valor, 'servicio': servicio + 1, 'servicio_read': (servicio+1)})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Modelo de Emprendimiento Canvas', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if servicio > 0:
                result['value'].update({'canvas': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1)})
        
        return result
    
    def onchange_lean_start_up(self, cr, uid, ids, valor, servicio, company_id, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if valor == True:
            result['value'].update({'lean_start_up': valor, 'servicio': servicio + 1, 'servicio_read': (servicio+1)})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Modelo de Emprendimiento Lean Start Up', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if servicio > 0:
                result['value'].update({'lean_start_up': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1)})
        
        return result
    
    def onchange_elevator_pitch(self, cr, uid, ids, valor, servicio, company_id, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if valor == True:
            result['value'].update({'elevator_pitch': valor, 'servicio': servicio + 1, 'servicio_read': (servicio+1)})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Modelo de Emprendimiento Elevator pitch', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if servicio > 0:
                result['value'].update({'elevator_pitch': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1)})
        
        return result
    
    def onchange_fuckup(self, cr, uid, ids, valor, servicio, company_id, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if valor == True:
            result['value'].update({'fuckup': valor, 'servicio': servicio + 1, 'servicio_read': (servicio+1)})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Modelo de Emprendimiento Fuckup', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if servicio > 0:
                result['value'].update({'fuckup': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1)})
        
        return result
    
    def onchange_incubation_line(self, cr, uid, ids, valor, servicio, company_id, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if valor == True:
            result['value'].update({'incubation_line': valor, 'servicio': servicio + 1, 'servicio_read': (servicio+1)})
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Modelo de Emprendimiento: Incubación en linea', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if servicio > 0:
                result['value'].update({'incubation_line': valor, 'servicio': servicio - 1, 'servicio_read': (servicio-1)})
        
        return result
    
    def onchange_emprendimiento(self, cr, uid, ids, valor, empre_text, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if company_id:
            self.pool.get('companies.ihce').write(cr, uid, [company_id], {'emprendimiento': valor, 'emprendimiento_text': empre_text })
        
            #~ Agregamos actividad al historial de la empresa
            if valor:
                result['value'].update({'emprendimiento': valor})
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Vinculada a Emprendimiento', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            else:
                result['value'].update({'emprendimiento': valor})
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se desvinculo de Emprendimiento', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
                
        return result
        
    def onchange_formacion(self, cr, uid, ids, valor, form_text, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if company_id:
            self.pool.get('companies.ihce').write(cr, uid, [company_id], {'formacion_capital_humano': valor, 'formacion_capital_humano_text': form_text})
        
            #~ Agregamos actividad al historial de la empresa
            if valor:
                result['value'].update({'formacion_capital_humano': valor})
                
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Vinculada a Formación de Capital Humano', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            else:
                result['value'].update({'formacion_capital_humano': valor})
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se desvinculo de Formación de Capital Humano', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        return result
    
    def onchange_desarrollo(self, cr, uid, ids, valor, des_text, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if company_id:
            self.pool.get('companies.ihce').write(cr, uid, [company_id], {'desarrollo_empresarial': valor, 'desarrollo_empresarial_text': des_text})
        
            #~ Agregamos actividad al historial de la empresa
            if valor:
                result['value'].update({'desarrollo_empresarial': valor})
                
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Vinculada a Desarrollo Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            else:
                result['value'].update({'desarrollo_empresarial': valor})
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se desvinculo de Desarrollo Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        return result
    
    def onchange_laboratorio(self, cr, uid, ids, valor, des_text, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if company_id:
            self.pool.get('companies.ihce').write(cr, uid, [company_id], {'laboratorio': valor, 'laboratorio_text': des_text})
        
            #~ Agregamos actividad al historial de la empresa
            if valor:
                result['value'].update({'laboratorio': valor})
                
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Vinculada a Laboratorio de Diseño', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            else:
                result['value'].update({'laboratorio': valor})

                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se desvinculo de Laboratorio de Diseño', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        return result

    
    def onchange_aceleracion(self, cr, uid, ids, valor, ace_text, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        if company_id:
            
            self.pool.get('companies.ihce').write(cr, uid, [company_id], {'aceleracion_empresarial': valor, 'aceleracion_empresarial_text': ace_text})
        
            #~ Agregamos actividad al historial de la empresa
            if valor:
                result['value'].update({'aceleracion_empresarial': valor})
                
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Vinculada a Aceleración Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            else:
                result['value'].update({'aceleracion_empresarial': valor})
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Se desvinculo de Aceleración Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        return result
        
    def sinc_vinculation(self, cr, uid, ids, context=None):
        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        data = self.browse(cr, uid, ids[0], context=context)
        row = self.pool.get('companies.ihce').browse(cr, uid, data.company_id.id, context=context)
        
        self.write(cr, uid, ids[0], {'emprendimiento': row.emprendimiento, 'emprendimiento_text': row.emprendimiento_text,  'formacion_capital_humano': row.formacion_capital_humano, 'formacion_capital_humano_text': row.formacion_capital_humano_text, 'desarrollo_empresarial': row.desarrollo_empresarial, 'desarrollo_empresarial_text': row.desarrollo_empresarial_text,  'laboratorio': row.laboratorio, 'aceleracion_empresarial': row.aceleracion_empresarial, 'aceleracion_empresarial_text': row.aceleracion_empresarial_text})
        
        return True
    
    def add_de_lines(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('services.de.lines').create(cr, uid, {'name': row.services_de.id, 'service': True, 'company_id': row.company_id.id})
        return True
    
    def add_lab_lines(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('services.lab.lines').create(cr, uid, {'name': row.services_de.id, 'service': True, 'company_id': row.company_id.id})
        return True
    
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        result = {}
        result['value'] = {}
        
        if user_id:
            row = self.pool.get('res.users').browse(cr, uid, user_id)
            
            result['value'].update({'option': row.option, 'area': row.area.id, 'emprered': row.emprered.id})
        
        return result

    
class incubators_ihce(osv.Model):
    _name = 'incubators.ihce'

    _columns = {
        'entrepreneurship_id': fields.many2one('entrepreneurship.ihce', 'Registro Emprendimiento'),
        'incubators_id': fields.many2one('incubators.catalog', 'Incubadora'),
    }
    
    _rec_name = 'incubators_id'

    def create(self, cr, uid, vals, context=None):
        fecha_actual = datetime.now()
        #~ Al crearse el registro, creamos en automatico el historial de la empresa.
        if vals.get('incubators_id') and vals.get('entrepreneurship_id'):
            row = self.pool.get('entrepreneurship.ihce').browse(cr, uid, vals.get('entrepreneurship_id'), context=context)
            data = self.pool.get('incubators.catalog').browse(cr, uid, vals.get('incubators_id'), context=context)
            
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'Se a incorporado a la incubadora ' + str(data.name), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            self.pool.get('entrepreneurship.ihce').write(cr, uid, [row.id], {'servicio': row.servicio + 1})
            
        return super(incubators_ihce, self).create(cr, uid, vals, context)
    
    
class incubators_catalog(osv.Model):
    _name = 'incubators.catalog'

    _columns = {
        'name': fields.char("Incubadora"),
        'contact': fields.char("Contacto"),
        'mail': fields.char("Correo electrónico"),
        'phone': fields.char("Teléfono"),
    }
    

