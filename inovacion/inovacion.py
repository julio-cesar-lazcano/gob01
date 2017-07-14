# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


######################################################################

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from datetime import datetime, date, timedelta
import time

class inovacion_ihce(osv.Model):
    _name = 'inovacion.ihce'

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