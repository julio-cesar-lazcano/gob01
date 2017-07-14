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

class reporte_servicio_pymes(osv.osv_memory):
    _name = "reporte.servicio.pymes"
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
        sheet_principal = workbook.add_sheet('Servicio MiPYMES', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Servicio-MiPYMES.xls"
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
            'description': 'Reporte Servicios DE',
            'res_model': 'reporte.servicio.pymes',
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
        sheet.col(1).width = 1500
        sheet.col(2).width = 10000
        sheet.col(3).width = 10000
        sheet.col(4).width = 2000
        sheet.col(5).width = 4000
        sheet.col(6).width = 4000
        sheet.col(7).width = 6000
        sheet.col(8).width = 3500
        sheet.col(9).width = 3500
        sheet.col(10).width = 3500
        sheet.col(11).width = 3500
        sheet.col(12).width = 3500
        sheet.col(13).width = 4500
        sheet.col(14).width = 4500
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        style2 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 14,("DESARROLLO EMPRESARIAL"), styleT)
        sheet.write_merge(1, 1, 0, 14,("SERVICIOS MiPYMES"), styleT)
        #TITULOS
        sheet.write(3, 0, 'Control', style)
        sheet.write(3, 1, 'No.', style)
        sheet.write(3, 2, 'Empresa', style)
        sheet.write(3, 3, 'Persona Física', style)
        sheet.write(3, 4, 'Sexo', style)
        sheet.write(3, 5, 'Municipio', style)
        sheet.write(3, 6, 'Sector', style)
        sheet.write(3, 7, 'Producto/Servicio', style)
        sheet.write(3, 8, 'Registro de Marca', style2)
        sheet.write(3, 9, 'Patente', style2)
        sheet.write(3, 10, 'Código de Barras', style2)
        sheet.write(3, 11, 'Tabla Nutrimental', style2)
        sheet.write(3, 12, 'Cursos -IHCE-', style2)
        sheet.write(3, 13, 'Cursos -Emprered-', style2)
        sheet.write(3, 14, 'Mes de Registro', style)
        
        i = 5
        m = 1
        a = 1
        ban = False
        e = 4
        meses = ['01','02','03','04','05','06','07','08','09','10','11','12']
        
        if data.type == 'completo':
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('option','=','ihce')], order='date ASC')
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('option','=','ihce')], order='date ASC')
            patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True')], order='date ASC')
            fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True')], order='date ASC')
        else:
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
            patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
            fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
            
        for z in meses:
            mes = self.month(cr, uid, z, context=context)
            for row in self.pool.get('register.trademark').browse(cr, uid, register_ids, context=context):
                if str(row.date[5:7]) == z:
                    sheet = self.carga(cr, uid, i, m, a, row, sheet, context)
                    sheet.write(i, 8, '1', style_n)
                    #~ Verificamos si el registro tiene cursos
                    for cur in row.courses_ids:
                        curso = self.pool.get('date.courses').browse(cr, uid, cur.id, context=context)
                        if curso.type == 'curso':
                            if curso.dependence == 'ihce':
                                sheet.write(i, 12, '1', style_n)
                            else:
                                if curso.dependence == 'emprered':
                                    sheet.write(i, 13, '1', style_n)
                    
                    sheet.write(i, 14, mes + '-' + str(row.date[0:4]), style_n)
                    ban = True
                    i = i + 1
                    m = m + 1
                    a = a + 1
            for rows in self.pool.get('bar.code').browse(cr, uid, bar_ids, context=context):
                if str(rows.date[5:7]) == z:
                    sheet = self.carga(cr, uid, i, m, a, rows, sheet, context)
                    sheet.write(i, 10, '1', style_n)
                    #~ Verificamos si el registro tiene cursos
                    for cur in rows.courses_ids:
                        curso = self.pool.get('date.courses').browse(cr, uid, cur.id, context=context)
                        if curso.type == 'curso':
                            if curso.dependence == 'ihce':
                                sheet.write(i, 12, '1', style_n)
                            else:
                                if curso.dependence == 'emprered':
                                    sheet.write(i, 13, '1', style_n)
                                    
                    sheet.write(i, 14, mes + '-' + str(row.date[0:4]), style_n)
                    ban = True
                    i = i + 1
                    m = m + 1
                    a = a + 1
            for roww in self.pool.get('patent.ihce').browse(cr, uid, patent_ids, context=context):
                if str(roww.date[5:7]) == z:
                    sheet = self.carga(cr, uid, i, m, a, roww, sheet, context)
                    sheet.write(i, 9, '1', style_n)
                    #~ Verificamos si el registro tiene cursos
                    for cur in roww.courses_ids:
                        curso = self.pool.get('date.courses').browse(cr, uid, cur.id, context=context)
                        if curso.type == 'curso':
                            if curso.dependence == 'ihce':
                                sheet.write(i, 12, '1', style_n)
                            else:
                                if curso.dependence == 'emprered':
                                    sheet.write(i, 13, '1', style_n)
                                    
                    sheet.write(i, 14, mes + '-' + str(row.date[0:4]), style_n)
                    ban = True
                    i = i + 1
                    m = m + 1
                    a = a + 1
            for fda in self.pool.get('fda.ihce').browse(cr, uid, fda_ids, context=context):
                if str(fda.date[5:7]) == z:
                    sheet = self.carga(cr, uid, i, m, a, fda, sheet, context)
                    sheet.write(i, 11, '1', style_n)
                    #~ Verificamos si el registro tiene cursos
                    for cur in fda.courses_ids:
                        curso = self.pool.get('date.courses').browse(cr, uid, cur.id, context=context)
                        if curso.type == 'curso':
                            if curso.dependence == 'ihce':
                                sheet.write(i, 12, '1', style_n)
                            else:
                                if curso.dependence == 'emprered':
                                    sheet.write(i, 13, '1', style_n)
                                    
                    sheet.write(i, 14, mes + '-' + str(row.date[0:4]), style_n)
                    ban = True
                    i = i + 1
                    m = m + 1
                    a = a + 1
                    
            if ban:
                sheet.write_merge(e, e, 0, 14, mes, styleG)
                e = i
                i = i + 1
                a = 1
                ban = False
        
        return sheet
        
    def carga(self, cr, uid, i, m, a, data, sheet, context={}):

        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))

        sheet.write(i, 0, m, style_n)
        sheet.write(i, 1, a, style_n)

        ro = self.pool.get('companies.ihce').browse(cr, uid, data.company_id.id, context)

        sheet.write(i, 2, ro.name or '', style_n)
        sheet.write(i, 3, ro.name_people.encode('utf-8') + " " + ro.apaterno.encode('utf-8') + " " + ro.amaterno.encode('utf-8') or '', style_n)
        sheet.write(i, 4, ro.sexo or '', style_n)
        sheet.write(i, 5, ro.town.name or '', style_n)
        sheet.write(i, 6, ro.sector.name or '', style_n)

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
