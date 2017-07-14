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
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta
import time

class crm_project_ihce(osv.Model):
    _name = "crm.project.ihce"
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    #~ Cambiamos el estado del proyecto, si ya no hay tareas fuera de tiempo
    def _get_state(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            ban = True
            if row.state == 'c-out_time':
                for task_row in row.task_ids:
                    if task_row.state == 'c-out':
                        ban = False
                        break
                        
                if ban == False:
                    res[row.id] = False
                else:
                    res[row.id] = True
                    self.write(cr, uid, row.id, {'state':'b-progress'})
            else:
                res[row.id] = True
        return res
    
    
    _columns = {
        'name': fields.char("Proyecto", size=200),
        'date': fields.date("Fecha de evento"),
        'user_id': fields.many2one('res.users',"Responsable del proyecto"),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
        'company_id': fields.many2one('companies.ihce', "Beneficiario"),
        'task_ids': fields.one2many('crm.task', 'crm_id', "Tareas"),
        'state': fields.selection([('a-draft','Nuevo'),('b-progress','Proceso'),('c-out_time','Fuera de tiempo'),('d-done','Finalizado'),('e-abandoned','Abandonado'),('f-cancel','Cancelado')], "Estado"),
        'notes': fields.text("Notas"),
        'color': fields.integer('Color Index'),
        'priority': fields.selection([('0','Normal'),('1','Importante')], "Actividad Relevante"),
        'type_crm': fields.selection([('manual','Manual'),('automatico','Automático')], "Tipo de proyecto"),
        'state_proyect': fields.function(_get_state, type='boolean', string="Estado del proyecto"),
        'cancel_reason': fields.one2many('cancellation.reason.wizard', 'project_id', "Motivos de cancelación"),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'state': 'a-draft',
        'color': 0,
        'type_crm': 'manual',
        'state_proyect': True,
        'priority': '0',
    }
    
    _order = 'state'
    
    #~ Cambia el estado de la actividad de borrador a proceso
    def comenzar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Se envía correo al usuario
        titulo = "Aviso CRM"
        texto = "<p>Se te ha asignado el proyecto "+str(row.name.encode('utf-8'))+". Ya puedes empezar a crear tareas.</p> "
        self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, uid, context=context)

        self.write(cr, uid, [row.id], {'state': 'b-progress'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Proyecto Iniciado"), context=context)
        
        return True
    
    #~ Cambia el estado de la actividad de proceso a realizado o terminado
    def terminar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        ban = True
        for line in row.task_ids:
            data = self.pool.get('crm.task').browse(cr, uid, line.id, context=context)
            if data.state == 'b-progress':
                raise osv.except_osv(_('Advertencia!'), _('No puede finalizar el proyecto, aún hay tareas abiertas.!'))
                ban = False
                break
        if ban:
            #~ Se envía correo al usuario
            titulo = "Aviso CRM"
            texto = "<p>El proyecto "+str(row.name.encode('utf-8'))+" ha sido finalizado.</p> "
            self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, uid, context=context)
            
            self.write(cr, uid, [row.id], {'state': 'd-done'})
            
            #~ self.message_post(cr, uid, [row.id], body=_("Proyecto Terminado"), context=context)
        
        return True
    
    def action_cancel(self, cr, uid, ids, context=None):
        """  
        Función para cancelar los projectos y cambiarlas a estado Cancelodo
        """
        rows = self.browse(cr, uid, ids[0], context)
        for row in rows.task_ids:
            if row.state != 'd-done' or row.state != 'f-cancel':
                self.pool.get('crm.task').action_cancel(cr, uid, [row.id], context)
        # Se actualiza el estado del proyecto a cancelado
        self.write(cr, uid, [rows.id], {'state':'f-cancel'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Proyecto Cancelado"), context=context)
        
        return True
    
    def action_cancel_wizard(self, cr, uid, ids, context=None):
        """
        Método para crear el wizard y seleccionar el motivo de la cancelación
        """
        # Wizard para cancelar el proyecto
        cancel_project_id = self.pool.get("cancellation.reason.wizard").create(cr, uid, {'project_id':ids[0]}, context=context)

        res = {
            'name':("Cancelación de Proyecto"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'cancellation.reason.wizard',
            'res_id': cancel_project_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': context,
        }
        return res
    
    #~ Cambia el estado de la actividad a cancelado.
    def abandonar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        
        #~ Abandonamos primero todas sus tareas.
        for task in row.task_ids:
            data = self.pool.get('crm.task').browse(cr, uid, task.id, context=context)
            if data.state == 'b-progress' or data.state == 'c-out':
                self.pool.get('crm.task').write(cr, uid, [data.id], {'state':'e-abandoned'})
                self.pool.get('ir.cron').write(cr, uid, [data.cron_id.id], {'active': False})
        
        self.write(cr, uid, [row.id], {'state': 'e-abandoned'})
        #~ Se envía correo al usuario
        titulo = "Aviso CRM"
        texto = "<p>El proyecto "+str(row.name.encode('utf-8'))+" ha sido abandonado.</p> "
        self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, uid, context=context)
        
        #~ self.message_post(cr, uid, [row.id], body=_("Proyecto Abandonado"), context=context)
        
        return True
    
    def reabrir(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Reabrimos tambien sus tareas
        for task in row.task_ids:
            data = self.pool.get('crm.task').browse(cr, uid, task.id, context=context)
            if data.state == 'e-abandoned':
                self.pool.get('crm.task').write(cr, uid, [data.id], {'state':'b-progress'})
                self.pool.get('ir.cron').write(cr, uid, [data.cron_id.id], {'active': True})
        
        self.write(cr, uid, row.id, {'state': 'b-progress'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Proyecto Reabierto"), context=context)
        
        return True
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['a-draft','f-cancel']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Inválida!'), _('No puede eliminar el proyecto.!'))

        return super(crm_project_ihce, self).unlink(cr, uid, unlink_ids, context=context)
    
    def adjuntos(self, cr, uid, ids, context=None):
        ids_attachment = self.pool.get('ir.attachment').search(cr, uid, [('res_id','=',ids[0]),('res_model','=','crm.project.ihce')])
        return True


class crm_task(osv.Model):
    _name = 'crm.task'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Actividad", size=200),
        'date': fields.date("Fecha de Inicio"),
        'date_compromise': fields.datetime("Fecha Compromiso"),
        'user_id': fields.many2one('res.users',"Responsable de la tarea"),
        'state': fields.selection([('b-progress','Abierta'),('c-out','Fuera de tiempo'),('d-done','Terminada'),('e-abandoned','Abandonada'),('f-cancel','Cancelado')], "Estado"),
        'crm_id': fields.many2one('crm.project.ihce', 'Proyecto'),
        'notes': fields.text("Notas"),
        'color': fields.integer('Color Index'),
        'cron_id': fields.many2one('ir.cron', "Tarea en proceso"),
        'call': fields.boolean("Llamada"),
        'meeting': fields.boolean("Reunión"),
        'type_task': fields.selection([('manual','Manual'),('automatico','Automática')], "Tipo de tarea"),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'state': 'b-progress',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'color': 0,
        'type_task': 'manual',
    }
    
    _order = "date_compromise asc"
    
    def create(self, cr, uid, vals, context=None):
        res = super(crm_task, self).create(cr, uid, vals, context)
        self.comenzar(cr, uid, [res], context=context)
        
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        #~ Si la fecha compromiso ha sido cambiada y además la tarea se encuentra fuera de tiempo, se está reabriendo el tiempo de esa tarea, por lo tanto la pasamos a estado proceso.
        if ids:
            if vals.get('date_compromise'):
                row = self.browse(cr, uid, ids[0], context=context)
                if row.state == 'c-out':
                    vals.update({'state': 'b-progress'})
        return super(crm_task,self).write(cr, uid, ids, vals, context=context)
    
    def _check_task(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_ejecucion = datetime.now()
        fecha_compromiso = datetime.strptime(row.date_compromise, "%Y-%m-%d %H:%M:%S")
        
        if row.state == 'b-progress':
            if fecha_compromiso < fecha_ejecucion:
                #~ Enviar correo que el tiempo de la tarea se terminó
                titulo = "Aviso CRM"
                texto = "<p>El tiempo para la tarea "+str(row.name.encode('utf-8'))+" se ha terminado.</p> "
                self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, row.user_id.id, context=context)
                
                self.write(cr, uid, ids[0], {'state': 'c-out'}, context=context)
                self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state':'c-out_time'})
        return True
    
    #~ Cambia el estado de la actividad de borrador a proceso
    def comenzar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        data = self.pool.get('crm.project.ihce').browse(cr, uid, row.crm_id.id, context=context)
        
        res = {
            'name':'Process : ' + row.name,
            'model':'crm.task',
            'args': repr([ids]), 
            'function':'_check_task',
            'priority':5,
            'interval_number':1,
            'interval_type':'work_days',
            'user_id':uid,
            'numbercall':-1,
            'doall':False,
            'active':True
        }
        
        id_cron = self.pool.get('ir.cron').create(cr, uid, res)
        self.write(cr, uid, [row.id], {'cron_id': id_cron, 'state': 'b-progress'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Tarea Iniciada"), context=context)
        
        return True
    
    #~ Cambia el estado de la actividad de proceso a realizado o terminado
    def terminar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0],context=context)
        self.write(cr, uid, [row.id], {'state': 'd-done'})
        
        data = self.pool.get('crm.project.ihce').browse(cr, uid, row.crm_id.id, context=context)
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Tarea Concluida"), context=context)
        
        return True
    
    #~ Cambia el estado de la actividad a cancelado.
    def action_cancel(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0],context=context)
        data = self.pool.get('crm.project.ihce').browse(cr, uid, row.crm_id.id, context=context)
        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active':False})
        
        titulo = "Aviso CRM"
        texto = "<p>La tarea "+str(row.name.encode('utf-8'))+" del proyecto "+ str(data.name.encode('utf-8')) +" ha sido cancelada.</p> "
        self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, row.user_id.id, context=context)
       
        self.write(cr, uid, [row.id], {'state': 'f-cancel'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Tarea Cancelada"), context=context)
        
        return True
    
    
    #~ Cambia el estado de la actividad a cancelado.
    def abandonar(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Se envía correo al usuario
        titulo = "Aviso CRM"
        texto = "<p>La tarea "+str(row.name.encode('utf-8'))+" ha sido abandonada.</p> "
        self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, uid, context=context)

        self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active': False})
        
        self.write(cr, uid, row.id, {'state': 'e-abandoned'})
        
        #~ self.message_post(cr, uid, [row.id], body=_("Tarea Abandonada"), context=context)
        
        return True
    
    def reabrir(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        #~ Solo podremos reabrir una tarea que pertenezca a un proyecto en proceso
        crm_data = self.pool.get('crm.project.ihce').browse(cr, uid, row.crm_id.id, context=context)
        if crm_data.state == 'b-progress':
            self.write(cr, uid, ids, {'state': 'b-progress'})
            self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], {'active': True})
            
            #~ self.message_post(cr, uid, [row.id], body=_("Tarea Reabierta"), context=context)
            
        else:
            raise osv.except_osv(_('Acción Inválida!'), _('No puede reabrir la tarea, primero reabra el proyecto.!'))
        return True
        
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['a-draft','f-cancel']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Inválida!'), _('No puede eliminar la tarea.!'))

        return super(crm_task, self).unlink(cr, uid, unlink_ids, context=context)

