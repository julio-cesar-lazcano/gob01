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

class suppliers_ihce(osv.Model):
    _name = 'suppliers.ihce'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _calculate_ranking(self, cr, uid, ids, field, args, context=None):
        res = {}
        valor = 0
        rows = self.browse(cr, uid, ids, context=context)

        for row in rows:
            i = 0
            valor = 0
            line = self.browse(cr, uid, row.id, context=context)
            
            for li in line.date_course:
                if li.course_evaluation:
                    i = i + 1
                    valor += int(li.course_evaluation)
            if valor > 0:
                valor = int(round(valor)) / i
                self.write(cr, uid, row.id, {'course_evaluation': str(valor)})
            res[row.id] = valor
        
        return res

    _columns = {
        'name': fields.char("Nombre", size=200, required=True),
        'courses_id': fields.many2many('courses.ihce','supplier_courses_rel','supplier_id','courses_id', "Cursos"),
        'rfc': fields.char("RFC", size=20),
        'street': fields.char("Calle", size=100),
        'internal_number': fields.char("Número Interno", size=10),
        'external_number': fields.char("Número Externo", size=10),
        'colony': fields.many2one('colony.hidalgo',"Colonia"),
        'cp': fields.char("Código postal", size=5),
        'city': fields.many2one('states.mexico',"Estado"),
        'country': fields.char("País", size=100,),
        'town': fields.many2one('town.hidalgo',"Municipio"),
        'phone': fields.char("Teléfono", size=20),
        'email': fields.char("Correo electrónico", size=100),
        'area': fields.many2one('forming.area',"Área de formación"),
        'web': fields.char("Paǵina web", size=100),
        'ranking': fields.function(_calculate_ranking, type="integer", string="Evaluación", readonly=True),
        'course_evaluation': fields.selection([('6','Excelente'),('5','Muy bueno'),('4','Bueno'),('3','Regular'),('2','Malo'),('1','Muy malo')], "Evaluación"),
        'date_course': fields.one2many('date.courses','supplier_id', "Fecha de curso"),
        'note': fields.text("Notas"),
    }
    
    _order = "name asc"
    
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['date_course'], context=context)
        unlink_ids = []
        for row in data:
            if not row['date_course']:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar un proveedor que está impartiendo un curso!'))

        return super(suppliers_ihce, self).unlink(cr, uid, unlink_ids, context=context)
