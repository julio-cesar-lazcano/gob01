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

class forming_area(osv.Model):
    _name = 'forming.area'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Área", size=200, required=True),
    }

    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)
        unlink_ids = []

        for row in data:
            rows_ids = self.pool.get('courses.ihce').search(cr, uid, [('forming_area','=',row['id'])])
            sup_ids = self.pool.get('suppliers.ihce').search(cr, uid, [('area','=',row['id'])])
            if not rows_ids and not sup_ids:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar un área de formación que está siendo utilizada!'))

        return super(forming_area, self).unlink(cr, uid, unlink_ids, context=context)
