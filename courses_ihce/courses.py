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

class courses_ihce(osv.Model):
    _name = 'courses.ihce'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _get_modules(self, cr, uid, ids, field, arg, context=None):
        res = {}

        for row in self.browse(cr, uid, ids, context=context):
            cr.execute("SELECT id FROM date_courses WHERE courses_id = '"+str(row.id)+"' AND state = 'done';")
            courses = cr.fetchall()
            if len(courses) >= row.modules:
                res[row.id] = True
            else:
                res[row.id] = False
        return res
        
    _columns = {
        'name': fields.char("Nombre", size=200, required=True),
        'type': fields.selection([('curso','Curso'),('taller','Taller'),('seminario','Seminario'),('consultoria','Consultoría'),('platica','Plática'),('diplomado','Diplomado'),('evento','Evento')], "Formato",help="Tipo de curso", required=True),
        'forming_area': fields.many2one('forming.area',"Área de formación", required=True),
        'supplier_id': fields.many2many('suppliers.ihce','supplier_courses_rel', 'courses_id', 'supplier_id', "Proveedores"),
        'objective': fields.text("Objetivo"),
        'agenda': fields.text("Temario"),
        'level': fields.many2one('level.knowledge', "Nivel del curso", required=True),
        'date_course': fields.one2many('date.courses','courses_id', "Fecha de curso"),
        'modules': fields.integer("Módulos del curso"),
        'state_cours': fields.function(_get_modules, type='boolean', string="Estado del curso"),
    }
    
    _order = "name asc"

    def create(self, cr, uid, vals, context=None):
        if vals.get('modules') <= 0:
            raise osv.except_osv(_('Acción Invalida!'), _('El curso debe tener al menos un módulo!'))
        return super(courses_ihce, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('modules') != None:
            if vals.get('modules') <= 0:
                raise osv.except_osv(_('Acción Invalida!'), _('El curso debe tener al menos un módulo!'))
        
        return super(courses_ihce,self).write(cr, uid, ids, vals, context=context)
        
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['date_course'], context=context)
        unlink_ids = []
        for row in data:
            if not row['date_course']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar un curso que está en proceso!'))

        return super(courses_ihce, self).unlink(cr, uid, unlink_ids, context=context)
