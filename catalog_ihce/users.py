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

from openerp import SUPERUSER_ID
from datetime import date
from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_users(osv.Model):
    _inherit = "res.users"
    
    _columns = {
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina', select=True),
        'area': fields.many2one('responsible.area', 'Área ihce', select=True),
        'emprered': fields.many2one('emprereds', 'Emprered', select=True),
        'email_crm': fields.boolean('Recibir notificaciones CRM'),
        #~ 'state_id': fields.many2one('states.mexico', "Estado"),
        #~ 'town_id': fields.many2one('town.hidalgo', "Municipio"),
    }
    
    #~ def onchange_area(self, cr, uid, ids, area, context=None):
        #~ result = {}
        #~ result['value'] = {}
    #~ 
        #~ if area:
	    #~ print ""
            #~ result['value'].update({'town_id': 48})
        #~ 
        #~ return result
    #~ 
    #~ def onchange_emprered(self, cr, uid, ids, emprered, context=None):
        #~ result = {}
        #~ result['value'] = {}
    #~ 
        #~ if emprered:
            #~ row = self.pool.get('emprereds').browse(cr, uid, emprered)
            #~ result['value'].update({'town_id': row.town_id.id})
        #~ 
        #~ return result
    
    _defaults = {
        'email_crm': False,
    }
