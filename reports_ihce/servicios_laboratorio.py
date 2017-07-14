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

class create_report_services_laboratory(osv.osv_memory):
    _name = "create.report.services.laboratory"
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']

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
        sheet_principal = workbook.add_sheet('Servicios Laboratorio', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Servicios-Laboratorio.xls"
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
            'description': 'Reporte Servicios LAB',
            'res_model': 'create.report.services.laboratory',
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
        sheet.col(2).width = 10000
        sheet.col(3).width = 10000
        sheet.col(4).width = 2000
        sheet.col(5).width = 4000
        sheet.col(6).width = 4000
        sheet.col(7).width = 6000
        sheet.col(8).width = 4000
        sheet.col(9).width = 4000
        sheet.col(10).width = 4000
        sheet.col(11).width = 4000
        sheet.col(12).width = 4000
        sheet.col(13).width = 4000
        sheet.col(14).width = 4000
        sheet.col(15).width = 4000
        sheet.col(16).width = 4000
        sheet.col(17).width = 4000
        sheet.col(18).width = 4000
        sheet.col(19).width = 4000
        sheet.col(20).width = 4000
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        style2 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour coral;'))
        style3 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #~ #CABECERA
        sheet.write_merge(0, 0, 0, 20,("SECRETARÍA DE DESARROLLO ECONÓMICO DEL ESTADO DE HIDALGO"), style_n)
        sheet.write_merge(1, 1, 0, 20,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), style_n)
        sheet.write_merge(2, 2, 0, 20,("DIRECCIÓN DE LABORATORIO DE DISEÑO Y DESARROLLO DE PRODUCTO"), style_n)
        sheet.write_merge(3, 3, 0, 20,("SERVICIOS A EMPRESAS ATENDIDAS"), style_n)
        #TITULOS
        sheet.write_merge(6, 6, 0, 7, '', style)
        sheet.write_merge(6, 6, 20, 20, '', style)
        sheet.write_merge(5, 5, 8, 19, 'Servicio', style2)
        sheet.write(5, 0, 'CONTROL POR MES', style)
        sheet.write(5, 1, 'No.', style)
        sheet.write(5, 2, 'NOMBRE DE LA EMPRESA', style)
        sheet.write(5, 3, 'NOMBRE PERSONA FISICA', style)
        sheet.write(5, 4, 'SEXO', style)
        sheet.write(5, 5, 'MUNICIPIO', style)
        sheet.write(5, 6, 'SECTOR', style)
        sheet.write(5, 7, 'PRODUCTO/SERVICIO', style)
        sheet.write(6, 8, 'Manual de Identidad Corporativa', style2)
        sheet.write(6, 9, 'Logotipo', style2)
        sheet.write(6, 10, 'Etiquetas', style2)
        sheet.write(6, 11, 'Punto de Venta', style2)
        sheet.write(6, 12, 'Envase', style2)
        sheet.write(6, 13, 'Embalaje', style2)
        sheet.write(6, 14, 'Empaque', style2)
        sheet.write(6, 15, 'Folletos y Catálogos', style2)
        sheet.write(6, 16, 'Fotografía de Producto', style2)
        sheet.write(6, 17, 'Producto 3D', style2)
        sheet.write(6, 18, 'Prototipado Rápido', style2)
        sheet.write(6, 19, 'Aplicaciones', style2)
        sheet.write(5, 20, 'MES DE REGISTRO', style)
        
        i = 8
        m = 1
        a = 1
        ban = False
        e = 7
        meses = ['01','02','03','04','05','06','07','08','09','10','11','12']
        
        if data.type == 'completo':
            laboratory_ids = self.pool.get('desing.laboratory').search(cr, uid, [('state','in',('pre_done','done'))], order='date_fin ASC')
        else:
            laboratory_ids = self.pool.get('desing.laboratory').search(cr, uid, [('state','in',('pre_done','done')),('date_fin','>=',data.date_ini),('date_fin','<=',data.date_fin)], order='date_fin ASC')
            
            
        for row in self.pool.get('desing.laboratory').browse(cr, uid, laboratory_ids, context=context):
            mes = self.month(cr, uid, str(row.date_fin[5:7]), context=context)
            if i == 8:
                sheet.write_merge(7, 7, 0, 20, mes, styleG)
                mez = mes
            else:
                if mez != mes:
                    sheet.write_merge(i, i, 0, 20, mes, styleG)
                    mez = mes
                    i = i +1
            
            sheet = self.carga(cr, uid, i, m, a, row, sheet, context)
            
            if row.option_service == '0':
                if row.service.id == 1:
                    sheet.write(i, 8, '1', style_n)
                elif row.service.id == 2:
                    sheet.write(i, 9, '1', style_n)
                elif row.service.id == 12:
                    sheet.write(i, 9, '1', style_n)
                elif row.service.id == 5:
                    sheet.write(i, 10, '1', style_n)
                elif row.service.id == 15:
                    sheet.write(i, 10, '1', style_n)
                elif row.service.id == 4:
                    sheet.write(i, 11, '1', style_n)
                elif row.service.id == 11:
                    sheet.write(i, 12, '1', style_n)
                elif row.service.id == 6:
                    sheet.write(i, 13, '1', style_n)
                elif row.service.id == 16:
                    sheet.write(i, 14, '1', style_n)
                elif row.service.id == 10:
                    sheet.write(i, 15, '1', style_n)
                elif row.service.id == 9:
                    sheet.write(i, 16, '1', style_n)
                elif row.service.id == 7:
                    sheet.write(i, 17, '1', style_n)
                else:
                    if row.service.id == 3:
                        sheet.write(i, 18, '1', style_n)
            else:
                sheet.write(i, 19, '1', style_n)
                    
            sheet.write(i, 20, mes + '-' + row.date_fin[0:4], style_n)
            i = i + 1
            m = m + 1
            a = a + 1
    
        return sheet
        
    def carga(self, cr, uid, i, m, a, data, sheet, context={}):

        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))

        sheet.write(i, 0, m, style_n)
        sheet.write(i, 1, a, style_n)

        ro = self.pool.get('companies.ihce').browse(cr, uid, data.company_id.id, context)

        sheet.write(i, 2, ro.name.encode('utf-8') or '', style_n)
        sheet.write(i, 3, ro.name_people.encode('utf-8') + " " + ro.apaterno.encode('utf-8') + " " + ro.amaterno.encode('utf-8') or '', style_n)
        sheet.write(i, 4, ro.sexo or '', style_n)
        sheet.write(i, 5, ro.town.name or '', style_n)
        sheet.write(i, 6, ro.sector.name or '', style_n)
        sheet.write(i, 7, ro.idea_commerce or '', style_n)
        
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
