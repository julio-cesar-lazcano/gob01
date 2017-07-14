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

class reporte_asesorias_emprered(osv.osv_memory):
    _name = "reporte.asesorias.emprered"
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
        sheet_principal = workbook.add_sheet('EMPRERED(Asesorias)', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "EMPRERED(Asesorias).xls"
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
            'description': 'Reporte Asesorias Emprered',
            'res_model': 'reporte.asesorias.emprered',
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
        sheet.col(1).width = 7000
        sheet.col(2).width = 10000
        sheet.col(3).width = 10000
        sheet.col(4).width = 2000
        sheet.col(5).width = 4000
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
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        style2 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour coral;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 20,("SECRETARIA DE DESARROLLO ECONÓMICO DEL ESTADO DE HIDALGO"), styleT)
        sheet.write_merge(1, 1, 0, 20,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 20,("DIRECCIÓN DE ACOMPAÑAMIENTO EMPRESARIAL"), styleT)
        sheet.write_merge(3, 3, 0, 20,("ASESORIAS EMPRERED"), styleT)
        #TITULOS
        sheet.write(5, 0, 'No', style)
        sheet.write(5, 1, 'Emprered', style)
        sheet.write(5, 2, 'Empresa', style)
        sheet.write(5, 3, 'Sexo', style)
        sheet.write(5, 4, 'Municipio', style)
        sheet.write(5, 5, 'Sector', style)
        sheet.write(5, 6, 'Clasificación', style)
        sheet.write(5, 7, 'Asesoría Gral. Servicios IHCE', style2)
        sheet.write(5, 8, 'Registro de Marca', style2)
        sheet.write(5, 9, 'Patente', style2)
        sheet.write(5, 10, 'Código de Barras', style2)
        sheet.write(5, 11, 'Imagen Corporativa y Etiquetado', style2)
        sheet.write(5, 12, 'Financiamiento', style2)
        sheet.write(5, 13, 'Emprendimiento', style2)
        sheet.write(5, 14, 'Registro ante la SHCP', style2)
        sheet.write(5, 15, 'Formación de Capital Humano', style2)
        sheet.write(5, 16, 'AIE', style2)
        sheet.write(5, 17, 'Manos a la obra', style2)
        sheet.write(5, 18, 'Aceleración Empresarial', style2)
        sheet.write(5, 19, 'Adecuació', style2)
        sheet.write(5, 20, 'Mes', style)
        
        i = 7
        m = 1
        a = 1
        ban = True
        e = 6
        meses = ['01','02','03','04','05','06','07','08','09','10','11','12']
        
        if data.type == 'completo':
            asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('option','=','emprered')], order='date ASC')
        else:
            asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')

            
        for row in self.pool.get('asesorias.ihce').browse(cr, uid, asesoria_ids, context=context):
            if row.name == 'asesoria' or row.name == 'marca' or row.name == 'patente' or row.name == 'codigo' or row.name == 'imagen' or row.name == 'financiamiento' or row.name == 'emprendimiento' or row.name == 'shcp' or row.name == 'capital' or row.name == 'aie' or row.name == 'manos' or row.name == 'aceleracion' or row.name == 'adecuacion':
                ban = True
            else:
                ban = False
            
            if ban:
                mes = self.month(cr, uid, row.date[5:7], context=context)
                if i == 7:
                    sheet.write_merge(6, 6, 0, 20, mes, styleG)
                    mez = mes
                else:
                    if mez != mes:
                        sheet.write_merge(i, i, 0, 20, mes, styleG)
                        mez = mes
                        i = i +1
                
                sheet.write(i, 1, row.emprered.name, style_n)
                sheet = self.carga(cr, uid, i, m, row, sheet, context)
                
                if row.name == 'asesoria':
                    sheet.write(i, 7, '1', style_n)
                elif row.name == 'marca':
                    sheet.write(i, 8, '1', style_n)
                elif row.name == 'patente':
                    sheet.write(i, 9, '1', style_n)
                elif row.name == 'codigo':
                    sheet.write(i, 10, '1', style_n)
                elif row.name == 'imagen':
                    sheet.write(i, 11, '1', style_n)
                elif row.name == 'financiamiento':
                    sheet.write(i, 12, '1', style_n)
                elif row.name == 'emprendimiento':
                    sheet.write(i, 13, '1', style_n)
                elif row.name == 'shcp':
                    sheet.write(i, 14, '1', style_n)
                elif row.name == 'capital':
                    sheet.write(i, 15, '1', style_n)
                elif row.name == 'aie':
                    sheet.write(i, 16, '1', style_n)
                elif row.name == 'manos':
                    sheet.write(i, 17, '1', style_n)
                elif row.name == 'adecuacion':
                    sheet.write(i, 19, '1', style_n)
                else:
                    if row.name == 'aceleracion':
                        sheet.write(i, 18, '1', style_n)
                        
                sheet.write(i, 20, mes + '-' + row.date[0:4], style_n)
                i = i + 1
                m = m + 1
                a = a + 1
        
        return sheet
        
    def carga(self, cr, uid, i, m, data, sheet, context={}):

        #style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
       # style_n = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        sheet.write(i, 0, m)

        ro = self.pool.get('companies.ihce').browse(cr, uid, data.company_id.id, context)

        sheet.write(i, 2, ro.name or '')
        sheet.write(i, 3, ro.sexo or '')
        sheet.write(i, 4, ro.town.name or '')
        sheet.write(i, 5, ro.sector.name or '')
        sheet.write(i, 6, ro.type or '')
        
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
