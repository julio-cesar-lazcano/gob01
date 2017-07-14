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

class reporte_consultorias_emprered(osv.osv_memory):
    _name = "reporte.consultorias.emprered"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'name':fields.text('Instrucciones'),
        'type': fields.selection([('completo', 'Completo'), ('rango', 'Por fecha')], 'Tipo de reporte'),
        'emprered': fields.many2one('emprereds','Emprered'),
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
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'user_id': lambda obj, cr, uid, context: uid,
    }
    
    #~ Función que crea la hoja de calculo para el reportes
    def action_create_report(self, cr, uid, ids, context=None):
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Consultorias Emprered', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Consultorias Emprered.xls"
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
            'description': 'Reporte Consultorias Emprered',
            'res_model': 'reporte.consultorias.emprered',
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
        sheet.col(1).width = 4000
        sheet.col(2).width = 4000
        sheet.col(3).width = 8000
        sheet.col(4).width = 8000
        sheet.col(5).width = 2000
        sheet.col(6).width = 4000
        sheet.col(7).width = 4000
        sheet.col(8).width = 7000
        sheet.col(9).width = 10000
        sheet.col(10).width = 3000
        sheet.col(11).width = 7000
        sheet.col(12).width = 3000
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        style2 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour coral;'))
        style3 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 12,("SECRETARIA DE DESARROLLO ECONÓMICO DEL ESTADO DE HIDALGO"), styleT)
        sheet.write_merge(1, 1, 0, 12,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 12,("DIRECCIÓN DE ACOMPAÑAMIENTO EMPRESARIAL"), styleT)
        sheet.write_merge(3, 3, 0, 12,("CONSULTORIAS EMPRERED"), styleT)
        #TITULOS
        sheet.write(5, 0, 'No.', style)
        sheet.write(5, 1, 'Emprered', style)
        sheet.write(5, 2, 'Clasificación', style)
        sheet.write(5, 3, 'Empresa', style)
        sheet.write(5, 4, 'Participante', style)
        sheet.write(5, 5, 'Sexo', style)
        sheet.write(5, 6, 'Municipio', style)
        sheet.write(5, 7, 'Sector', style)
        sheet.write(5, 8, 'Producto/Servicio', style)
        sheet.write(5, 9, 'Descripción del servicio de consultoria especializada', style)
        sheet.write(5, 10, 'Horas', style)
        sheet.write(5,11, 'Consultor', style)
        sheet.write(5, 12, 'Mes', style)
        
        i = 7
        a = 1
        meses = ['01','02','03','04','05','06','07','08','09','10','11','12']


        if data.emprered.id:
            if data.type == 'completo':
                courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('dependence','=','emprered'),('type','=','consultoria'),('emprered','=',data.emprered.id)], order='date ASC')
            else:
                courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin),('dependence','=','emprered'),('type','=','consultoria'),('emprered','=',data.emprered.id)], order='date ASC')
        else:
            if data.type == 'completo':
                courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('dependence','=','emprered'),('type','=','consultoria')], order='date ASC')
            else:
                courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin),('dependence','=','emprered'),('type','=','consultoria')], order='date ASC')
    
    
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context):
            mes1 = self.month(cr, uid, row.date[5:7], context)
            if i == 7:
                sheet.write_merge(6, 6, 0, 12,(mes1), styleG)
            else:
                if mes != mes1:
                    sheet.write_merge(i, i, 0, 12,(mes1), styleG)
                    i+=1
            sheet.write(i, 1, row.emprered.name.encode('utf-8') or '', style_n)
            sheet.write(i, 9, row.courses_id.name.encode('utf-8') + "--" + row.name.encode('utf-8') or '', style_n)
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('company.line').browse(cr, uid, line)
                ro = self.pool.get('companies.ihce').browse(cr, uid, li.contact_id.id, context)
               
                sheet.write(i, 0, a, style_n)
                sheet.write(i, 2, ro.parent_id.type, style_n)
                sheet.write(i, 3, (ro.parent_id.name.encode('utf-8')) or '', style_n)
                sheet.write(i, 4, ro.name.encode('utf-8') or '', style_n)
                sheet.write(i, 5, ro.sexo or '', style_n)
                sheet.write(i, 6, ro.town.name.encode('utf-8') or '', style_n)
                sheet.write(i, 7, ro.parent_id.sector.name or '', style_n)
                sheet.write(i, 8, ro.parent_id.idea_commerce or '', style_n)
                sheet.write(i, 10, row.hours_training or '', style_n)
                sheet.write(i, 11, row.supplier_id.name.encode('utf-8') or '', style_n)
                sheet.write(i, 12, mes1 + '-' + str(row.date[0:4]) or '', style_n)
                
                a = a + 1
                i = i + 1
                
            for line in self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('list.new.persons').browse(cr, uid, line)
               
                sheet.write(i, 0, a, style_n)
                #~ sheet.write(i, 1, b, style_n)
                sheet.write(i, 2, li.name.encode('utf-8') or '', style_n)
                sheet.write(i, 3, '', style_n)
                sheet.write(i, 4, li.sexo or '', style_n)
                sheet.write(i, 5, li.town.name.encode('utf-8') or '', style_n)
                sheet.write(i, 6, '', style_n)
                sheet.write(i, 7, row.name.encode('utf-8') or '', style_n)
                sheet.write(i, 8, row.hours_training or '', style_n)
                sheet.write(i, 9, row.supplier_id.name.encode('utf-8') or '', style_n)
                sheet.write(i, 10, mes1 + '-' + str(row.date[0:4]) or '', style_n)
                
                #~ b = b + 1
                a = a + 1
                i = i + 1
           
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
