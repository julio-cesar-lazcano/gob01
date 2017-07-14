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

class acceleration_ihce(osv.Model):
    _name = 'acceleration.ihce'
    
    #~ Obtenemos el porcentaje de cada empresa y obtenemos el promedio para el porcentaje total del proyecto
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        percent = 0
        for row in self.browse(cr, uid, ids, context=context):
            for ro in row.company_list_ids:
                data = self.pool.get('company.list.acceleration').browse(cr, uid, ro.id, context=context)
                percent += data.percent
            
            if len(row.company_list_ids) > 0:
                percent = percent / len(row.company_list_ids)
            else:
                percent = 0
            res[row.id] = percent
        return res
    
    #~ Se obtiene el número de empresas agregadas al proyetco
    def _get_number_company(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            res[row.id] = len(row.company_list_ids)
        return res
    
    #~ Se obtiene el número de empresas agregadas al proyecto
    def _get_number_asesoria(self, cr, uid, ids, field, arg, context=None):
        res = {}
        con = 0
        lista_ids = ""
        for row in self.browse(cr, uid, ids, context=context):
            for ro in row.courses_ids:
                lista_ids = str(ro.id) + ","
            if lista_ids:
                lista_ids = lista_ids[:-1]
                cr.execute("SELECT courses_id FROM date_courses WHERE id IN ("+str(lista_ids)+") AND state = 'done' GROUP BY courses_id;")
                cours = cr.fetchall()
                for ro in cours:
                    data = self.pool.get('courses.ihce').browse(cr, uid, ro[0], context=context)
                    if data.state_cours == True:
                        con = con +1
            res[row.id] = con
        return res
        
    _columns = {
        'name': fields.char("Proyecto", size=200),
        'description': fields.char("Descripción", size=250),
        'date_ini': fields.date("Fecha inicio"),
        'date_fin': fields.date("Fecha final"),
        'notes': fields.text("Observación general"),
        'state_ace': fields.selection([
            ('draft', 'Nuevo'),
            ('process', 'Proceso'),
            ('out_time', 'Fuera de tiempo'),
            ('done', 'Terminado'),
            ('cancel','Cancelado'),
            ], 'Estado', select=True),
        'percent': fields.function(_get_percent, type='integer', string="Porcentaje de avance"),
        'company_list_ids': fields.one2many('company.list.acceleration', 'acceleration_id', "Beneficiarios"),
        'number_company': fields.function(_get_number_company, type='integer', string="Número de Beneficiarios"),
        'service': fields.integer("Servicios"),
        'asesoria': fields.function(_get_number_asesoria, type='integer', string="Consultorías"),
        'crm_id': fields.many2one('crm.project.ihce',"Proyecto crm"),
        'task_id': fields.integer("Tarea crm"),
        'courses_ids': fields.one2many('date.courses', 'acceleration_id', "Consultorías"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina de atención'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
        'change_user': fields.boolean("Cambiar Usuario"),
    }
    
    _defaults = {
        'state_ace': 'draft',
        'date_ini': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'change_user': False,
    }
    
    _order = "date_ini asc"
    
    def create(self, cr, uid, vals, context=None):
        return super(acceleration_ihce, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        return super(acceleration_ihce,self).write(cr, uid, ids, vals, context=context)
        
    #~ Función para empezar proyecto, permite agregar empresas y crea un proyecto en el crm del usuario
    def empezar_proyecto_ace(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Al aprobarse el registro se crea un proyecto en el crm del usuario.
        valores = {
            'name': row.name.encode('utf-8'),
            'state': 'a-draft',
            'type_crm': 'manual',
        }
        crm_id = self.pool.get('crm.project.ihce').create(cr, uid, valores, context=context)
        self.pool.get('crm.project.ihce').comenzar(cr, uid, [crm_id], context=context)
        
        self.write(cr, uid, ids[0], {'state_ace':'process', 'crm_id':crm_id}, context=context)
        
        return True
    
    #~ Finaliza el proyecto solo si sus empresas agregadas estan certificadas o se quedaron en estado nuevo.
    def finalizar_proyecto_ace(self, cr, uid, ids, context=None):
        rows = self.browse(cr, uid, ids[0], context=context)
        ban = True
        for row in rows.company_list_ids:
            data = self.pool.get('company.list.acceleration').browse(cr, uid, row.id, context=context)
            if data.state != 'done':
                ban = False
                break
        if ban:
            self.write(cr, uid, ids[0], {'state_ace':'done'}, context=context)
        else:
            raise osv.except_osv(_('Acción Invalida!'), _('No puede terminar el proyecto, hay empresas que no han sido certificadas.!'))
        
        return True
        
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        result = {}
        result['value'] = {}
        
        if user_id:
            row = self.pool.get('res.users').browse(cr, uid, user_id)
            
            result['value'].update({'option': row.option, 'area': row.area.id, 'emprered': row.emprered.id})
        
        return result


class company_list_acceleration(osv.Model):
    _name = 'company.list.acceleration'
    
    _columns = {
        'company_id': fields.many2one('companies.ihce', "Beneficiario"),
        'acceleration_id': fields.many2one('acceleration.ihce', 'Proyecto'),
        'percent': fields.integer("Porcentaje"),
        #~ etapas
        'adiagnostic': fields.boolean("Diagnóstico"),
        'date_fin_diag': fields.date("Fecha"),
        'training': fields.boolean("Capacitación"),
        'date_fin_trai': fields.date("Fecha"),
        'implementation': fields.boolean("Implementación"),
        'date_fin_imple': fields.date("Fecha"),
        'cross_audit': fields.boolean("Auditoría cruzada"),
        'date_fin_cros': fields.date("Fecha"),
        'acceptation_audit': fields.boolean("Aceptación Pre-Auditoría"),
        'date_fin_acep': fields.date("Fecha"),
        'audit': fields.boolean("Auditoría"),
        'date_fin_audi': fields.date("Fecha"),
        'certificate': fields.boolean("Certificado"),
        'date_fin_cer': fields.date("Fecha"),
        'state': fields.selection([
            ('process', 'Proceso'),
            ('out_time', 'Fuera de tiempo'),
            ('done', 'Terminado'),
            ], 'Estado'),
        'cron_id': fields.many2one('ir.cron', "Tarea en proceso"),
    }
    
    _rec_name = 'company_id'

    _defaults = {
        'percent': 0,
    }

    #~ Función que checa el tiempo y las etapas de acuerdo al planificador
    def _check_task_ace(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_ejecucion = datetime.now().date()
        
        if row.state != 'done':
            if row.adiagnostic == False and fecha_ejecucion > datetime.strptime(row.date_fin_diag, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.training == False and fecha_ejecucion > datetime.strptime(row.date_fin_trai, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.implementation == False and fecha_ejecucion > datetime.strptime(row.date_fin_imple, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.cross_audit == False and fecha_ejecucion > datetime.strptime(row.date_fin_cros, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.acceptation_audit == False and fecha_ejecucion > datetime.strptime(row.date_fin_acep, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.audit == False and fecha_ejecucion > datetime.strptime(row.date_fin_audi, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            elif row.certificate == False and fecha_ejecucion > datetime.strptime(row.date_fin_cer, "%Y-%m-%d").date():
                self.write(cr, uid, [ids[0]], {'state':'out_time'})
            else:
                self.write(cr, uid, [ids[0]], {'state':'process'})
                
        return True
        
    def create(self, cr, uid, vals, context=None):
        com_id = super(company_list_acceleration, self).create(cr, uid, vals, context)
        row = self.browse(cr, uid, com_id, context=context)
        
        res = {
            'name':'Process : ' + str(com_id),
            'model':'company.list.acceleration',
            'args': repr([[com_id]]), 
            'function':'_check_task_ace',
            'priority':5,
            'interval_number':1,
            'interval_type':'hours',
            'user_id':uid,
            'numbercall':-1,
            'doall':False,
            'active':True
        }
        
        id_cron = self.pool.get('ir.cron').create(cr, uid, res)
        
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, vals.get('acceleration_id'), context=context)
         
        if acele_row.option == 'emprered':
            self.indicadores_servicios(cr, uid, [acele_row.id], True, context=context)
        
        self.write(cr, uid, [com_id], {'state': 'process', 'cron_id': id_cron}, context=context)

    
    #~ Cada vez que se hace un write se crea una tarea nueva
    def write(self, cr, uid, ids, vals, context=None):
        return super(company_list_acceleration,self).write(cr, uid, ids, vals, context=context)
    
    def get_percent(self, cr, uid, ids, context=None):
        #~ Obtenemos id de tiempos
        percent_ids = self.pool.get('percent.acceleration').search(cr, uid, [])
        percent_row = self.pool.get('percent.acceleration').browse(cr, uid, percent_ids)
        
        return percent_row
    
    def crea_tarea_crm(self, cr, uid, ids, etapa, fecha, proyecto, context=None):
        data = self.pool.get('acceleration.ihce').browse(cr, uid, proyecto)
        
        datos = {
            'name': etapa,
            'date_compromise': fecha,
            'user': uid,
            'crm_id': data.crm_id.id,
            'type_task': 'automatico',
        }

        task_id = self.pool.get('crm.task').create(cr, uid, datos, context=context)
            
        return True
        
    def onchange_adiagnostic(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'adiagnostic': valor, 'percent': percent + percent_row.adiagnostic_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Asesoría del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.adiagnostic_percent
                else:
                    per = 0
                result['value'].update({'adiagnostic': valor, 'training': False, 'construction_manuals': False, 'implementation': False, 'cross_audit': False, 'deviation': False, 'acceptation_audit': False, 'audit': False, 'certificate': False, 'percent': per})
        
        return result

    def onchange_training(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'training': valor, 'percent': percent + percent_row.training_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Capacitación del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.training_percent
                else:
                    per = 0
                result['value'].update({'training': valor, 'construction_manuals': False, 'implementation': False, 'cross_audit': False, 'deviation': False, 'acceptation_audit': False, 'audit': False, 'certificate': False, 'percent': per})
        
        return result
    
    def onchange_implementation(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'implementation': valor, 'percent': percent + percent_row.implemetation_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Implementación del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.implemetation_percent
                else:
                    per = 0
                result['value'].update({'implementation': valor, 'cross_audit': False, 'deviation': False, 'acceptation_audit': False, 'audit': False, 'certificate': False, 'percent': per})
        
        return result
        
    def onchange_cross_audit(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'cross_audit': valor, 'percent': percent + percent_row.cross_audit_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Aditoría Cruzada del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.cross_audit_percent
                else:
                    per = 0
                result['value'].update({'cross_audit': valor, 'deviation': False, 'acceptation_audit': False, 'audit': False, 'certificate': False,  'percent': per})
        
        return result

    def onchange_acceptation_audit(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'acceptation_audit': valor, 'percent': percent + percent_row.acceptation_audit_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Aceptación Pre-Auditoría del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.acceptation_audit_percent 
                else:
                    per = 0
                result['value'].update({'acceptation_audit': valor, 'audit': False, 'certificate': False, 'percent': per})
        
        return result
        
    def onchange_audit(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if valor == True:
            result['value'].update({'audit': valor, 'percent': percent + percent_row.audit_percent})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Auditoría del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.audit_percent 
                else:
                    per = 0
                result['value'].update({'audit': valor, 'certificate': False, 'percent': per})
        
        return result
        
    def onchange_certificate(self, cr, uid, ids, valor, percent, company_id, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        anio = fecha_actual.year
        percent_row = self.get_percent(cr, uid, ids, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        
        if ids:
            row = self.browse(cr, uid, ids[0], context=context)
        
        if valor == True:
            result['value'].update({'certificate': valor, 'percent': percent + percent_row.certificate_percent})
            self.pool.get('acceleration.ihce').write(cr, uid, context.get('acceleration_id'), {'service': acele_row.service + 1})
            
            self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
            
            #~ Agregamos actividad al historial de la empresa
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha_actual, 'name':'Certificado emitido del proyecto ' + acele_row.name.encode('utf-8'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            self.indicadores_servicios(cr, uid, [acele_row.id], True, context=context)
                    
        else:
            if ids:
                if percent > 0:
                    per = percent - percent_row.certificate_percent 
                else:
                    per = 0
                result['value'].update({'certificate': valor, 'percent': per})
                self.pool.get('acceleration.ihce').write(cr, uid, context.get('acceleration_id'), {'service': acele_row.service - 1})
                self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':True})
                
                self.indicadores_servicios(cr, uid, [acele_row.id], False, context=context)
                            
        
        return result
    
    def onchange_date_fin_diag(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Diagnostico para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_diag': fecha})
            
        return result
    
    def onchange_date_fin_trai(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Capacitación para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_trai': fecha})
            
        return result
    
    def onchange_date_fin_imple(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Implementación para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_imple': fecha})
            
        return result
    
    def onchange_date_fin_cros(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Auditoría cruzada para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_cros': fecha})
            
        return result
    
    def onchange_date_fin_acep(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Aceptación pre-auditoria para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_acep': fecha})
            
        return result
    
    def onchange_date_fin_audi(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Auditoría para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_audi': fecha})
            
        return result
    
    def onchange_date_fin_cer(self, cr, uid, ids, fecha, company_id, context=None):
        result = {}
        result['value'] = {}
        data = self.pool.get('companies.ihce').browse(cr, uid, company_id, context=context)
        acele_row = self.pool.get('acceleration.ihce').browse(cr, uid, context.get('acceleration_id'), context=context)
        if fecha:
            if fecha < acele_row.date_ini or fecha > acele_row.date_fin:
                raise osv.except_osv(_('Acción Invalida!'), _('La fecha que está ingresado no se encuentra dentro del rango de fechas del proyecto.!'))
            else:
                self.crea_tarea_crm(cr, uid, ids, "Certificado para " + str(data.name), fecha, context.get('acceleration_id'), context=context)
                result['value'].update({'date_fin_cer': fecha})
        
        return result
        
    def finish_proyect(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        if row.certificate == True:
            self.write(cr, uid, [row.id], {'state': 'done'})
            #~ self.message_post(cr, uid, [row.id], body=_("Cerificación Finalizada"), context=context)
        else:
            raise osv.except_osv(_('Acción Invalida!'), _('No puede finalizar el proyecto, la empresa no ha sido certificada.!'))
        
        return True 


    def indicadores_servicios(self, cr, uid, ids, indicador, context=None):
        row = self.pool.get('acceleration.ihce').browse(cr, uid, ids[0], context=context)
            
        if row.option == 'ihce':
            self.meses(cr, uid, ids, 'indicador.aceleracion', indicador, 4, context=context)
        else:
            if row.emprered.id == 1:
                self.meses(cr, uid, ids, 'indicador.emprered.tula', indicador, 9, context=context)
            elif row.emprered.id == 2:
                self.meses(cr, uid, ids, 'indicador.emprered.tizayuca', indicador, 9, context=context)
            elif row.emprered.id == 4:
                self.meses(cr, uid, ids, 'indicador.emprered.mixquiahuala', indicador, 9, context=context)
            elif row.emprered.id == 5:
                self.meses(cr, uid, ids, 'indicador.emprered.huichapan', indicador, 9, context=context)
            elif row.emprered.id == 6:
                self.meses(cr, uid, ids, 'indicador.emprered.zimapan', indicador, 9, context=context)
            elif row.emprered.id == 7:
                self.meses(cr, uid, ids, 'indicador.emprered.apan', indicador, 9, context=context)
            elif row.emprered.id == 8:
                self.meses(cr, uid, ids, 'indicador.emprered.huejutla', indicador, 9, context=context)
            elif row.emprered.id == 9:
                self.meses(cr, uid, ids, 'indicador.emprered.ixmiquilpan', indicador, 9, context=context)
            elif row.emprered.id == 10:
                self.meses(cr, uid, ids, 'indicador.emprered.pachuca', indicador, 9, context=context)
            elif row.emprered.id == 11:
                self.meses(cr, uid, ids, 'indicador.emprered.zacualtipan', indicador, 9, context=context)
            elif row.emprered.id == 12:
                self.meses(cr, uid, ids, 'indicador.emprered.jacala', indicador, 9, context=context)
            elif row.emprered.id == 16:
                self.meses(cr, uid, ids, 'indicador.emprered.atotonilco', indicador, 9, context=context)
            else:
                if row.emprered.id == 13:
                    self.meses(cr, uid, ids, 'indicador.emprered.tulancingo', indicador, 9, context=context)


    def meses(self, cr, uid, ids, objeto, indicador, num, context=None):
        mes = datetime.now().month
        
        row = self.pool.get(objeto).browse(cr, SUPERUSER_ID, num, context=context)
        
        if mes == 1:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'enero': row.enero + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'enero': row.enero - 1})
        elif mes == 2:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'febrero': row.febrero + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'febrero': row.febrero - 1})
        elif mes == 3:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'marzo': row.marzo + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'marzo': row.marzo - 1})
        elif mes == 4:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'abril': row.abril + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'abril': row.abril - 1})
        elif mes == 5:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'mayo': row.mayo + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'mayo': row.mayo - 1})
        elif mes == 6:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'junio': row.junio + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'junio': row.junio - 1})
        elif mes == 7:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'julio': row.julio + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'julio': row.julio - 1})
        elif mes == 8:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'agosto': row.agosto + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'agosto': row.agosto - 1})
        elif mes == 9:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'septiembre': row.septiembre + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'septiembre': row.septiembre - 1})
        elif mes == 10:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'octubre': row.octubre + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'octubre': row.octubre - 1})
        elif mes == 11:
            if indicador:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'noviembre': row.noviembre + 1})
            else:
                self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'noviembre': row.noviembre - 1})
        else:
            if mes == 12:
                if indicador:
                    self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'diciembre': row.diciembre + 1})
                else:
                    self.pool.get(objeto).write(cr, SUPERUSER_ID, num, {'diciembre': row.diciembre - 1})
                    
                    
                    
class date_courses(osv.Model):
    _inherit = 'date.courses'

    _columns = {
        'acceleration_id': fields.many2one('acceleration.ihce', "Aceleración Empresarial"),
    }
    
    def add_company_project(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        con = 0
        data = self.pool.get('acceleration.ihce').browse(cr, uid, row.acceleration_id.id, context=context)
        for line in data.company_list_ids:
            dat = self.pool.get('company.list.acceleration').browse(cr, uid, line.id, context=context)
            cr.execute("SELECT company_id FROM company_invited WHERE company_id = '"+str(dat.company_id.id)+"' AND course_id = '"+str(ids[0])+"';")
            companies = cr.fetchall()
            com = self.pool.get('companies.ihce').browse(cr, uid, dat.company_id.id, context=context)
            if not companies:
                if com.type == 'moral':
                    razon = com.company_name
                else:
                    razon = com.name
                cr.execute("INSERT INTO company_invited (company_id,course_id,company_name,town,phone,email,level_knowledge,state) VALUES ('"+str(com.id)+"','"+str(ids[0])+"','"+str(razon.encode('utf-8'))+"', "+str(com.town.id)+", "+str(com.phone)+", '"+str(com.email.encode('utf-8'))+"', "+str(com.level_knowledge.id)+",'nuevo');")
                con = con +1
        if con > 0:
            self.write(cr, uid, [ids[0]], {'invited': con}, context=context)
            
        return True
    
