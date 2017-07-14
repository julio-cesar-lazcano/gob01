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

class bar_code(osv.Model):
    _name = 'bar.code'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _get_consultoria(self, cr, uid, ids, field, arg, context=None):
        res = {}
        code = False
        lista_ids = ""
        for row in self.browse(cr, uid, ids, context=context):
            for ro in row.courses_ids:
                lista_ids = str(ro.id) + ","
            if lista_ids:
                lista_ids = lista_ids[:-1]
                cr.execute("SELECT courses_id FROM date_courses WHERE id IN ("+str(lista_ids)+") AND state = 'done' AND type = 'consultoria' GROUP BY courses_id;")
                cours = cr.fetchall()
                for ro in cours:
                    data = self.pool.get('courses.ihce').browse(cr, uid, ro[0], context=context)
                    if data.state_cours == True:
                        code = True
                        break
            
            res[row.id] = code
        
        return res
        
    _columns = {
        'name': fields.char("Registro", size=200),
        'description': fields.char("Descripción", size=250),
        'date': fields.date("Fecha de registro"),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'requirements_sheet': fields.boolean("Entrega de Hoja de Requisitos"),
        'requirements_sheet_note': fields.char("Notas"),
        'information_gs1': fields.boolean("Llenado de Información GS1"),
        'information_gs1_note': fields.char("Notas"),
        'reception_information': fields.boolean("Recepción de Información"),
        'reception_information_note': fields.char("Notas"),
        'send_information_gs1': fields.boolean("Envío de Información a GS1"),
        'send_information_gs1_note': fields.char("Notas"),
        'reception_letters': fields.boolean("Recepción de Cartas de Asociado"),
        'reception_letters_note': fields.char("Notas"),
        'advice_company': fields.boolean("Citar a empresa para asesoría"),
        'advice_company_note': fields.char("Notas"),
        'notes': fields.text("Observación General"),
        'state': fields.selection([
            ('draft', 'Nuevo'),
            ('process', 'Proceso'),
            ('out_time', 'Fuera de tiempo'),
            ('done', 'Por aprobar/Rechazar'),
            ('approved', 'Aprobado'),
            ('not_approved','Rechazado'),
            ('abandoned','Abandonado'),
            ], 'Estado', select=True),
        'cron_id': fields.many2one('ir.cron', "Tarea en proceso"),
        'task': fields.selection([
            ('1', 'Entrega de Hoja de Requisitos'),
            ('2', 'Llenado de información a GS1'),
            ('3', 'Recepción de información'),
            ('4', 'Envío de información a GS1'),
            ('5', 'Recepción de cartas de asociado'),
            ('6', 'Citar a empresa para asesoría'),
            ('7', 'Por aprobar/rechazar'),
            ], 'Etapa', select=True),
        'time_task': fields.integer("Tiempo"),
        'date_bool': fields.date("Fecha de tarea"),
        'percent': fields.integer("Porcentaje"),
        'consultoria': fields.function(_get_consultoria, type='boolean', string="Consultoría"),
        'servicio': fields.boolean("Servicio"),
        'type_membership': fields.many2one('type.membership', 'Tipo de membresía'),
        'mail_gs1': fields.selection([
            ('recibido', 'Información aceptada en GS1'),
            ('rechazado', 'Información rechazada en GS1'),
            ], 'Status GS1', select=True),
        'date_next_task': fields.date("Fecha de próxima etapa"),
        'crm_id': fields.many2one('crm.project.ihce',"Proyecto crm"),
        'task_id': fields.integer("Tarea crm"),
        'courses_ids': fields.one2many('date.courses', 'code_id', "Relación cursos"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
        'change_user': fields.boolean("Cambiar Usuario"),
        
    }
    
    _defaults = {
        'name': 'BC',
        'state': 'draft',
        'task': 0,
        'time_task': 0,
        'percent': 0,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'consultoria': False,
        'servicio': False,
        'asesoria': False,
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'change_user': False,
    }
    
    _order = "date_next_task asc"
    
    def create(self, cr, uid, vals, context=None):
        # Genera referencia de registro (nombre) 
        if vals.get('name','BC')=='BC':
            new_seq = self.pool.get('ir.sequence').get(cr, uid, 'bar.code')
            vals.update({'name':new_seq})
        return super(bar_code, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        return super(bar_code,self).write(cr, uid, ids, vals, context=context)
        
    def crm_tareas(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now()
        time_row = self.time_development(cr, uid, ids, context=context)

        if row.task == False:
            tarea = "Entrega de Hoja de Requisitos"
            dias = time_row.requirements_sheet
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '1':
            tarea = "Llenado de Información a GS1"
            dias = time_row.information_gs1
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '2':
            tarea = "Recepción de Información"
            dias = time_row.reception_information
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '3':
            tarea = "Envío de Información a GS1"
            dias = time_row.send_information_gs1
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '4':
            tarea = "Recepción de Cartas de asociado"
            dias = time_row.reception_letters
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '5':
            tarea = "Citar a empresa para asesoría"
            dias = time_row.advice_company
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '6':
            tarea = "Por aprobar/rechazar"
            fecha_siguiente = fecha_actual

        if row.task_id != 0:
            self.pool.get('crm.task').terminar(cr, uid, [row.task_id], context=context)
        
        datos = {
            'name': tarea,
            'date_compromise': fecha_siguiente,
            'user': uid,
            'crm_id': row.crm_id.id,
            'type_task': 'automatico',
        }
        
        task_id = self.pool.get('crm.task').create(cr, uid, datos, context=context)
            
        return task_id
        
    def approved(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El proceso de Código de Barras ha sido aprobado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        self.write(cr, uid, row.id, {'state':'approved', 'task': False}, context=context)
        #~ Si el proyecto es aprobado, finalizamos el proyecto en el crm, solo si todos sus tareas estan finalizadas
        ban = True
        crm_data = self.pool.get('crm.project.ihce').browse(cr, uid, row.crm_id.id, context=context)
        for task in crm_data.task_ids:
            crm_task = self.pool.get('crm.task').browse(cr, uid, task.id, context=context)
            if crm_task.state != 'd-done' or crm_task.state != 'f-cancel':
                ban = False
                break
        if ban:
            self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state': 'd-done'})
        
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])
        
    def not_approved(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El proceso de Código de Barras ha sido rechazado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
       
        self.write(cr, uid, row.id, {'state':'not_approved', 'task': False}, context=context)
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])
    
    def _check_homework(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_creacion = datetime.strptime(row.date_bool, "%Y-%m-%d").date()
        fecha_ejecucion = datetime.now().date()

        fecha = fecha_ejecucion - fecha_creacion
        dias = fecha.days
        #~ titulo = "Aviso CRM"
        
        if row.state == 'process':
            if row.task == '1':
                if dias >= row.time_task and not row.requirements_sheet:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '2':
                if dias >= row.time_task and not row.information_gs1:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '3':
                if dias >= row.time_task and not row.reception_information:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '4':
                if dias >= row.time_task and not row.send_information_gs1:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '5':
                if dias >= row.time_task and not row.reception_letters:
                    texto = "<p>El tiempo para la recepción de cartas de asociado del código de barras " + str(row.description.encode('utf-8')) + ", se ha terminado.</p> "
                    self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, uid, context=context)
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            else:
                if row.task == '6':
                    if dias >= row.time_task and not row.advice_company:
                        self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
        
        return True
    
    def time_development(self, cr, uid, ids, context=None):
        #~ Obtenemos id de tiempos
        time_ids = self.pool.get('time.development').search(cr, uid, [])
        time_row = self.pool.get('time.development').browse(cr, uid, time_ids)
        
        return time_row
        
    def start_process(self, cr, uid, ids, context=None):
        #~ En el momento que comienza el proceso tiene un tiempo para cumplir la primera tarea.
        row = self.browse(cr, uid, ids[0], context=context)
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        dias = time_row.requirements_sheet
        fecha_siguiente = fecha_actual + timedelta(days=dias)
       
        res = {
            'name':'Process : ' + row.name,
            'model':'bar.code',
            'args': repr([ids]), 
            'function':'_check_homework',
            'priority':5,
            'interval_number':1,
            'interval_type':'work_days',
            'user_id':uid,
            'numbercall':-1,
            'doall':False,
            'active':True
        }
        
        id_cron = self.pool.get('ir.cron').create(cr, uid, res)
        
        #~ Al aprobarse el registro se crea un proyecto en el crm del usuario.
        valores = {
            'name': row.description.encode('utf-8'),
            'company_id': row.company_id.id,
            'state': 'a-draft',
            'type_crm': 'automatico',
        }
        crm_id = self.pool.get('crm.project.ihce').create(cr, uid, valores, context=context)
        self.pool.get('crm.project.ihce').comenzar(cr, uid, [crm_id], context=context)
        
        #~ Agregamos actividad al historial de la empresa
        fecha_crm = datetime.now()
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_crm, 'name':'Empezó proceso de Código de Barras', 'user':uid, 'date_compromise': fecha_crm, 'state':'done'}, context=context)
        
        self.write(cr, uid, row.id, {'cron_id': id_cron, 'state':'process', 'time_task': time_row.requirements_sheet, 'date_bool': fecha_actual, 'date_next_task': fecha_siguiente,'crm_id':crm_id}, context=context)
        
        task = self.crm_tareas(cr, uid, ids, context=context)
        self.write(cr, uid, row.id, {'task_id': task, 'task': '1'}, context=context)
        
        return True
    
    def re_start(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        time_row = self.time_development(cr, uid, ids, context=context)
        
        time_time = 0
        fecha_actual = datetime.now().date()

        if row.task == '1':
            time_time = time_row.requirements_sheet
            dias = time_row.requirements_sheet
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '2':
            time_time = time_row.information_gs1
            dias = time_row.information_gs1
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '3':
            time_time = time_row.reception_information
            dias = time_row.reception_information
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '4':
            time_time = time_row.send_information_gs1
            dias = time_row.send_information_gs1
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '5':
            time_time = time_row.reception_letters
            dias = time_row.reception_letters
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        else:
            if row.task == '6':
                time_time = time_row.advice_company
                dias = time_row.advice_company
                fecha_siguiente = fecha_actual + timedelta(days=dias)

        if row.state == 'out_time':
            self.write(cr, uid, row.id, {'state':'process','time_task':time_time, 'date_bool': fecha_actual, 'date_next_task': fecha_siguiente}, context=context)
            #~ Reabrimos el tiempo de la tarea en el crm
            self.pool.get('crm.task').write(cr, uid, [row.task_id], {'state': 'b-progress', 'date_compromise':fecha_siguiente})
        
            
        return True
    
    def onchange_task2(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.information_gs1
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.requirements_sheet_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids, {'task_id': task_id, 'requirements_sheet': valor, 'task': '2', 'time_task':time_row.information_gs1, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Entrega de hoja de requisitos de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.requirements_sheet
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.requirements_sheet_percent
                    
                    self.write(cr, uid, ids, {'requirements_sheet': valor, 'task': '1', 'time_task':time_row.requirements_sheet, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
            
        return result
    
    def onchange_task3(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.reception_information
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.information_gs1_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids, {'task_id': task_id, 'information_gs1': valor, 'task': '3', 'time_task':time_row.reception_information, 'date_bool': fecha_actual, 'percent':percent, 'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Llenado de información a GS1 de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.information_gs1
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.information_gs1_percent
                    
                    self.write(cr, uid, ids, {'information_gs1': valor, 'task': '2', 'time_task':time_row.information_gs1, 'date_bool': fecha_actual, 'percent':percent, 'date_next_task': fecha_siguiente}, context=context)
            
        return result
    
    def onchange_task4(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.send_information_gs1
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.reception_information_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids, {'task_id': task_id, 'reception_information': valor, 'task': '4', 'time_task': time_row.send_information_gs1, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Recepción de información de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.reception_information
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.reception_information_percent
                    
                    self.write(cr, uid, ids, {'reception_information': valor, 'task': '3', 'time_task': time_row.reception_information, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
            
        return result
    
    
    #~ AQUI SE CUENTA EL SERVICIO DE CODIGO DE BARRAS
    def onchange_task5(self, cr, uid, ids, valor, company_id, opcion, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        anio = datetime.now().year
        dias = time_row.reception_letters
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.send_information_gs1_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids, {'task_id': task_id, 'send_information_gs1': valor, 'task': '5' ,'time_task': time_row.reception_letters, 'date_bool': fecha_actual, 'percent': percent, 'servicio':True, 'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Envío de información a GS1 de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
                    
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.send_information_gs1
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.send_information_gs1_percent
                    
                    self.write(cr, uid, ids, {'send_information_gs1': valor, 'task': '4' ,'time_task': time_row.send_information_gs1, 'date_bool': fecha_actual, 'percent': percent, 'servicio':False, 'date_next_task': fecha_siguiente}, context=context)
                    
            
        return result
    
    def onchange_task6(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.advice_company
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.reception_letters_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids, {'task_id': task_id, 'reception_letters': valor, 'task': '6', 'time_task': time_row.advice_company, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Recepción de cartas de asociado de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.reception_letters
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.reception_letters_percent
                    
                    self.write(cr, uid, ids, {'reception_letters': valor, 'task': '5', 'time_task': time_row.reception_letters, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
            
        return result
    
    def onchange_task7(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        fecha_siguiente = fecha_actual + timedelta(days=2)
        result = {}
        result['value'] = {}
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.advice_company_percent
                
                self.pool.get('crm.task').terminar(cr, uid, [row.task_id], context=context)
                
                self.write(cr, uid, ids, {'advice_company': valor, 'state': 'done', 'percent': percent, 'task': '7', 'date_next_task': False}, context=context)
                self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Cita a empresa para asesoría de código de barras', 'user_id':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    dias = time_row.advice_company
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    percent = row.percent - time_row.advice_company_percent
                    
                    self.write(cr, uid, ids, {'advice_company': valor, 'task': '6', 'time_task': time_row.advice_company, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente, 'state':'process'}, context=context)
                    self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':True})
            
        return result
    
    def abandoned(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        self.write(cr, uid, row.id, {'state':'abandoned'}, context=context)
        #~ Si el proyecto es abandonado, abandonamos tambien el proyecto en el crm
        self.pool.get('crm.project.ihce').abandonar(cr, uid, [row.crm_id.id], context=context)
        
        fecha_actual = datetime.now()

        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El proceso de Código de Barras ha sido abandonado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])

        
    def re_start_all(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now()

        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El proceso de Código de Barras ha sido reiniciado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        for ro in row.courses_ids:
            self.pool.get('date.courses').write(cr, uid, [ro.id], {'code_id': False}, context=context)
        
        self.pool.get('crm.project.ihce').abandonar(cr, uid, [row.crm_id.id], context=context)
        
        self.write(cr, uid, row.id, {'task_id': 0, 'date': fecha_actual, 'state':'draft', 'consultoria': False, 'servicio': False, 'requirements_sheet': False, 'information_gs1': False, 'reception_information': False, 'send_information_gs1': False, 'reception_letters': False, 'advice_company': False, 'percent': 0, 'task': 0, 'date_next_task': False})

    
    def return_task(self, cr, uid, ids, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        fecha_actual = datetime.now().date()
        dias = time_row.information_gs1
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        percent = time_row.requirements_sheet_percent
        
        self.write(cr, uid, ids[0], {'reception_information': False, 'information_gs1': False, 'send_information_gs1': False, 'percent': percent, 'task': '2', 'time_task':time_row.information_gs1, 'date_bool': fecha_actual,'date_next_task':fecha_siguiente})
        
        self.crm_tareas(cr, uid, ids, context=context)

    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['draft']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar el registro.!'))

        return super(bar_code, self).unlink(cr, uid, unlink_ids, context=context)

    
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        result = {}
        result['value'] = {}
        
        if user_id:
            row = self.pool.get('res.users').browse(cr, uid, user_id)
            
            result['value'].update({'option': row.option, 'area': row.area.id, 'emprered': row.emprered.id})
        
        return result
        


        
class type_membership(osv.Model):
    _name = 'type.membership'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Tipo de membresía"),
    }


