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

class reporte_cursos(osv.osv_memory):
    _name = "reporte.cursos"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'name':fields.text('Instrucciones'),
        'type': fields.selection([('completo', 'Completo'), ('rango', 'Por fecha')], 'Tipo de reporte'),
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
        sheet_principal = workbook.add_sheet('Cursos FCH', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Reporte(FCH).xls"
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
            'description': 'Reporte Cursos FCH',
            'res_model': 'reporte.cursos',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        return True
    
    #~ Función que llena la hoja con los datos correspondientes del reporte
    def create_principal_sheet(self, cr, uid, ids, sheet, context={}):
        data = self.browse(cr, uid, ids[0], context=context)
        # Damos tamaños a las columnas
        sheet.col(0).width = 1500
        sheet.col(1).width = 10000
        sheet.col(2).width = 2000
        sheet.col(3).width = 1500
        sheet.col(4).width = 3500
        sheet.col(5).width = 10000
        sheet.col(6).width = 2000
        sheet.col(7).width = 7000
        sheet.col(8).width = 5000
        sheet.col(9).width = 4000
        sheet.col(10).width = 4000
        sheet.col(11).width = 5000
        sheet.col(12).width = 3500
        sheet.col(13).width = 3500
        sheet.col(14).width = 3500
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 14,("FORMACIÓN DE CAPITAL HUMANO"), styleT)
        sheet.write_merge(1, 1, 0, 14,("REPORTE DE CURSOS"), styleT)
        #TITULOS
        sheet.write(3, 0, 'ID', style)
        sheet.write(3, 1, 'TEMA', style)
        sheet.write(3, 2, 'CONSECUTIVO', style)
        sheet.write(3, 3, 'No.', style)
        sheet.write(3, 4, 'CLASIFICACIÓN', style)
        sheet.write(3, 5, 'PARTICIPANTE', style)
        sheet.write(3, 6, 'SEXO', style)
        sheet.write(3, 7, 'NEGOCIO', style)
        sheet.write(3, 8, 'SECTOR', style)
        sheet.write(3, 9, 'IDEA DE NEGOCIO', style)
        sheet.write(3, 10, 'MUNICIPIO', style)
        sheet.write(3, 11, 'EMAIL', style)
        sheet.write(3, 12, 'TELEFONO', style)
        sheet.write(3, 13, 'HORAS', style)
        sheet.write(3, 14, 'MES', style)
        
        i = 5
        a = 1
        c = 1
        
        if data.type == 'completo':
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('services','=','formacion'),('state','=','done'),('dependence','=','ihce'),('type','!=','consultoria')], order='date ASC')
        else:
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('services','=','formacion'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin),('dependence','=','ihce'),('type','!=','consultoria')], order='date ASC')
            
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context):
            mes1 = self.month(cr, uid, row.date[5:7], context)
            if i == 5:
                sheet.write_merge(4, 4, 0, 14,(mes1), styleG)
            else:
                if mes != mes1:
                    sheet.write_merge(i, i, 0, 14,(mes1), styleG)
                    i+=1

            sheet.write(i, 0, c or '', style_n)
            #sheet.write(i, 1, row.courses_id.name.encode('utf-8') + " -- " + row.name.encode('utf-8') or '', style_n)
            sheet.write(i, 1, row.courses_id.name + " -- " + row.name or '', style_n)
            
            m = i
            b = 1
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('company.line').browse(cr, uid, line)
                ro = self.pool.get('companies.ihce').browse(cr, uid, li.contact_id.id, context)
               
                sheet.write(m, 2, a, style_n)
                sheet.write(m, 3, b, style_n)
                sheet.write(m, 4, ro.parent_id.type or '', style_n)
                #sheet.write(m, 5, ro.name.encode('utf-8') or '', style_n)
                sheet.write(m, 5, ro.name or '', style_n)
                sheet.write(m, 6, ro.sexo or '', style_n)
                #sheet.write(m, 7, (ro.parent_id.name.encode('utf-8')) or '', style_n)
                sheet.write(m, 7, (ro.parent_id.name) or '', style_n)
                
                sheet.write(m, 8, ro.parent_id.sector.name or '', style_n)
                sheet.write(m, 9, li.idea_commerce or '', style_n)
                sheet.write(m, 10, ro.town.name or '', style_n)
                sheet.write(m, 11, li.email or '', style_n)
                sheet.write(m, 12, ro.phone or '', style_n)
                
                m+=1
                b+=1
                a+=1
                
            for line in self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('list.new.persons').browse(cr, uid, line)
               
                sheet.write(m, 2, a, style_n)
                sheet.write(m, 3, b, style_n)
                sheet.write(m, 4, '', style_n)
                sheet.write(m, 5, li.name or '', style_n)
                sheet.write(m, 6, li.sexo or '', style_n)
                sheet.write(m, 7, '', style_n)
                
                sheet.write(m, 8, '', style_n)
                sheet.write(m, 9, li.idea_commerce or '', style_n)
                sheet.write(m, 10, li.town.name or '', style_n)
                sheet.write(m, 11, li.email or '', style_n)
                sheet.write(m, 12, li.phone or li.cel_phone or '', style_n)
                
                m+=1
                b+=1
                a+=1
           
            sheet.write(i, 13, row.hours_training or '', style_n)
            sheet.write(i, 14, mes1 + '-' + str(row.date[0:4]) or '', style_n)
           
            i=m +1
            c += 1
            mes = mes1
        
        return sheet
    
    #~ Función para obtener el nombre del mes
    def month(self, cr, uid, val, context=None):
        mes = ""
        if val == '01':
            mes = "ENERO"
        elif val == '02':
            mes = "FEBRERO"
        elif val == '03':
            mes = "MARZO"
        elif val == '04':
            mes = "ABRIL"
        elif val == '05':
            mes = "MAYO"
        elif val == '06':
            mes = "JUNIO"
        elif val == '07':
            mes = "JULIO"
        elif val == '08':
            mes = "AGOSTO"
        elif val == '09':
            mes = "SEPTIEMBRE"
        elif val == '10':
            mes = "OCTUBRE"
        elif val == '11':
            mes = "NOVIEMBRE"
        elif val == '12':
            mes = "DICIEMBRE"
        
        return mes
