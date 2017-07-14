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
import os.path
import base64
import io, StringIO
from PIL import Image

class ir_attachment(osv.Model):
    _inherit = 'ir.attachment'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    def create(self, cr, uid, values, context=None):
        try:
			if values.get('res_model') == 'crm.project.ihce':
				image_stream = io.BytesIO(values.get('datas').decode('base64'))
				img = Image.open(image_stream)
				img.thumbnail((200, 300), Image.ANTIALIAS)
				img_stream = StringIO.StringIO()
				root = "/var/www/img/" + str(values.get('name'))
				img.save(root)
				sprint_file = base64.b64encode(open("/var/www/img/%s" % (values.get('name')), 'rb').read())
				values.update({'datas': sprint_file})
			
			id_atach = super(ir_attachment, self).create(cr, uid, values, context)
			
			row = self.pool.get(values.get('res_model')).browse(cr, uid, values.get('res_id'))
		
			if row.company_id:
				data = self.search(cr, uid, [('name','=',values.get('name')),('res_model','=','companies.ihce'),('res_id','=',row.company_id.id)])
				if not data:
					dat = self.browse(cr, uid, id_atach)
					data_attach = {
						'name': dat.name,
						'datas': dat.datas,
						'datas_fname': dat.datas_fname,
						'res_model': 'companies.ihce',
						'res_id': row.company_id.id,
						'type': 'binary',
					}
					self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        except:
            pass
        
