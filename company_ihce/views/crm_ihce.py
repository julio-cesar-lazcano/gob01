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
import datetime
from datetime import date,timedelta
import time
from time import strptime

class crm_ihce(osv.Model):
    _name = 'crm.ihce'
    
    _columns = {
        'company_id': fields.many2one('companies.ihce', "Beneficiario"),
        'date': fields.datetime("Fecha"),
        'name': fields.text("Actividad"),
        'call': fields.boolean("Llamada"),
        'meeting': fields.boolean("Reunión"),
        'user': fields.many2one('res.users',"Usuario"),
        'date_compromise': fields.datetime("Fecha compromiso"),
        'state': fields.selection([('draft','Borrador'),('progress','Proceso'),('done','Terminado'),('cancel','Cancelado')], "Estado"),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
    }
    
    _defaults = {
        #~ 'user': lambda obj, cr, uid, context: uid,
        'state': 'draft',
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
    }

    _order = "date desc"
    
    #~ Cambia el estado de la actividad de borrador a proceso
    def comenzar(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'progress'})
        
        return True
    
    #~ Cambia el estado de la actividad de proceso a realizado o terminad
    def terminar(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done'})
        
        return True
    
    #~ Cambia el estado de la actividad a cancelado.
    def cancelar(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'})
        
        return True
    
    def unlink(self, cr, uid, ids, context=None):
        order = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in order:
            if s['state'] in ['draft','cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar la actividad'))

        return super(crm_ihce, self).unlink(cr, uid, unlink_ids, context=context)


