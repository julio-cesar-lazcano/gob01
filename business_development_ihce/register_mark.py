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
from datetime import datetime, date, timedelta
from openerp.tools.translate import _
import time


class register_trademark(osv.Model):
    _name = 'register.trademark'
    
    def _get_consultoria(self, cr, uid, ids, field, arg, context=None):
        res = {}
        mark = False
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
                        mark = True
                        break
                    
            res[row.id] = mark
        
        return res
        
    _columns = {
        'name': fields.char("Registro", size=200),
        'description': fields.char("Descripción", size=250),
        'date': fields.date("Fecha de registro"),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'phonetic_search': fields.boolean("Búsqueda Fonética"),
        'phonetic_search_note': fields.char("Notas", size=300),
        'application_format': fields.boolean("Formato de solicitud"),
        'send_format': fields.boolean("Envío de formato de IHCE a cliente"),
        'send_format_note': fields.char("Notas", size=300),
        'vobo_format': fields.boolean("VoBo de formato"),
        'vobo_format_note': fields.char("Notas", size=300),
        'receiving_record': fields.boolean("Recepción de Expediente para ingreso"),
        'receiving_record_nota': fields.char("Notas", size=300),
        'impi': fields.boolean("Ingreso al IMPI"),
        'impi_note': fields.char("Notas", size=300),
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
            ('1', 'Búsqueda fonética'),
            ('2', 'Formato de solicitud'),
            ('3', 'Envío de formato de IHCE a cliente'),
            ('4', 'VoBo de formato'),
            ('5','Recepción de expediente para ingreso'),
            ('6','Ingreso al IMPI'),
            ('7','Por aprobar/rechazar'),
            ], 'Etapa', select=True),
        'time_task': fields.integer("Tiempo"),
        'date_bool': fields.date("Fecha de tarea"),
        'percent': fields.integer("Porcentaje"),
        'consultoria': fields.function(_get_consultoria, type='boolean', string="Consultoría"),
        'servicio': fields.boolean("Servicio"),
        'rechazo_impi': fields.selection([
            ('rechazado', 'Rechazado en el IMPI'),
            ('aceptado', 'Aceptado en el IMPI'),
            ], 'Status IMPI', select=True),
        'date_next_task': fields.date("Fecha de próxima etapa"),
        'crm_id': fields.many2one('crm.project.ihce', "Crm"),
        'task_id': fields.integer("Tarea crm"),
        'courses_ids': fields.one2many('date.courses', 'mark_id', "Relacion cursos"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
        'change_user': fields.boolean("Cambiar Usuario"),
    }
    
    _defaults = {
        'name': 'RM',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'state': 'draft',
        'time_task': 0,
        'percent': 0,
        'consultoria': False,
        'servicio': False,
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
    }
    
    _order = "date_next_task asc"
    
    def create(self, cr, uid, vals, context=None):
        # Genera referencia de registro (nombre) 
        if vals.get('name','RM')=='RM':
            new_seq = self.pool.get('ir.sequence').get(cr, uid, 'register.trademark')
            vals.update({'name':new_seq})
        
        return super(register_trademark, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        return super(register_trademark,self).write(cr, uid, ids, vals, context=context)
    
    def crm_tareas(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now()
        time_row = self.time_development(cr, uid, ids, context=context)
        tarea = ''
        dias = 0
        fecha_siguiente = fecha_actual
        
        if row.task == False:
            tarea = "Búsqueda Fonética"
            dias = time_row.phonetic_search
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '2':
            tarea = "Envío de formato de ihce al cliente"
            dias = time_row.send_format
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '3':
            tarea = "VoBo. de Formato"
            dias = time_row.vobo_format
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '4':
            tarea = "Recepción de Expediente para ingreso"
            fecha_siguiente = fecha_actual + timedelta(days=1)
        elif row.task == '5':
            tarea = "Ingreso al IMPI"
            dias = time_row.impi
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '6':
            tarea = "Por aprobar/rechazar"
            fecha_siguiente = fecha_actual
        
        if row.task_id != 0 or row.task_id != False:
            self.pool.get('crm.task').terminar(cr, uid, [row.task_id], context=context)
            
        datos = {
            'name': tarea,
            'date_compromise': fecha_siguiente,
            'user': uid,
            'type_task': 'automatico',
            'crm_id': row.crm_id.id,
        }

        task_id = self.pool.get('crm.task').create(cr, uid, datos, context=context)
        self.pool.get('crm.task').comenzar(cr, uid, [task_id], context=context)
            
        return task_id
        
    def approved(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de Registro de marca ha sido aprobado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])
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
        
    def not_approved(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de Registro de marca ha sido rechazado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])
        self.write(cr, uid, row.id, {'state':'not_approved', 'task': False}, context=context)
    
    def _check_homework(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_creacion = datetime.strptime(row.date_bool, "%Y-%m-%d").date()
        fecha_ejecucion = datetime.now().date()

        fecha = fecha_ejecucion - fecha_creacion
        dias = fecha.days
        #~ titulo = "Aviso CRM"
        
        if row.state == 'process':
            if row.task == '1':
                if dias >= row.time_task and not row.phonetic_search:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '3':
                if dias >= row.time_task and not row.send_format:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            elif row.task == '4':
                if dias >= row.time_task and not row.vobo_format:
                    self.write(cr, uid, row.id, {'state': 'out_time'}, context=context)
            else:
                if row.task == '6':
                    if dias >= row.time_task and not row.impi:
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
        dias = time_row.phonetic_search
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        res = {
            'name':'Process : ' + row.name,
            'model':'register.trademark',
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

        #~ Agregamos actividad al historial de la empresa
        fecha_crm = datetime.now()
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_crm, 'name':'Se ha iniciado el servicio de Registro de marca', 'user':uid, 'date_compromise': fecha_crm, 'state':'done'}, context=context)
        
        #~ Agregamos proyecto al crm del usuario
        valores = {
            'name': row.description.encode('utf-8'),
            'company_id': row.company_id.id,
            'state': 'a-draft',
            'type_crm': 'automatico',
        }
        crm_id = self.pool.get('crm.project.ihce').create(cr, uid, valores, context=context)
        self.pool.get('crm.project.ihce').comenzar(cr, uid, [crm_id], context=context)
        
        id_cron = self.pool.get('ir.cron').create(cr, uid, res)
        
        self.write(cr, uid, row.id, {'cron_id': id_cron, 'state':'process', 'time_task': dias, 'date_bool': fecha_actual, 'date_next_task': fecha_siguiente, 'crm_id': crm_id}, context=context)
        
        #~ Se crea la tarea
        task = self.crm_tareas(cr, uid, ids, context=context)
        self.write(cr, uid, row.id, {'task_id': task,'task': '1'}, context=context)
        
        return True
    
    def re_start(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        time_row = self.time_development(cr, uid, ids, context=context)
        
        time_time = 0
        fecha_actual = datetime.now().date()

        if row.task == '1':
            time_time = time_row.phonetic_search
            dias = time_row.phonetic_search
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '2':
            time_time = 0
        elif row.task == '3':
            time_time = time_row.send_format
            dias = time_row.send_format
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '4':
            time_time = time_row.vobo_format
            dias = time_row.vobo_format
            fecha_siguiente = fecha_actual + timedelta(days=dias)
        elif row.task == '5':
            time_time = 0
        else:
            if row.task == '6':
                time_time = time_row.impi

        if row.state == 'out_time':
            self.write(cr, uid, row.id, {'state':'process','time_task':time_time, 'date_bool': fecha_actual, 'date_next_task': fecha_siguiente}, context=context)
            #~ Reabrimos el tiempo de la tarea en el crm
            self.pool.get('crm.task').write(cr, uid, [row.task_id], {'state': 'b-progress', 'date_compromise':fecha_siguiente})
        
        return True

    
    def onchange_task2(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.send_format
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        if ids:
            if valor == True:
                percent = time_row.phonetic_search_percent
                row = self.browse(cr, uid, ids[0], context=context)
                
                self.write(cr, uid, ids[0], {'phonetic_search': valor, 'task': '2', 'time_task':0, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                id_crm = self.pool.get('crm.ihce').create(cr, SUPERUSER_ID, {'company_id': company_id, 'date':fecha, 'name':'Búsqueda fonética de Registro de marca',  'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    dias = time_row.phonetic_search
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    row = self.browse(cr, uid, ids[0], context=context)
                    percent = row.percent - time_row.phonetic_search_percent
                    
                    self.write(cr, uid, ids[0], {'phonetic_search': valor, 'task': '1', 'time_task': time_row.phonetic_search, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
        
        return True
    
    def onchange_task3(self, cr, uid, ids, valor, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.send_format
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        if ids:
            if valor == True:
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids[0], {'task_id': task_id, 'application_format': valor, 'task': '3', 'time_task':time_row.send_format, 'date_bool': fecha_actual,'date_next_task': fecha_siguiente}, context=context)
            
            else:
                if valor == False:
                    dias = time_row.send_format
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                   
                    self.write(cr, uid, ids[0], {'application_format': valor, 'task': '2', 'time_task':0, 'date_bool': fecha_actual,'date_next_task': fecha_siguiente}, context=context)
        
        return True
    
    def onchange_task4(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.vobo_format
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.send_format_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids[0], {'task_id': task_id, 'send_format': valor, 'task': '4', 'time_task': time_row.vobo_format, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Envío de formato de IHCE de Registro de marca', 'user':uid, 'date_compromise': fecha, 'state':'done'}, context=context)

            else:
                if valor == False:
                    dias = time_row.send_format
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    row = self.browse(cr, uid, ids[0], context=context)
                    percent = row.percent - time_row.send_format_percent
                    
                    self.write(cr, uid, ids[0], {'send_format': valor, 'task': '3', 'time_task': time_row.send_format, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
        
        return True
    
    def onchange_task5(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        dias = time_row.impi
        fecha_siguiente = fecha_actual + timedelta(days=dias)

        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.vobo_format_percent
               
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids[0], {'task_id': task_id, 'vobo_format': valor, 'task': '5' ,'time_task': 0, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'VoBo de formato de Registro de marca', 'user':uid, 'date_compromise': fecha, 'state':'done'}, context=context)

            else:
                if valor == False:
                    dias = time_row.vobo_format
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    row = self.browse(cr, uid, ids[0], context=context)
                    percent = row.percent - time_row.vobo_format_percent
                   
                    self.write(cr, uid, ids[0], {'vobo_format': valor, 'task': '4' ,'time_task': time_row.vobo_format, 'date_bool': fecha_actual, 'percent': percent,'date_next_task': fecha_siguiente}, context=context)
        
        return True
    
    
    #~ AQUI SE CUENTA EL SERVICIO DE REGISTRO DE MARCA
    def onchange_task6(self, cr, uid, ids, valor, company_id, opcion, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()
        anio = datetime.now().year
        dias = time_row.impi
        fecha_siguiente = fecha_actual + timedelta(days=dias)
        
        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.receiving_record_percent
                
                task_id = self.crm_tareas(cr, uid, ids, context=context)
                
                self.write(cr, uid, ids[0], {'task_id': task_id, 'receiving_record': valor, 'task': '6', 'time_task': time_row.impi, 'date_bool': fecha_actual, 'percent': percent, 'servicio':True,'date_next_task': fecha_siguiente}, context=context)
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Recepción de Expediente para ingreso de Registro de marca', 'user':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
            else:
                if valor == False:
                    row = self.browse(cr, uid, ids[0], context=context)
                    percent = row.percent - time_row.receiving_record_percent
                    
                    self.write(cr, uid, ids[0], {'receiving_record': valor, 'task': '5', 'time_task': 0, 'date_bool': fecha_actual, 'percent': percent, 'servicio':False,'date_next_task': fecha_siguiente}, context=context)
        
        return True
    
    def onchange_task7(self, cr, uid, ids, valor, company_id, context=None):
        time_row = self.time_development(cr, uid, ids, context=context)
        
        fecha_actual = datetime.now().date()
        fecha = datetime.now()

        if ids:
            if valor == True:
                row = self.browse(cr, uid, ids[0], context=context)
                percent = row.percent + time_row.impi_percent
                self.pool.get('crm.task').terminar(cr, uid, [row.task_id], context=context)
                
                self.write(cr, uid, ids[0], {'impi': valor, 'state': 'done', 'percent': percent, 'task': '7', 'date_next_task': False}, context=context)
                self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
                
                #~ Agregamos actividad al historial de la empresa
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': company_id, 'date':fecha, 'name':'Ingreso al IMPI de Registro de marca', 'user':uid, 'date_compromise': fecha, 'state':'done'}, context=context)
                
            else:
                if valor == False:
                    dias = time_row.impi
                    fecha_siguiente = fecha_actual + timedelta(days=dias)
                    row = self.browse(cr, uid, ids[0], context=context)
                    percent = row.percent - time_row.impi_percent
                    
                    self.write(cr, uid, ids[0], {'impi': valor, 'state':'process','task': '6', 'time_task': time_row.impi, 'date_bool': fecha_actual, 'percent': percent, 'date_next_task': fecha_siguiente}, context=context)
                    self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':True})

        return True
    
    def abandoned(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        self.write(cr, uid, row.id, {'state':'abandoned'}, context=context)
        #~ Si el proyecto es abandonado, abandonamos tambien el proyecto en el crm
        self.pool.get('crm.project.ihce').abandonar(cr, uid, [row.crm_id.id], context=context)
        
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de Registro de marca ha sido abandonado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        self.pool.get('ir.cron').unlink(cr, uid, [row.cron_id.id])
        
    
    def re_start_all(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Agregamos actividad al historial de la empresa
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de Registro de marca ha sido reiniciado', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        for ro in row.courses_ids:
            self.pool.get('date.courses').write(cr, uid, [ro.id], {'mark_id': False}, context=context)
        
        self.pool.get('crm.project.ihce').abandonar(cr, uid, [row.crm_id.id], context=context)
        
        self.write(cr, uid, row.id, {'task_id': 0, 'date': fecha_actual, 'state':'draft', 'consultoria': False, 'servicio': False, 'phonetic_search': False, 'application_format': False, 'send_format': False, 'vobo_format': False, 'receiving_record': False, 'impi': False, 'percent': 0, 'task': 0, 'date_next_task': False})
        
    
    def mail_partner(self, cr, uid, ids, context=None):
        emails = ''
        email_vals = {}
        
        mail_message_obj = self.pool.get('mail.mail')
        mod_obj = self.pool.get('ir.model.data')
        user_row = self.pool.get('res.users').browse(cr, uid, uid)
        row = self.browse(cr, uid, ids, context)[0]
        
        data = self.pool.get('companies.ihce').browse(cr, uid, row.company_id.id, context=context)
        email = data.email
        email_from = user_row.email
        
        if email_from:
            subject = "Aviso Registro de Marca"
            
            body_text = "<p>  </p> "

            email_vals.update({'subject':subject, 'body_html':body_text, 'body':body_text, 'email_to': email, 'email_from': email_from})
            mail_id = mail_message_obj.create(cr, uid, email_vals )
            
            res = mod_obj.get_object_reference(cr, uid, 'mail_ihce', 'mail_compose_message_form_ihce')
            res_id = res and res[1] or False
            
            self.write(cr, uid, ids[0], {'state': 'done'})
            
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.mail',
                'res_id': mail_id,
                'view_id': [res_id],
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': context,
            }
            
        else:
            raise osv.except_osv(_('Advertencia!'), _('El usuario no tiene correo electrónico!'))
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['draft']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar el registro.!'))

        return super(register_trademark, self).unlink(cr, uid, unlink_ids, context=context)
        
    
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        result = {}
        result['value'] = {}
        
        if user_id:
            row = self.pool.get('res.users').browse(cr, uid, user_id)
            
            result['value'].update({'option': row.option, 'area': row.area.id, 'emprered': row.emprered.id})
        
        return result
