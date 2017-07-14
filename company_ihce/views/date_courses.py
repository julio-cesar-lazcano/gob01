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
import pdb

class date_courses(osv.Model):
    _name = 'date.courses'
    
    def _get_state_mail(self, cr, uid, ids, field, args, context=None):
        res = {}
        
        for row in self.browse(cr, uid, ids, context=context):
            mail_data = self.pool.get('mail.mail').browse(cr, uid, row.mail_id.id, context=context)
            if row.state == 'confirm':
                if mail_data.state == 'sent':
                    #~ se cambia el curso a estado proceso
                    self.write(cr, uid, [row.id], {'state': 'progress'})
                    res[row.id] = True
                else:
                    res[row.id] = False
            else:
                res[row.id] = False
        
        return res
    
    def _get_attendess(self, cr, uid, ids, field, args, context=None):
        res = {}
        con = 0
        for row in self.browse(cr, uid, ids, context=context):
            for line in row.company_invited_line:
                if line.confirm == True:
                    con = con +1 
            
            res[row.id] = con
        
        return res
        
    _columns = {
        'name': fields.char("Tema", size=200, required=True),
        'date': fields.date("Fecha", required=True),
        'courses_id': fields.many2one('courses.ihce', "Curso", required=True),
        'level': fields.many2one('level.knowledge',"Nivel de conocimiento"),
        'supplier_id': fields.many2one('suppliers.ihce', "Consultor", required=True),
        'hours_training': fields.float('Horas de capacitación'),
        'number_attendees': fields.integer("No. asistentes", readonly=True),
        'invited': fields.integer("Invitados", readonly=True),
        'attendees': fields.function(_get_attendess, type="integer", string="Asistencia confirmada"),
        'municipio': fields.many2one('town.hidalgo', "Municipio"),
        'emprered': fields.many2one('emprereds', "Emprered"),
        'responsible_area': fields.many2one('responsible.area',"Área responsable"),
        'services': fields.selection([('formacion', 'Formación de Capital Humano'),('emprendimiento', 'Emprendimiento')], "Servicios", help="Selecciona el rubro en el que contarán tus indicadores (Asistentes, horas de capacitación, curso)."),
        'course_evaluation': fields.selection([('6','Excelente'),('5','Muy bueno'),('4','Bueno'),('3','Regular'),('2','Malo'),('1','Muy malo')], "Evaluación"),
        'notes': fields.text("Comentario de evaluación"),
        'cost': fields.float("Costo del curso", help="Costo total del curso"),
        'federal_contribution': fields.integer("Aportación federal en %"),
        'state_contribution': fields.integer("Aportación estatal en %"),
        'company_contribution': fields.integer("Aportación empresarial en %"),
        'beca': fields.integer("Beca %"),
        'federal_cost': fields.float("Aportación federal $"),
        'state_cost': fields.float("Aportación estatal $"),
        'company_cost': fields.float("Aportación de la empresa $"),
        'beca_cost': fields.float("Beca $"),
        'state': fields.selection([
            ('draft', 'Nuevo'),
            ('confirm', 'Aprobado'),
            ('progress', 'Proceso'),
            ('done', 'Realizado'),
            ('abandoned','Abandonado'),
            ('cancel','Cancelado'),
            ], 'Estado', select=True),
        'all_company': fields.boolean("Agregar a todos los beneficiarios"),
        'line': fields.one2many('company.line', 'course_id', "Linea"),
        'company_invited_line': fields.one2many('company.invited', 'course_id', "Invitados"),
        'dependence': fields.selection([('ihce','IHCE'),('emprered','Emprered')], "Dependencia"),
        'dependence_bool': fields.boolean("Bandera"),
        'type': fields.selection([('curso','Curso'),('taller','Taller'),('seminario','Seminario'),('consultoria','Consultoría'),('platica','Plática'),('diplomado','Diplomado'),('evento','Evento')], "Formato",help="Tipo de curso", required=True),
        'per_level': fields.boolean("Agregar por niveles"),
        'level_add': fields.many2one('level.knowledge',"Nivel de conocimiento"),
        'mail_id': fields.many2one('mail.mail',"Correo"),
        'state_mail': fields.function(_get_state_mail, type="boolean", string="Estado correo"),
        'user_id': fields.many2one('res.users',"Responsable"),
        'img':  fields.text("Url para imagen"),
        'list_new': fields.boolean("Lista de asistentes no registrados"),
        'list_lines': fields.one2many('list.new.persons', 'course_id', "Linea"),
	'image': fields.binary("Imagen de evidencia", help="Seleciona la imagen de evidencia"),
    }
    
    _defaults = {
        'state': 'draft',
        'all_company': False,
        'dependence_bool': False,
        'user_id': lambda obj, cr, uid, context: uid,
        'dependence': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'responsible_area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'list_new': False,
    }
    
    _order = "date desc"
    
    def onchange_course(self, cr, uid, ids, course_id, context=None):
        result = {}
        result['value'] = {}
        if course_id:
            row = self.pool.get('courses.ihce').browse(cr, uid, course_id)
            result['value'].update({'type': row.type})
        
        return result
    
    def onchange_type(self, cr, uid, ids, tipo, context=None):
        res = {'domain': {'courses_id': []}}
        if tipo:
            res['domain'] = {'courses_id': [('type','=',tipo)]}
        
        return res
    
    def onchange_dependence(self, cr, uid, ids, valor, context=None):
        result = {}
        result['value'] = {}
        if valor:
            if valor == 'ihce':
                result['value'].update({'dependence_bool': True})
            else:
                result['value'].update({'dependence_bool': False})
        
        return result

    def create(self, cr, uid, vals, context=None):
        today = datetime.today()
        mes = today.strftime("%m")
        today2=vals.get('date')
        today_now = date(*map(int, today2.split('-')))
        mes2 = today_now.strftime("%m")
        if mes == mes2:
            hola = 'va crear'
            if vals.get('cost') > 0:
                if vals.get('beca') == 0 and vals.get('federal_contribution') == 0 and vals.get('state_contribution') == 0 and vals.get('company_contribution') == 0:
                    raise osv.except_osv(_('Verifique'), _('No se ha indicado el porcentaje de aportaciones.'))
                else:
                    porcentaje = vals.get('federal_contribution') + vals.get('state_contribution') + vals.get('company_contribution')
                    beca = vals.get('beca')
                    if beca == 100:
                        beca_cost = vals.get('cost')
                        vals.update({'beca_cost': beca_cost})
                    else:
                        if porcentaje == 100:
                            federal = float((float(vals.get('federal_contribution')) * float(vals.get('cost'))) / 100)
                            estatal = float((float(vals.get('state_contribution')) * float(vals.get('cost'))) / 100)
                            company = float((float(vals.get('company_contribution')) * float(vals.get('cost'))) / 100)
                            vals.update({'federal_cost': federal, 'state_cost': estatal, 'company_cost': company})
                        else:
                            raise osv.except_osv(_('Verifique'), _('La suma de las aportaciones no suma el 100%'))
        
            return super(date_courses, self).create(cr, uid, vals, context)
      
            
            
        
    def write(self, cr, uid, ids, vals, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        if row.mail_id:
            data = self.pool.get('mail.mail').browse(cr, uid, row.mail_id.id, context=context)
            if data.state == 'sent':
                for li in row.company_invited_line:
                    self.pool.get('company.invited').write(cr, uid, li.id, {'state':'invitado'})
                vals.update({'mail_id': False})
            
        if vals.get('cost') or vals.get('federal_contribution') or vals.get('federal_contribution') == 0 or vals.get('state_contribution') or vals.get('state_contribution') == 0 or vals.get('company_contribution') or vals.get('company_contribution') == 0 or vals.get('beca') or vals.get('beca') == 0:
            row = self.browse(cr, uid, ids[0], context=context)
            costo = vals.get('cost') or row.cost
            federal = vals.get('federal_contribution') or row.federal_contribution
            estatal = vals.get('state_contribution') or row.state_contribution
            company = vals.get('company_contribution') or row.company_contribution
            beca = vals.get('beca') or row.beca
            
            beca = float(beca)
            costo = float(costo)
            federal = float(federal)
            estatal = float(estatal)
            company = float(company)
            
            porcentaje = federal + estatal + company
            
            if beca == 100:
                beca_cost = (beca * costo ) / 100
                vals.update({'beca_cost': beca_cost, 'federal_cost': 0, 'state_cost': 0, 'company_cost': 0, 'cost': costo, 'federal_contribution': 0, 'state_contribution': 0, 'company_contribution': 0})
            else:
                if porcentaje == 100:
                    federal_cost = float((federal * costo ) / 100)
                    estatal_cost = float((estatal * costo ) / 100)
                    company_cost = float((company * costo ) / 100)
                    vals.update({'beca_cost': 0, 'beca': 0, 'federal_cost': federal_cost, 'state_cost': estatal_cost, 'company_cost': company_cost, 'cost': costo, 'federal_contribution': federal, 'state_contribution': estatal, 'company_contribution': company})
                else:
                    raise osv.except_osv(_('Verifique'), _('Las aportaciones del curso no son correctas'))
                    
        return super(date_courses,self).write(cr, uid, ids, vals, context=context)

    def action_cancel(self, cr, uid, ids, reason, context=None):
        self.write(cr, uid, ids, {'state':'cancel', 'notes': reason}, context=context)
        
        return True
    
    def action_cancel_wizard(self, cr, uid, ids, context=None):
        """
        Método para crear el wizard y seleccionar el motivo de abandono
        """

        row = self.browse(cr, uid, ids[0], context=context)
        if row.list_lines or row.line:
            raise osv.except_osv(_('Advertencia'), _('No puede cancelar un curso con asistentes.'))
            return False
        else:
            # Wizard para cancelar el proyecto
            abandoned_course_id = self.pool.get("cancellation.course.wizard").create(cr, uid, {'course_id':ids[0]}, context=context)

            res = {
                'name':("Cancelar Curso"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'cancellation.course.wizard',
                'res_id': abandoned_course_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': context,
            }
            return res
        

    def confirm(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        course = self.pool.get('courses.ihce').browse(cr, uid, row.courses_id.id, context=context)
        self.write(cr, uid, ids, {'state':'confirm', 'level':course.level.id}, context=context)
        
        return True
    
    def return_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'}, context=context)

    def return_progress(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'progress'}, context=context)
    
    def add_company_level(self, cr, uid, ids, context=None):
        con = 0
        row = self.browse(cr, uid, ids[0], context=context)
        company_ids = self.pool.get('companies.ihce').search(cr, uid, [('company','=',True),('state','=','done'),('level_knowledge','=',row.level_add.id)], context=context)
        razon = ""
        for line in self.pool.get('companies.ihce').browse(cr, uid, company_ids, context=context):
            cr.execute("SELECT company_id FROM company_invited WHERE company_id = '"+str(line.id)+"' AND course_id = '"+str(row.id)+"';")
            companies = cr.fetchall()
            if not companies: 
                cr.execute("INSERT INTO company_invited (company_id,course_id,company_name,town,cel_phone,phone,email,level_knowledge,state,idea_commerce) VALUES ('"+str(line.id)+"','"+str(ids[0])+"','"+str(line.name.encode('utf-8'))+"', "+str(line.town.id or '')+", '"+str(line.cel_phone or '')+"', '"+str(line.phone or '')+"', '"+str(line.email.encode('utf-8') or '')+"', "+str(line.level_knowledge.id or '')+",'nuevo', '"+str(line.idea_commerce or '')+"');")
                
        return True
    
    #~ Función que envía correo electronico a todos los contactos de las empresas seleccionadas
    def send_email(self, cr, uid, ids, context=None):
        mail_message_obj = self.pool.get('mail.mail')
        mod_obj = self.pool.get('ir.model.data')
        crm_obj = self.pool.get('crm.ihce')
        user_row = self.pool.get('res.users').browse(cr, uid, uid)
        row = self.browse(cr, uid, ids[0], context)
        fecha_actual = datetime.now()
        con = 0
        con1 = 0
        emails = ''
        email_vals = {}
        
        for company in row.company_invited_line:
            con = con + 1
            data = self.pool.get('companies.ihce').browse(cr, uid, company.company_id.id, context=context)
            if company.state == 'nuevo':
                emails += data.email +","
                #~ Obtenemos los emails de sus contactos
                contact_ids = self.pool.get('companies.ihce').search(cr, uid,[('parent_id','=',company.company_id.id)] , context=context)
                if contact_ids:
                    for contacts in self.pool.get('companies.ihce').browse(cr, uid, contact_ids, context=context):
                        emails += contacts.email +","
                    
                #~ Creamos la línea de actividad en el historial de la compañia
                crm_obj.create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Invitado al curso '+str(row.courses_id.name.encode('utf-8')) +' con el tema ' + str(row.name.encode('utf-8')), 'user':uid, 'date_compromise':fecha_actual, 'state':'done'}, context=context)
        
        emails = emails[:-1] 
        
        if row.invited > 0:
            con1 = row.invited
        else:
            con1 = con

        email_from = user_row.email
        
        if email_from:
            subject = "Invitación al curso "+ str(row.courses_id.name.encode('utf-8'))
            
            if not row.img:
                img = ""
            else:
                img = row.img
                
            body_text = "<p> Se le hace una cordial invitación a participar en el curso de "+ str(row.courses_id.name.encode('utf-8')) +" que se llevará a cabo el " + str(row.date) +".</p> <p>El curso será impartido por " +  str(row.supplier_id.name.encode('utf-8')) + " en un tiempo de " + str(row.hours_training)+ " horas. </p>" + str(img) + " "
            
            email_vals.update({'subject':subject, 'body': body_text, 'body_html': body_text, 'email_to': email_from, 'email_bcc': emails, 'email_from': email_from})

            mail_id = mail_message_obj.create(cr, uid, email_vals )
            self.write(cr, uid, [row.id], {'mail_id': mail_id, 'invited': con}, context=context)
            
            res = mod_obj.get_object_reference(cr, uid, 'mail_ihce', 'mail_compose_message_form_ihce')
            res_id = res and res[1] or False
            
            #~ Se abre la ventana para enviar correo
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
                
        
    #~ Función que finaliza el curso solo si hay asistentes.
    def complete(self, cr, uid, ids, context=None):
        crm_obj = self.pool.get('crm.ihce')
        fecha_actual = datetime.now()
        anio = fecha_actual.year
        row = self.browse(cr, uid, ids, context)[0]
        con = 0
        evaluation = 0
        ban = True
        company_ids = []
        i = 0
        bande = False
        
        #~ Verificamos que haya asistentes no registrados y sobreescribimos la variable de numero de asistentes
        if row.list_lines and not row.line:
            bande = True
            
        for line in row.line:
            con = con + 1
            if line.course_evaluation:
                evaluation += int(line.course_evaluation)
            else:
                ban = False
                raise osv.except_osv(_('Advertencia!'), _('No se ha ingresado evaluación de todos los asistentes!'))
                break 
            
        for line in row.list_lines:
            con = con + 1
            if line.course_evaluation:
                evaluation += int(line.course_evaluation)
            else:
                ban = False
                raise osv.except_osv(_('Advertencia!'), _('No se ha ingresado evaluación de todos los asistentes!'))
                break 
        
        if con > 0 and ban:
            evaluation = round(evaluation / con)
            evaluation = int(evaluation)
                
            self.write(cr, uid, [row.id], {'number_attendees': con, 'state':'done', 'course_evaluation': str(evaluation)}, context=context)

            if not bande:
                for line in row.line:
                    #~ Creamos la línea de actividad en el historial de la compañia
                    self.pool.get('company.line').write(cr, uid, [line.id], {'courses_id': row.courses_id.id, 'date':row.date, 'type':row.type})
                    li = self.pool.get('company.line').browse(cr, uid, line.id, context=context)
                    
                    if i == 0:
                        company_ids.append(li.company_id.id)
                        crm_obj.create(cr, uid, {'company_id': li.company_id.id, 'date':fecha_actual, 'name':'Asistió al curso '+str(row.courses_id.name.encode('utf-8')) + " con el tema "+ str(row.name.encode('utf-8')) +" el "+str(row.date), 'user':uid, 'date_compromise':row.date, 'state':'done'}, context=context)
                    else:
                        ban = True
                        for a in company_ids:
                            if a == li.company_id.id:
                                ban = False
                                break
                        if ban:
                            company_ids.append(li.company_id.id)
                            crm_obj.create(cr, uid, {'company_id': li.company_id.id, 'date':fecha_actual, 'name':'Asistió al curso '+str(row.courses_id.name.encode('utf-8')) + " con el tema "+ str(row.name.encode('utf-8')) +" el "+str(row.date), 'user':uid, 'date_compromise':row.date, 'state':'done'}, context=context)
                    i = i +1
        else:
            raise osv.except_osv(_('Advertencia!'), _('El curso no puede ser finalizado, no hay asistentes.!'))
        
        return True
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            if row['state'] in ['draft','cancel']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar un curso que está en proceso!'))

        return super(date_courses, self).unlink(cr, uid, unlink_ids, context=context)
    
    
class companies_ihce(osv.Model):
    _inherit = 'companies.ihce'

    _columns = {
        'company_course': fields.one2many('company.line', 'company_id', "Relacion cursos"),
    }
    
class company_line(osv.Model):
    _name = 'company.line'

    _columns = {
        'contact_id': fields.many2one('companies.ihce', "Participante"),
        'company_id': fields.many2one('companies.ihce', "Beneficiario"),
        'courses_id': fields.many2one('courses.ihce', "Curso"),
        'course_id': fields.many2one('date.courses', 'Módulo'),
        'name_company': fields.char('Razón social/Negocio', size=200),
        'town': fields.many2one('town.hidalgo',"Municipio"),
        'cel_phone': fields.char("Teléfono móvil", size=30),
        'phone': fields.char("Teléfono fijo", size=15),
        'email': fields.char("Correo electrónico", size=100),
        'idea_commerce': fields.char('Idea de Negocio', size=250),
        'date': fields.date("Fecha de curso"),
        'course_evaluation': fields.selection([('6','Excelente'),('5','Muy bueno'),('4','Bueno'),('3','Regular'),('2','Malo'),('1','Muy malo')], "Evaluación"),
        'type': fields.selection([('curso','Curso'),('taller','Taller'),('seminario','Seminario'),('consultoria','Consultoría'),('platica','Plática'),('diplomado','Diplomado'),('evento','Evento')], "Formato", help="Tipo de curso"),
    }
    
    _rec_name = 'contact_id'
    
    def write(self, cr, uid, ids, values, context=None):
        return super(company_line,self).write(cr, uid, ids, values, context=context)
    
    def onchange_company(self, cr, uid, ids, contact, context=None):
        result = {}
        result['value'] = {}
        if contact:
            row = self.pool.get('companies.ihce').browse(cr, uid, contact, context=context)
            data = self.pool.get('companies.ihce').browse(cr, uid, row.parent_id.id, context=context)

            if data.type == 'moral':
                razon = data.company_name
            else:
                razon = data.name
            
            result['value'].update({'name_company': razon, 'town':row.town , 'phone': row.phone, 'cel_phone': row.cel_phone, 'email': row.email,'company_id': row.parent_id.id,'idea_commerce': row.idea_commerce})
        
        return result


class company_invited(osv.Model):
    _name = 'company.invited'

    _columns = {
        'company_id': fields.many2one('companies.ihce', "Beneficiario"),
        'course_id': fields.many2one('date.courses', 'Módulo'),
        'company_name': fields.char('Razón social/Negocio', size=200),
        'town': fields.many2one('town.hidalgo',"Municipio"),
        'cel_phone': fields.char("Teléfono móvil", size=30),
        'phone': fields.char("Teléfono fijo", size=15),
        'email': fields.char("Correo electrónico", size=100),
        'level_knowledge': fields.many2one('level.knowledge',"Nivel de conocimiento"),
        'idea_commerce': fields.char('Idea de Negocio', size=250),
        'confirm': fields.boolean("Confirma asistencia"),
        'state': fields.selection([('nuevo','Nuevo'),('invitado','Invitado')], "Status"),
    }
    
    _rec_name = 'company_id'
    
    _defaults  = {
        'state': 'nuevo',
    }
    
    def write(self, cr, uid, ids, values, context=None):
        return super(company_invited,self).write(cr, uid, ids, values, context=context)
    
    def onchange_company_in(self, cr, uid, ids, company, context=None):
        result = {}
        result['value'] = {}
        if company:
            row = self.pool.get('companies.ihce').browse(cr, uid, company, context=context)

            if row.type == 'moral':
                razon = row.company_name
            else:
                razon = row.name
            
            result['value'].update({'company_name': razon, 'town':row.town , 'phone': row.phone, 'cel_phone': row.cel_phone, 'email': row.email, 'level_knowledge': row.level_knowledge, 'idea_commerce': row.idea_commerce})
        
        return result


class list_new_persons(osv.Model):
    _name = 'list.new.persons'

    _columns = {
        'course_id': fields.many2one('date.courses', 'Módulo'),
        'name': fields.char('Nombre Completo/Nombre Comercial', size=200),
        'sexo': fields.selection([('F','Femenino'),('M','Masculino')], "Sexo"),
        'town': fields.many2one('town.hidalgo',"Municipio"),
        'cel_phone': fields.char("Teléfono móvil", size=30),
        'phone': fields.char("Teléfono fijo", size=15),
        'email': fields.char("Correo electrónico", size=100),
        'idea_commerce': fields.char('Idea de Negocio', size=250),
        'course_evaluation': fields.selection([('6','Excelente'),('5','Muy bueno'),('4','Bueno'),('3','Regular'),('2','Malo'),('1','Muy malo')], "Evaluación"),
    }
