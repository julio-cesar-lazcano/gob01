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

from openerp.osv import osv, fields
import xlwt
import base64
import psycopg2
import psycopg2.extras
from openerp.tools.translate import _
import time

class cursos_ihce_ejecutivo(osv.osv_memory):
    _name = "cursos.ihce.ejecutivo"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'name':fields.text('Instrucciones'),
        'date': fields.date('Fecha de reporte'),
        'date_ini': fields.date('Fecha Inicio'),
        'date_fin': fields.date('Fecha Final'),
        'xls_file_name':fields.char('xls file name', size=128),
        'xls_file':fields.binary('Archivo', readonly=True),
        'user_id': fields.many2one('res.users',"Responsable"),
    }

    _defaults = {
        'name': "Se creara un archivo .xls con el reporte seleccionado.",
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda obj, cr, uid, context: uid,
    }
    
     #~ Función que crea la hoja de calculo para el reportes
    def action_create_report(self, cr, uid, ids, context=None):
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Cursos IHCE Ejecutivo', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Cursos IHCE Ejecutivo.xls"
        # Creamos la ruta con el nombre del archivo donde se guardara
        root = "/tmp/" + str(name)
        # Guardamos la hoja de calculo en la ruta antes creada
        workbook.save(root)
        sprint_file = base64.b64encode(open("/tmp/%s" % (name), 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': name,
            'datas': sprint_file,
            'datas_fname': name,
            'description': 'Reporte Cursos IHCE Ejecutivo',
            'res_model': 'cursos.ihce.ejecutivo',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        return True
    
    #~ Función que llena la hoja con los datos correspondientes del reporte
    def create_principal_sheet(self, cr, uid, ids, sheet, context={}):
        data = self.browse(cr, uid, ids[0], context=context)
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center; '))
        style = xlwt.easyxf(('font: height 180, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 7,("SUBPROGRAMA DE FORMACIÓN DE CAPITAL HUMANO"), styleT)
        sheet.write_merge(1, 1, 0, 7,("Cursos impartidos en el IHCE "), styleT)
        
        sheet.write_merge(2, 2, 0, 7,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
        #TITULOS
        sheet.write(6, 1, 'No. Cursos', style)
        sheet.write(6, 2, 'Horas', style)
        sheet.write(6, 3, 'Asistentes', style)
        sheet.write(6, 4, 'Hombres', style)
        sheet.write(6, 5, 'Mujeres', style)
        
        sheet.write(9, 0, 'No.', style)
        sheet.write_merge(9, 9, 1, 4, 'Curso/Taller', style)
        sheet.write_merge(9, 9, 5, 6, 'Institución', style)
        
        i = 10
        a = 1
        horas = 0
        asistentes = 0
        mujeres = 0
        hombres = 0

        courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin),('dependence','=','ihce')], order='date ASC')
        
        sheet.write(7, 1, len(courses_ids), style_n)
            
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context):
            sheet.write(i, 0, a, style_n)
            sheet.write_merge(i, i, 1, 4, (row.courses_id.name.encode('utf-8')) or '',style_n)
            sheet.write_merge(i, i, 5, 6, row.supplier_id.name  or '', style_n)
            horas += row.hours_training
            asistentes += row.number_attendees
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('company.line').browse(cr, uid, line)
                ro = self.pool.get('companies.ihce').browse(cr, uid, li.contact_id.id, context)
                if ro.sexo == 'M':
                    hombres = hombres + 1
                else:
                    if ro.sexo == 'F':
                        mujeres = mujeres + 1
                        
            for line in self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('list.new.persons').browse(cr, uid, line)
                if li.sexo == 'M':
                    hombres = hombres + 1
                else:
                    if li.sexo == 'F':
                        mujeres = mujeres + 1
            
            a = a + 1
            i = i + 1
        
        sheet.write(7, 2, horas, style_n)
        sheet.write(7, 3, asistentes, style_n)
        sheet.write(7, 4, hombres, style_n)
        sheet.write(7, 5, mujeres, style_n)
        
        return sheet
    
   
      
