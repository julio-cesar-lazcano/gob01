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

class cancellation_course_wizard(osv.Model):
    _name = "cancellation.course.wizard"
    
    _columns = {
        'instrucctions': fields.text("Instrucciones", readonly=True),
        'cancellation_reason': fields.text('Razón de cancelación', help="Razón por la cual se cancela el curso"),
        'course_id': fields.many2one('date.courses','Curso'),
    }
    
    _defaults = {
        'instrucctions': "INSTRUCCIONES: \n\n \t Se debe agregar una razón por la cual el curso ha sido cancelado, luego preciona el botón Cancelar. \n\n \t Si no deseas cancelar el curso cierra la ventana",
    }
    
    _rec_name = 'cancellation_reason'
    
    
    def action_confirm(self, cr, uid, ids, context=None):
        """
        Metodo para cancelar el proyecto seleccionando algun tipo de cancelacion
        """
        course_obj = self.pool.get('date.courses')
        cancel_wizard_row = self.browse(cr, uid, ids[0], context)
        # Ejecutamos la acction_cancel del projecto
        course_obj.action_cancel(cr, uid, [cancel_wizard_row.course_id.id], cancel_wizard_row.cancellation_reason, context=context)
        
        return {}
