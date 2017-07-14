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

class app_laboratory(osv.Model):
    _name = 'app.laboratory'
    
    _columns = {
        'name': fields.char("Aplicación", size=200),
    }

class laboratory_ihce(osv.Model):
    _name = 'laboratory.ihce'
    
    def _get_percent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for rows in self.browse(cr, uid, ids, context=context):
            percent = 0
            suma = 0
            con = 0
            for row in rows:
                for line in row.lines_services:
                    if line.state != 'detained':
                        suma += line.percent
                        con = con + 1
                    
                if suma > 0:
                    percent = suma / con
                res[row.id] = percent
            
        return res
    
    def _get_services(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for rows in self.browse(cr, uid, ids, context=context):
            suma = 0
            for row in rows:
                for line in row.lines_services:
                    if line.state == 'pre_done' or line.state == 'done':
                        suma = suma + 1
                res[row.id] = suma
            
        return res
    
    def _get_advices(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for rows in self.browse(cr, uid, ids, context=context):
            suma = 0
            for row in rows:
                res[row.id] = len(row.lines_advices)
            
        return res
    
    def _get_state(self, cr, uid, ids, field, arg, context=None):
        res = {}
        
        for rows in self.browse(cr, uid, ids, context=context):
            done = False
            detained = False
            pro = False
            for row in rows:
                if row.state == 'process':
                    for line in row.lines_services:
                        if line.state == 'pre_done' or line.state == 'done':
                            done = True
                        elif line.state == 'detained':
                            detained = True
                        else:
                            pro = True
                            
                    if done and not detained and not pro: 
                        #~ Si todos los servicios estan terminados cambiamos el estado y enviamos la encuesta
                        self.send_test(cr, uid, ids, context=context)
                        res[row.id] = True
                    else:
                        if done and detained and not pro: 
                            #~ Si todos los servicios estan terminados cambiamos el estado y enviamos la encuesta
                            self.send_test(cr, uid, ids, context=context)
                            res[row.id] = True
                        else:
                            if (done and detained and pro) or (pro and done) or (detained and pro) or pro: 
                                self.write(cr, uid, row.id, {'state': 'process'})
                                res[row.id] = False
                            else:
                                if not done and not pro and detained:
                                    self.write(cr, uid, row.id, {'state': 'detained'})
            
        return res
        
        
    _columns = {
        'name': fields.char("ID de Proyecto", size=200),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'date': fields.datetime("Fecha de inicio"),
        'percent': fields.function(_get_percent, type='integer', string="Porcentaje de avance"),
        'notes': fields.text("Observación General"),
        'state': fields.selection([('process', 'Proceso'),('stand', 'Encuesta Enviada'),('done', 'Terminado'),('detained','Abandonado')], 'Estado', select=True),
        'servicio': fields.function(_get_services, type='integer', string="No. Servicios"),
        'advices': fields.function(_get_advices, type='integer', string="No. Asesorías"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'lines_services': fields.one2many('desing.laboratory', 'id_project', 'Servicios'),
        'lines_advices': fields.one2many('advices.laboratory', 'laboratory', 'Asesorías'),
        'url_test': fields.char("Url de Encuesta", size=200),
        'test': fields.one2many('test.laboratory', 'laboratory', "Encuesta de Satisfacción"),
        'state_done': fields.function(_get_state, type='boolean', string="Estado del proyecto"),
        'tests_bol': fields.boolean("Encuestas"),
        'sector': fields.many2one('sector.actividad.economica',"Sector",help="Sector económico"),
    }
    
    _defaults = {
        'state': 'process',
        'percent': 0,
        'user_id': lambda obj, cr, uid, context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'tests_bol': False,
    }
    
    _order = "name desc"
    
    def create(self, cr, uid, vals, context=None):
        return super(laboratory_ihce, self).create(cr, uid, vals, context)
        
    def write(self, cr, uid, ids, vals, context=None):
        return super(laboratory_ihce,self).write(cr, uid, ids, vals, context=context)
        
    #~ Función para enviar correo con la liga de encuesta de satisfacción
    def send_test(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        email_vals = {}
        row = self.browse(cr, uid, ids[0], context=context)
        
        mail_message_obj = self.pool.get('mail.mail')
        user_row = self.pool.get('res.users').browse(cr, uid, row.user_id.id)
        companies = self.pool.get('companies.ihce').browse(cr, uid, row.company_id.id, context=context)
        
        url = "http://192.241.169.197/encuesta/index.php?&token=" + str(row.id)
        self.write(cr, uid, row.id, {'url_test': url, 'state': 'done'}, context=context)
        
        if user_row.email:
            subject = "ENCUESTA DE SATISFACCIÓN LABORATORIO DE DISEÑO"
            
            body_text = "Estimado "+ str(companies.name.encode('utf-8')) + "</br></br><p>Para brindarte un mejor servicio el Laboratorio de Diseño te envita a contestar la siguiente encuesta de satisfacción.</p> <p></br></br>"+ str(url) + "</p> </br></br> <p>Gracias.</p>"

            email_vals.update({'subject': subject, 'body_html': body_text, 'body': body_text, 'email_to': companies.email, 'email_from': user_row.email})
            mail_id = mail_message_obj.create(cr, uid, email_vals )
            mail_message_obj.send(cr, uid, [mail_id], False, None, context=context)
            
            #~ Linea de historial del beneficiario
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'Se ha enviado encuesta de satisfacción al beneficiario del proyecto ' + str(row.name.encode('utf-8')) + " del laboratorio de diseño.", 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
            #~ self.message_post(cr, uid, [row.id], body=_("Encuesta Enviada"), context=context)
            
        else:
            raise osv.except_osv(_('Advertencia!'), _('El usuario no tiene correo electrónico!'))
        
        return True
        


class desing_laboratory(osv.Model):
    _name = 'desing.laboratory'
    
    def _get_date_new(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context=context):
            if row.state == 'out_time':
                if row.return_date2:
                    self.write(cr, uid, row.id, {'state':'process'})
            
        return res

    _columns = {
        'name': fields.char("Nombre"),
        'service': fields.many2one('services.laboratory', 'Servicio'),
        'app': fields.many2one('app.laboratory', 'Aplicación'),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'id_project': fields.many2one('laboratory.ihce',"ID de Proyecto"),
        'date': fields.datetime("Fecha de inicio"),
        'date_fin': fields.datetime("Fecha de termino"),
        'date_next': fields.datetime("Fecha de próxima cita"),
        'percent': fields.integer("Porcentaje de avance"),
        'notes': fields.text("Observación General"),
        'state': fields.selection([
            ('draft', 'Nuevo'),
            ('process', 'Proceso'),
            ('out_time', 'Fuera de tiempo'),
            ('pre_done', 'Para Terminar'),
            ('done', 'Terminado'),
            ('detained','Abandonado'),
            ], 'Estado', select=True),
        'servicio': fields.integer("Servicio"),
        'asesoria': fields.integer("Asesoría"),
        'crm_id': fields.many2one('crm.project.ihce',"Proyecto crm"),
        'task_id': fields.integer("Tarea crm"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'binnacle_lines': fields.one2many('binnacle.laboratory', 'service', 'Bitácora de trabajo'),
        'cron_id': fields.many2one('ir.cron', "Tarea en proceso"),
        'return_date': fields.function(_get_date_new, type='boolean', string="Fecha cambiada"),
        'return_date2': fields.boolean("Fecha cambiada"),
        'option_service': fields.selection([('0', 'Servicio'), ('1', 'Aplicación')], 'Opción'),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
        'sector': fields.many2one('sector.actividad.economica',"Sector",help="Sector económico"),
    }
    
    _defaults = {
        'state': 'draft',
        'percent': 0,
        'return_date2': False,
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
    }
    
    _order = "date_next asc"
    
    def create(self, cr, uid, vals, context=None):
        name = ''
        # Generamos id consecutivo, verificamos que el beneficiario no tenga id aún
        row = self.pool.get('companies.ihce').browse(cr, uid, vals.get('company_id'), context=context)
        new_seq = ""
        if not row.id_project_laboratory:
            new_seq = self.pool.get('ir.sequence').get(cr, uid, 'sector.laboratorio')
            
            #~ Guardamos el numero de proyecto al beneficiario
            id_project = self.pool.get('laboratory.ihce').create(cr, uid, {'name': new_seq, 'company_id': vals.get('company_id'), 'user_id': vals.get('user_id'), 'sector': row.sector.id})
            self.pool.get('companies.ihce').write(cr, uid, row.id, {'id_project_laboratory': id_project})
            vals.update({'id_project': id_project})
        else:
            vals.update({'id_project': row.id_project_laboratory.id})
            self.pool.get('laboratory.ihce').write(cr, uid, vals.get('id_project'), {'state': 'process'})
        
        if vals.get('option_service') == '0':
            servi = self.pool.get('services.laboratory').browse(cr, uid, vals.get('service'), context=context)
            name = servi.name
        else:
            if vals.get('option_service') == '1':
                app = self.pool.get('app.laboratory').browse(cr, uid, vals.get('app'), context=context)
                name = app.name
        
        vals.update({'name': name, 'sector': row.sector.id})
        
        return super(desing_laboratory, self).create(cr, uid, vals, context)
        
    def write(self, cr, uid, ids, vals, context=None):
        return super(desing_laboratory,self).write(cr, uid, ids, vals, context=context)
    
    def _check_laboratory(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_ejecucion = datetime.now()
        if row.date_next:
            fecha_compromiso = datetime.strptime(row.date_next, "%Y-%m-%d %H:%M:%S")
        
            if row.state == 'process':
                if row.date_next:
                    if fecha_compromiso < fecha_ejecucion:
                        self.write(cr, uid, ids[0], {'state': 'out_time', 'return_date2': False}, context=context)
                        #~ Apartir del momento en que se encuentra fuera de tiempo, tiene 10 días para reagendar o para que se presente el beneficiario, pasado este tiempo el servicio se pondrá en estado detenido.
                        fecha_detenido = fecha_ejecucion + timedelta(days=14)
                        #~ Linea de historial del beneficiario
                        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_ejecucion, 'name':'El servicio de ' + str(row.service.name.encode('utf-8')) + " del laboratorio de diseño se encuentra fuera de tiempo. No se realizó cita en la fecha establecida.", 'user':uid, 'date_compromise': fecha_ejecucion, 'state':'done'}, context=context)
                        
                        #~ self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state': 'c-out_time'})
                        
                        #~ Enviar correo que el tiempo de la tarea se terminó
                        titulo = "Aviso CRM"
                        texto = "<p>El tiempo para el servicio "+str(row.service.name.encode('utf-8'))+ " del beneficiario " + str(row.company_id.name.encode('utf-8')) + " con número " + str(row.id_project) + " está fuera de tiempo. Requerie se agende nueva fecha para cita.</p> "
                        self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, row.user_id.id, context=context)
                        
            if row.state == 'out_time':
                if fecha_detenido == fecha_ejecucion:
                    self.write(cr, uid, ids[0], {'state': 'detained'}, context=context)
                    #~ Linea de historial del beneficiario
                    self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_ejecucion, 'name':'El servicio de ' + str(row.service.name.encode('utf-8')) + " del laboratorio de diseño se encuentra detenido. No se realizó cita en la fecha establecida.", 'user':uid, 'date_compromise': fecha_ejecucion, 'state':'done'}, context=context)
                    
                    #~ self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state': 'e-abandoned'})
                    
                    #~ Enviar correo que el tiempo de la tarea se terminó, el servicio pasa a detenido
                    titulo = "Aviso CRM"
                    texto = "<p>El tiempo para el servicio "+str(row.name.encode('utf-8'))+ " del beneficiario " +row.company_id.name.encode('utf-8') + " con número " + row.id_project + " está fuera de tiempo. El servicio pasa a estado DETENIDO, ya que se le dieron 10 días de plazo después de la última cita.</p> "
                    self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, row.user_id.id, context=context)
                
        return True
        
    def start_process(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now()
        
        res = {
            'name':'Process : ' + row.id_project.name,
            'model':'desing.laboratory',
            'args': repr([ids]), 
            'function':'_check_laboratory',
            'priority':5,
            'interval_number':1,
            'interval_type':'hours',
            'user_id':uid,
            'numbercall':-1,
            'doall':False,
            'active':True
        }
        
        id_cron = self.pool.get('ir.cron').create(cr, uid, res)
        
        if row.option_service == '0':
            servi = row.service.name.encode('utf-8')
        else:
            servi = row.app.name.encode('utf-8')
        
        #~ Linea de historial del beneficiario
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'Se ha iniciado el servicio de ' + str(servi) + " del laboratorio de diseño.", 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        #~ Al aprobarse el registro se crea un proyecto en el crm del usuario.
        valores = {
            'name': servi + " " + str(row.id_project.name),
            'company_id': row.company_id.id,
            'state': 'a-draft',
            'type_crm': 'automatico',
        }
        crm_id = self.pool.get('crm.project.ihce').create(cr, uid, valores, context=context)
        self.pool.get('crm.project.ihce').comenzar(cr, uid, [crm_id], context=context)
        
        self.write(cr, uid, ids[0], {'cron_id': id_cron, 'state': 'process', 'date': fecha_actual, 'crm_id': crm_id}, context=context)
        
        #~ self.message_post(cr, uid, [row.id], body=_("Servicio Iniciado"), context=context)
    
    def onchange_date_next(self, cr, uid, ids, fecha, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
    
        if fecha:
            fecha_next = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
            
            #~ if fecha_next < fecha_actual:
                #~ raise osv.except_osv(_('Advertencia!'), _('La fecha de la próxima cita debe ser posterior al día de hoy!'))
                #~ return False
            #~ else:
            result['value'].update({'date_next': fecha, 'return_date2': True})
            
            #~ self.message_post(cr, uid, ids, body=_("Cita Reprogramada"), context=context)
        
        return result
        
        
    def detained_process(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        self.write(cr, uid, ids[0], {'state': 'detained'}, context=context)
        self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state': 'e-abandoned'})
        #~ Linea de historial del beneficiario
        if row.option_service == '0':
            servi = row.service.name.encode('utf-8')
        else:
            servi = row.app.name.encode('utf-8')
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de ' + str(servi) + " del laboratorio de diseño ha sido detenido/abandonado.", 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        #~ self.message_post(cr, uid, [row.id], body=_("Servicio Detenido"), context=context)
        
        return True
        
    def action_detained_wizard(self, cr, uid, ids, context=None):
        """
        Método para crear el wizard y seleccionar el motivo de la cancelación
        """
        # Wizard para cancelar el proyecto
        cancel_project_id = self.pool.get("detained.services").create(cr, uid, {'service_id':ids[0]}, context=context)

        res = {
            'name':("Abandonar Servicio"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'detained.services',
            'res_id': cancel_project_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': context,
        }
        return res
    
    def refresh_process(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        self.write(cr, uid, ids[0], {'state': 'process', 'return_date2': False}, context=context)
        self.pool.get('crm.project.ihce').write(cr, uid, [row.crm_id.id], {'state': 'b-progress'})
        #~ Linea de historial del beneficiario
        if row.option_service == '0':
            servi = row.service.name.encode('utf-8')
        else:
            servi = row.app.name.encode('utf-8')
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de ' + str(servi) + " del laboratorio de diseño ha sido reabierto.", 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        #~ self.message_post(cr, uid, [row.id], body=_("Servicio Reabierto"), context=context)
        
        return True
        
    def done_process(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        row = self.browse(cr, uid, ids[0], context=context)
        self.write(cr, uid, ids[0], {'state': 'done'}, context=context)
        self.pool.get('crm.project.ihce').write(cr, SUPERUSER_ID, [row.crm_id.id], {'state': 'd-done'})
        #~ Linea de historial del beneficiario
        if row.option_service == '0':
            servi = row.service.name.encode('utf-8')
        else:
            servi = row.app.name.encode('utf-8')
        
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El servicio de ' + str(servi) + " del laboratorio de diseño ha sido concluido.", 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        #~ self.message_post(cr, uid, [row.id], body=_("Servicio Terminado"), context=context)
        
        return True
    
    def onchange_company(self, cr, uid, ids, company, user, service, app, context=None):
        result = {}
        result['value'] = {}
    
        if user:
            us = self.pool.get('res.users').browse(cr, uid, user)
        if company:
            if service:
                services_ids = self.search(cr, uid, [('company_id','=',company),('service','=',service)])
                if services_ids:
                    raise osv.except_osv(_('Advertencia!'), _('Ya existe un servicio para la empresa seleccionada, que ha creado el usuario '+ str(us.name.encode('utf-8'))+'. Por favor verifique si es necesario crear otro!'))
            if app:
                app_ids = self.search(cr, uid, [('company_id','=',company),('app','=',app)])
                if app_ids:
                    raise osv.except_osv(_('Advertencia!'), _('Ya existe una aplicación para la empresa seleccionada, que ha creado el usuario '+ str(us.name.encode('utf-8')) +'.  Por favor verifique si es necesario crear otra!'))
        
        return result
        
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['draft']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar el servicio/aplicación.!'))

        return super(desing_laboratory, self).unlink(cr, uid, unlink_ids, context=context)

    
    def onchange_user(self, cr, uid, ids, user_id, context=None):
        result = {}
        result['value'] = {}
        
        if user_id:
            row = self.pool.get('res.users').browse(cr, uid, user_id)
            
            result['value'].update({'option': row.option, 'area': row.area.id, 'emprered': row.emprered.id})
        
        return result

        
        
class binnacle_laboratory(osv.Model):
    _name = 'binnacle.laboratory'
    
    _columns = {
        'name': fields.char("Actividad", size=200),
        'id_project': fields.many2one('laboratory.ihce',"ID de Proyecto"),
        'service': fields.many2one('desing.laboratory', 'Servicio'),
        'date': fields.datetime("Fecha"),
        'date_next': fields.datetime("Próxima cita"),
        'notes': fields.text("Comentarios/Acuerdos"),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'percent': fields.integer("Porcentaje de avance"),
        'state': fields.selection([
            ('draft', 'Nuevo'),
            ('done', 'Terminado'),
            ], 'Estado'),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'draft',
    }
    
    
    
    def create(self, cr, uid, vals, context=None):
        fecha_actual = datetime.now()
        row = self.pool.get('desing.laboratory').browse(cr, uid, vals.get('service'))
        vals.update({'id_project': row.id_project.id})
        if vals.get('percent') >= 0 and vals.get('percent') <= 100:
            #~ Creamos la tarea en el crm
            
            notas = vals.get('notes')
            if notas:
                notas = notas.encode('utf-8')
            else:
                notas = ""
            
            if vals.get('percent') == 100:
                if row.task_id != 0:
                    self.pool.get('crm.task').terminar(cr, SUPERUSER_ID, [row.task_id], context=context)
                    
                self.pool.get('desing.laboratory').write(cr, uid, vals.get('service'), {'percent': vals.get('percent'), 'date_next': False, 'state': 'pre_done', 'date_fin': fecha_actual})
            else:
                if row.task_id != 0:
                    self.pool.get('crm.task').terminar(cr, SUPERUSER_ID, [row.task_id], context=context)
                
                datos = {
                    'name': vals.get('name').encode('utf-8'),
                    'date_compromise': vals.get('date_next'),
                    'user_id': uid,
                    'crm_id': row.crm_id.id,
                    'notes': notas,
                    'type_task': 'automatico',
                }
                task_id = self.pool.get('crm.task').create(cr, SUPERUSER_ID, datos, context=context)
                    
                self.pool.get('desing.laboratory').write(cr, uid, vals.get('service'), {'percent': vals.get('percent'), 'date_next': vals.get('date_next'), 'task_id': task_id, 'state': 'process'})
            
            vals.update({'state': 'done'})
            
            #~ Linea de historial del beneficiario
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name': str(vals.get('name').encode('utf-8')) + " para el servicio de " + str(row.name.encode('utf-8')) + " del laboratorio de diseño. " + notas, 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        else:
            raise osv.except_osv(_('Advertencia!'), _('El porcentaje ingresado no se encuentra dentro del rango correcto.!'))
            return False

        return super(binnacle_laboratory, self).create(cr, uid, vals, context)


class companies_ihce(osv.Model):
    _inherit = 'companies.ihce'
    
    _columns = {
        'id_project_laboratory': fields.many2one('laboratory.ihce', "ID de Proyecto Laboratorio"),
        'laboratory_lines': fields.one2many('desing.laboratory', 'company_id', "Servicios de Laboratorio"),
    }

class services_lab_lines(osv.Model):
    _inherit = 'services.lab.lines'
    
    def open_service(self, cr, uid, ids, context=None):

        return {
            'name': "",
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'desing.laboratory',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'context': context,
            'target': 'current',
        }
    
    
    
class test_laboratory(osv.Model):
    _name = 'test.laboratory'
    
    _columns = {
        'name': fields.char("Nombre", size=200),
        'date': fields.date("Fecha"),
        'rfc': fields.char("RFC", size=20),
        'laboratory': fields.many2one('laboratory.ihce', "Servicio"),
        'question1': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '1.- La persona que lo atendió se mostró dispuesto a ayudarlo y a resolver sus dudas.'),
        'question2': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '2.- La persona que lo atendió se mostró siempre en un trato respetuoso y atento a sus comentarios.'),
        'question3': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '3.- La persona que lo atendió cumplió las citas agendadas para la revisión de los avances.'),
        'question4': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '1.- El servicio proporcionado cumplió con sus expectativas.'),
        'question5': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '2.- El servicio proporcionado se cumplió en los tiempos establecidos.'),
        'question6': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '3.- El servicio proporcionado se prestó siempre de forma profesional.'),
        'question7': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '4.- El material entregado cumplió con sus necesidades.'),
        'question8': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '1.- Las instalaciones, equipo y software son los necesarios para cubrir sus necesidades.'),
        'question9': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '2.- El servicio de prototipado 3D cumplió con sus expectativas.'),
        'question10': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '3.- El servicio de impresión cumplió con sus expectativas.'),
        'question11': fields.selection([('Excelente', 'Excelente'),('Bueno', 'Bueno'),('Regular', 'Regular'),('Deficiente', 'Deficiente'),('MuyDeficiente', 'Muy Deficiente'),('NoAplica', 'No Aplica')], '4.- El servicio de fotografía de producto cumplió con sus expectativas.'),
        'comments': fields.text("Comentarios"),
        'recommendation': fields.text("Recomendaciones"),
    }
    
class advices_laboratory(osv.Model):
    _name = 'advices.laboratory'
    
    _columns = {
        'name': fields.text("Nota", size=200),
        'date': fields.date("Fecha"),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'laboratory': fields.many2one('laboratory.ihce', "Proyecto"),
        'option': fields.selection([('0','Servicio'),('1','Aplicación')],"Opción.."),
        'service': fields.many2one('services.laboratory', 'Servicio'),
        'app': fields.many2one('app.laboratory', 'Aplicación'),
        'user_id': fields.many2one('res.users',"Responsable",help="Es el usuario al que se le contarán los indicadores."),
        'option_dep': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'option_dep': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
    }
    
    _order = "date desc"
    
    def onchange_company(self, cr, uid, ids, valor, context=None):
        result = {}
        result['value'] = {}
        
        if valor:
            row = self.pool.get('companies.ihce').browse(cr, uid, valor, context=context)
        
            result['value'].update({'laboratory': row.id_project_laboratory.id})
            
        return result
        
    def onchange_project(self, cr, uid, ids, valor, context=None):
        result = {}
        result['value'] = {}
        
        if valor:
            rows = self.pool.get('companies.ihce').search(cr, uid, [('id_project_laboratory','=',valor)], context=context)
            row = self.pool.get('companies.ihce').browse(cr, uid, rows[0], context=context)
            result['value'].update({'company_id': row.id})
            
        return result
    

