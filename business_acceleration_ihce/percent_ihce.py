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
import time

class percent_acceleration(osv.Model):
    _name = 'percent.acceleration'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Nombre"),
        'description': fields.char("Descripción"),
        'date': fields.date("Fecha"),
        'adiagnostic_percent': fields.integer("Diagnóstico"),
        'training_percent': fields.integer("Capacitación"),
        #~ 'construction_manuals_percent': fields.integer("Construcción de manuales"),
        'implemetation_percent': fields.integer("Implemetaciones"),
        'cross_audit_percent': fields.integer("Auditoría cruzada"),
        'acceptation_audit_percent': fields.integer("Aceptación Pre-Auditoría"),
        'audit_percent': fields.integer("Auditoría"),
        'certificate_percent': fields.integer("Certificado"),
    }

    _defaults = {
        'name': "Ingrese el procentaje que desea asignar a cada etapa.",
        'description': "Porcentajes asignados a cada etapa de los servicios de Aceleración Empresarial",
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    def create(self, cr, uid, vals, context=None):
        return super(percent_acceleration, self).create(cr, uid, vals, context)
        
    def write(self, cr, uid, ids, vals, context=None):
        super(percent_acceleration,self).write(cr, uid, ids, vals, context=context)
        self.check_percent(cr, uid, ids, context=context)
        return True

    def check_percent(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        percent = row.adiagnostic_percent + row.training_percent + row.implemetation_percent + row.cross_audit_percent + row.acceptation_audit_percent + row.audit_percent + row.certificate_percent
        if percent != 100: 
            raise osv.except_osv(_('Verifique'), _('La suma de los percentajes no es el 100%'))
        
        return True
