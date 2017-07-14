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
import xlsxwriter
import base64
from StringIO import StringIO
import psycopg2
import psycopg2.extras
from openerp.tools.translate import _
import time
import locale
from PIL import Image
import os
import xmlrpclib
import io, StringIO
from PIL import Image
from datetime import datetime
from datetime import datetime, date, timedelta
import pdb
#pdb.set_trace()


class reports_aceleracion(osv.osv_memory):
    _name = "reports.aceleracion"
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

    def action_create_report(self, cr, uid, ids, context=None):
        uid = 1
   
        data = self.browse(cr, uid, ids[0], context=context)

        file_name = '/tmp/Aceleracion.xlsx'

        workbook = xlsxwriter.Workbook(file_name)

        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        #styleT = workbook.add_format({'font: height 260, bold 1, color black; alignment: horizontal center;'})
        styleT = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'left'})

        styleTa = workbook.add_format({'font_color': 'black','align': 'horizontal center', 'align':'center', 'bg_color':'orange'})

        styleT2 = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'right'})

        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        # Create a new Chart object.
        chart = workbook.add_chart({'type': 'column'})


        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 8
        l = 1

        worksheet.set_row(0, 30)
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 40)
        worksheet.set_column('C:C', 40)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 30)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 40)
        worksheet.set_column('I:I', 8)
        worksheet.set_column('J:J', 13)
        worksheet.set_column('K:K', 30)
        worksheet.set_column('L:L', 25)
        worksheet.set_column('M:M', 15)
        worksheet.set_column('N:N', 17)
        worksheet.set_column('O:O', 10)



        worksheet.write('A2', '', styleTa)
        worksheet.write('B2', '', styleTa)
        worksheet.write('C2', 'INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL', styleTa)
        worksheet.write('D2', '', styleTa)
        worksheet.write('E2', '', styleTa)
        worksheet.write('F2', '', styleTa)
        worksheet.write('G2', '', styleTa)
        worksheet.write('H2', '', styleTa)
        worksheet.write('I2', '', styleTa)
        worksheet.write('J2', '', styleTa)
        worksheet.write('K2', '', styleTa)
        worksheet.write('L2', '', styleTa)
        worksheet.write('M2', '', styleTa)
        worksheet.write('N2', '', styleTa)
        worksheet.write('O2', '', styleTa)



        date_time = datetime.now()

        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align':'left'})
       
         

        worksheet.write('B4',"Reporte correspondiente del "+str(data.date_ini), styleT2)
        worksheet.write('C4'," Al  "+str(data.date_fin), styleT)
        worksheet.write('A7', 'No.', styleT)
        worksheet.write('B7', 'Nombre', styleT)
        worksheet.write('C7', 'Nombre Comercial', styleT)
        worksheet.write('D7', 'Producto o servicio', styleT)
        worksheet.write('E7', 'Tramite', styleT)
        worksheet.write('F7', 'Municipio', styleT)
        worksheet.write('G7', 'RFC', styleT)
        worksheet.write('H7', 'Correo', styleT)
        worksheet.write('I7', 'Sexo', styleT)
        worksheet.write('J7', 'Telefono', styleT)
        worksheet.write('K7', 'Area de atención', styleT)
        worksheet.write('L7', 'Emprered', styleT)
        worksheet.write('M7', 'Fecha', styleT)
        worksheet.write('N4',"Fecha  ", styleT2)
        worksheet.write('O4', date_time, date_format) 
        
       

        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin), ('name','!=','')], context=None)

        #pdb.set_trace()
        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
        #pdb.set_trace()
            #if(row.name != ''):
          

            worksheet.write('A'+str(i), str(l), styleT)
            worksheet.write('B'+str(i), row.name, styleT)
            worksheet.write('C'+str(i), row.name_commercial, styleT)
            worksheet.write('D'+str(i), row.Productos_Servicios, styleT)
            worksheet.write('E'+str(i), row.tramit, styleT)
            worksheet.write('F'+str(i), row.town_company.name, styleT)
            worksheet.write('G'+str(i), row.rfc, styleT)
            worksheet.write('H'+str(i), row.email, styleT)
            worksheet.write('I'+str(i), row.sexo, styleT)
            worksheet.write('J'+str(i), row.cel_phone, styleT)
            worksheet.write('K'+str(i), row.atention_area.name, styleT)
            worksheet.write('L'+str(i), row.emprered.name, styleT)
            worksheet.write('M'+str(i), row.date, styleT)

            if row.sexo == 'M':
                   hombres = hombres + 1
            
            if row.sexo == 'F':
                   mujeres = mujeres + 1

            i = i + 1
            l = l + 1



        worksheet.write('A'+str(i+10), 'Hombres', styleT)
        worksheet.write_column('B'+str(i+10), [hombres])
        worksheet.write('A'+str(i+11), 'Mujeres', styleT)
        worksheet.write_column('B'+str(i+11), [mujeres])

        chart.add_series({
           'name':       'H'+str(hombres),
          'values': '=Sheet1!$B$'+str(i+10)})
        chart.add_series({
           'name':       'M'+str(mujeres),
           'values': '=Sheet1!$B$'+str(i+11)})

        worksheet.insert_chart('A'+str(i+15), chart)
        worksheet.write_column('B'+str(i+10), [])

        workbook.close()

        
        sprint_file = base64.b64encode(open("/tmp/Aceleracion.xlsx", 'rb').read())
        #sprint_file = base64.b64encode(open("/tmp/Recepcion.xlsx", 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': 'Testing.xlsx',
            'datas': sprint_file,
            'datas_fname': 'Testing.xlsx',
            'description': 'Informe Mensual Aceleracion Empresarial',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':'Aceleracion.xlsx'})

        return True

   
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ EMPRENDIMIENTO
        sheet.write_merge(6, 6, 2, 9,("Instituto Hidalguense de Competitividad Empresarial "), styleGA)
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(7, 7, 2, 9,("Registro de entradas"), styleG)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 11
        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('write_uid','=',72),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        sheet.write(10, 2, ("Nombre"), styleGA)
        sheet.write(10, 3, ("Edad"), styleGA)
        sheet.write(10, 4, ("Email"), styleGA)
        sheet.write(10, 5, ("Telefono"), styleGA)
        sheet.write(10, 6, ("Sexo"), styleGA)
        sheet.write(10, 7, ("Fecha"), styleGA)

        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
            anios = datetime.strptime(row.date, "%Y-%m-%d").date().year - datetime.strptime(row.date_birth, "%Y-%m-%d").date().year
            sheet.write(i, 2, row.name, style_n)
            sheet.write(i, 3, anios, style_n)
            sheet.write(i, 4, row.email, style_n)
            sheet.write(i, 5, row.cel_phone, style_n)
            sheet.write(i, 6, row.sexo, style_n)
            sheet.write(i, 7, row.date, style_n)
            if row.sexo == 'M':
                    hombres = hombres + 1
            
            if row.sexo == 'F':
                    mujeres = mujeres + 1

            i = i + 1

        sheet.write(10, 8, ("Total:"), styleV)
        sheet.write(10, 9, len(courses_ids), style_n)

        sheet.write(11, 8, ("Hombres:"), styleV)
        sheet.write(11, 9, hombres, style_n)

        sheet.write(12, 8, ("Mujeres:"), styleV)
        sheet.write(12, 9, mujeres, style_n)
        
        return sheet

    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
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

class reports_recepcion(osv.osv_memory):
    _name = "reports.recepcion"
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

    def action_create_report(self, cr, uid, ids, context=None):

        uid = 1

        data = self.browse(cr, uid, ids[0], context=context)

        file_name = '/tmp/Recepcion.xlsx'

        workbook = xlsxwriter.Workbook(file_name)

        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        #styleT = workbook.add_format({'font: height 260, bold 1, color black; alignment: horizontal center;'})
        #styleT = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'left'})

        #styleTa = workbook.add_format({'font_color': 'black','align': 'horizontal center', 'align':'center', 'bg_color':'orange'})

        #styleT2 = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'right'})

        #format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        # Create a new Chart object.


        styleTitulosL = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12,  'left':1, 'bottom':1, 'top':1, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosR = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12,  'right':1, 'bottom':1, 'top':1, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulos = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosUp = workbook.add_format({'font_color': 'black', 'top':1, 'bottom':1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosDown = workbook.add_format({'font_color': 'black', 'top':1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bold':True})

        styleTitulosAll = workbook.add_format({'font_color': 'black', 'border': 1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleT = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 1, 'align':'left'})

        styleTa = workbook.add_format({'font_color': 'black','align': 'horizontal center', 'align':'center', 'border': 1, 'bg_color':'white', })

        styleT2 = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'center', 'bold':True,'bg_color':'#58a9ab'})

        styleT2a = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 1, 'align':'center', 'bold':True, 'bg_color':'#ab5a58'})

        styleT2b = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'center', 'bold':True})

        styleT2W = workbook.add_format({'font_color': 'white', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'center', 'bold':True})

        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})


        chart = workbook.add_chart({'type': 'column'})


        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 8
        l = 0

        worksheet.set_row(0, 30)
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:C', 11)
        worksheet.set_column('D:D', 7)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 17)
        worksheet.set_column('G:G', 10)


        worksheet.write('A2', '', styleT2)
        worksheet.write('B2', '', styleT2)
        worksheet.write('C2', 'INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL', styleT2)
        worksheet.write('D2', '', styleT2)
        worksheet.write('E2', '', styleT2)
        worksheet.write('F2', '', styleT2)
        worksheet.write('G2', '', styleT2)



        date_time = datetime.now()

        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align':'left', 'bold':True, 'bg_color':'#58a9ab'})
       
        worksheet.write('A4', '', styleT2) 
        worksheet.write('B4',"Reporte correspondiente del "+str(data.date_ini), styleT2)
        worksheet.write('C4'," Al  "+str(data.date_fin), styleT2)
        worksheet.write('D4', '', styleT2)
        worksheet.write('E4',"Fecha  ", styleT2)
        worksheet.write('F4', date_time, date_format) 
        worksheet.write('G4', '', styleT2)



        worksheet.write('A7', 'No.', styleT2a)
        worksheet.write('B7', 'Nombre', styleT2a)
        worksheet.write('C7', 'Edad', styleT2a)
        worksheet.write('D7', 'Sexo', styleT2a)
        worksheet.write('E7', 'Correo', styleT2a)
        worksheet.write('F7', 'Telefono', styleT2a)
        worksheet.write('G7', 'Fecha', styleT2a)
       

        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('write_uid','=',72),('date','>=',data.date_ini),('date','<=',data.date_fin), ('name','!=','')], context=None)

        #pdb.set_trace()
        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
            #pdb.set_trace()
            #if(row.name != ''):
            anios = datetime.strptime(row.date, "%Y-%m-%d").date().year - datetime.strptime(row.date_birth, "%Y-%m-%d").date().year

            worksheet.write('A'+str(i), str(l), styleT)
            worksheet.write('B'+str(i), row.name, styleT)
            worksheet.write('C'+str(i), anios, styleT)
            worksheet.write('D'+str(i), row.sexo, styleT)
            worksheet.write('E'+str(i), row.email, styleT)
            worksheet.write('F'+str(i), row.cel_phone, styleT)
            worksheet.write('G'+str(i), row.date, styleT)

            if row.sexo == 'M':
                    hombres = hombres + 1
            
            if row.sexo == 'F':
                    mujeres = mujeres + 1

            i = i + 1
            l = l + 1



        worksheet.write('A'+str(i+10), 'Hombres', styleT2W)
        worksheet.write_column('B'+str(i+10), [hombres], styleT2W)
        worksheet.write('C'+str(i+10), 'Mujeres', styleT2W)
        worksheet.write_column('D'+str(i+10), [mujeres], styleT2W)

        chart.add_series({
            'name':       'H'+str(hombres),
            'values': '=Sheet1!$B$'+str(i+10)})
        chart.add_series({
            'name':       'M'+str(mujeres),
            'values': '=Sheet1!$D$'+str(i+10)})

        worksheet.insert_chart('J'+str(9), chart)

        workbook.close()


        sprint_file = base64.b64encode(open("/tmp/Recepcion.xlsx", 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': 'Testing.xlsx',
            'datas': sprint_file,
            'datas_fname': 'Testing.xlsx',
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':'Recepcion.xlsx'})

        return True

    #~ Función que crea la hoja de calculo para el informe mensual
    def action_create_report2(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Informe IHCE Recepción', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, sheet_principal, data, context)
        # Creamos el nombre del archivo
        name = "Informe IHCE Recepcion.xls"
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
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        
        return True
    
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ EMPRENDIMIENTO
        sheet.write_merge(6, 6, 2, 9,("Instituto Hidalguense de Competitividad Empresarial "), styleGA)
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(7, 7, 2, 9,("Registro de entradas"), styleG)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 11
        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('write_uid','=',72),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        sheet.write(10, 2, ("Nombre"), styleGA)
        sheet.write(10, 3, ("Edad"), styleGA)
        sheet.write(10, 4, ("Email"), styleGA)
        sheet.write(10, 5, ("Telefono"), styleGA)
        sheet.write(10, 6, ("Sexo"), styleGA)
        sheet.write(10, 7, ("Fecha"), styleGA)

        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
            anios = datetime.strptime(row.date, "%Y-%m-%d").date().year - datetime.strptime(row.date_birth, "%Y-%m-%d").date().year
            sheet.write(i, 2, row.name, style_n)
            sheet.write(i, 3, anios, style_n)
            sheet.write(i, 4, row.email, style_n)
            sheet.write(i, 5, row.cel_phone, style_n)
            sheet.write(i, 6, row.sexo, style_n)
            sheet.write(i, 7, row.date, style_n)
            if row.sexo == 'M':
                    hombres = hombres + 1
            
            if row.sexo == 'F':
                    mujeres = mujeres + 1

            i = i + 1

        sheet.write(10, 8, ("Total:"), styleV)
        sheet.write(10, 9, len(courses_ids), style_n)

        sheet.write(11, 8, ("Hombres:"), styleV)
        sheet.write(11, 9, hombres, style_n)

        sheet.write(12, 8, ("Mujeres:"), styleV)
        sheet.write(12, 9, mujeres, style_n)
        
        return sheet
    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
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

class reports_ihce(osv.osv_memory):
    _name = "reports.ihce"
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

    #~ Función que crea la hoja de calculo para el informe mensual


    def action_create_report(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Informe IHCE', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, sheet_principal, data, context)
        # Creamos el nombre del archivo
        name = "Informe IHCE.xls"
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
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        
        return True

    
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ EMPRENDIMIENTO
        sheet.write_merge(6, 6, 2, 9,("Instituto Hidalguense de Competitividad Empresarial "), styleGA)
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(7, 7, 2, 9,("Emprendimiento"), styleG)
        sheet.write_merge(8, 8, 2, 8,  "Emprendedores de Alto Impacto", style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(9, 9, 2, 8,  "Platicas/Cursos/Talleres, etc Emprendimiento", style_n)
        courses_empre_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','emprendimiento'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin), ('type','!=','consultoria')], context=None)
        sheet.write(9, 9, len(courses_empre_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(10, 10, 2, 8,  "Asistentes", style_n)
        asis_empre = 0
        for row_asi in self.pool.get('date.courses').browse(cr, uid, courses_empre_ids, context=None):
            asis_empre += row_asi.number_attendees
        sheet.write(10, 9, asis_empre, style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(11,11, 2, 8,  "Asesoría a emprendedores", style_n)
        asesorias_empre_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','emprendimiento')], order='date ASC')
        sheet.write(11, 9, len(asesorias_empre_ids), style_n)
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DESARROLLO EMPRESARIAL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(13, 13, 2, 9,("Servicios Empresariales"), styleG)
        sheet.write_merge(14, 14, 2, 9,("Asesorías"), styleV)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(15, 15, 2, 8,  "Registro de marca", style_n)
        register_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','marca')], order='date ASC')
        sheet.write(15, 9, len(register_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(16, 16, 2, 8,  "Patente", style_n)
        patent_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','patente')], order='date ASC')
        sheet.write(16, 9, len(patent_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(17,17, 2, 8,  "Código de Barras", style_n)
        bar_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','codigo'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(17, 9, len(bar_ids), style_n)
        
         #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(18,18, 2, 8,  "Adecuación de Procesos", style_n)
        adec_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(18, 9, len(adec_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(19,19, 2, 8,  "Normatividad Nacional", style_n)
        norm_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','normatividad'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(19, 9, len(norm_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(20, 20, 2, 8,  "Pruebas de laboratorio/Tabla nutrimental", style_n)
        fda_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','tabla'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(20, 9, len(fda_ids), style_n)
       
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        sheet.write_merge(21, 21, 2, 8,  "Total", style_B)
        total = len(register_ids) + len(patent_ids) + len(bar_ids) + len(adec_ids) + len(norm_ids) + len(fda_ids)
        sheet.write(21, 9, total, style_B)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(22, 22, 2, 9,("Servicios"), styleV)
        
        sheet.write_merge(23, 23, 2, 8,  "Registro de marca", style_n)
        register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(23, 9, len(register_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(24, 24, 2, 8,  "Patente", style_n)
        patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write(24, 9, len(patent_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(25, 25, 2, 8,  "Membresías Código de Barras", style_n)
        bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(25, 9, len(bar_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(26, 26, 2, 8,  "Pruebas de laboratorio/Tabla nutrimental", style_n)
        fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write(26, 9, len(fda_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(27, 27, 2, 8,  "Total", style_B)
        total = len(register_ids) + len(patent_ids) + len(bar_ids) + len(fda_ids)
        sheet.write(27, 9, total, style_B)
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FORMACION DE CAPITAL HUMANO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(29, 29, 2, 9,("Formación de Capital Humano"), styleG)
        sheet.write_merge(30, 30, 2, 8, "Empresas que recibieron consultoría individual para resolver problemas empresariales específicos", style_n)
        sheet.write_merge(31, 31, 2, 8,  "Horas", style_n)
        sheet.write_merge(32, 32, 2, 8 , "Cursos, talleres, diplomados, platicas, etc.", style_n)
        sheet.write_merge(33, 33, 2, 8,  "Horas", style_n)
        sheet.write_merge(34, 34, 2, 8, "Asistentes", style_n)
        
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        
        #~ Consultoria, horas y empresas
        consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        for row in self.pool.get('date.courses').browse(cr, uid, consultoria_ids, context=None):
            horas_con += row.hours_training
            invitados_ids = self.pool.get('company.invited').search(cr, uid, [('course_id','=', row.id)], context=None)
            for line in self.pool.get('company.invited').browse(cr, uid, invitados_ids, context=None):
                ban = False
                for li in company_ids:
                    if li == line.company_id.id:
                        ban = True
                        break 
                if not ban:
                    company_ids.append(line.company_id.id)
        
        sheet.write(30, 9, len(company_ids), style_n)
        #sheet.write(30, 9, len(consultoria_ids), style_n)

        sheet.write(31, 9, horas_con, style_n)
        
        #~ Cursos, talleres, etc
        courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('services','=','formacion'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        sheet.write(32, 9, len(courses_ids), style_n)
        
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            horas += row.hours_training
            asistentes += row.number_attendees
        
        sheet.write(33, 9, horas, style_n)
        sheet.write(34, 9, asistentes, style_n)
        
        
    
        #~ A prtir de aqui se agregan las notas del crm que son marcadas como importantes y las fotografias que se hayan adjuntado al proyecto de crm
        actividades = self.pool.get('crm.project.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('priority','=','1'),('option','=','ihce'),('area','!=',10),('state','=','d-done')], context=None)
        
        if actividades:
            sheet.write_merge(38, 38, 1, 10, "ACTIVIDADES RELEVANTES", styleTT)
            
            con = 1
            col = 40
            style_na = xlwt.easyxf(('font: height 175, color black; alignment: horizontal left'))

            for row in self.pool.get('crm.project.ihce').browse(cr, uid, actividades, context=None):
                if not row.notes:
                    sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + str(row.name.encode('utf-8')) + "    " + str(row.date), style_na)
                else:
                    sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + str(row.name.encode('utf-8')) + "    " + str(row.date) + "   " + str(row.notes.encode('utf-8')), style_na)
                col = col + 4
                j = 1
                
                fotos_ids = self.pool.get('ir.attachment').search(cr, uid, [('res_model','=','crm.project.ihce'),('res_id','=',row.id)], context=None)
                ro = 1
                for line in self.pool.get('ir.attachment').browse(cr, uid, fotos_ids):
                    name = line.name.split('.')
                    #~ Convertimos y guardamos la imagen en formato bmp
                    try:
                        img = Image.open("/var/www/img/%s" % (line.name)).convert("RGB").save("/var/www/img/"+str(name[0])+".bmp")
                        #~ Se muestra la imagen
                        if j == 3:
                            ro = 1
                            j = 1
                            col = col + 16
                        sheet.insert_bitmap("/var/www/img/"+str(name[0])+".bmp", col, ro)
                        ro = ro + 4
                        j = j + 1
                    except:
                        print ""
            
                col = col + 16
                con = con + 1
        
        return sheet
    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
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

class reports_vitacora(osv.osv_memory):
    _name = "reports.vitacora"
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

    def action_create_report(self, cr, uid, ids, context=None):

        

        data = self.browse(cr, uid, ids[0], context=context)

        file_name = '/tmp/Testing.xlsx'

        workbook = xlsxwriter.Workbook(file_name)

        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        #styleT = workbook.add_format({'font: height 260, bold 1, color black; alignment: horizontal center;'})
        styleT = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'left'})

        styleTa = workbook.add_format({'font_color': 'black','align': 'horizontal center', 'align':'center', 'bg_color':'white'})

        styleT2 = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'right'})

        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        # Create a new Chart object.
        chart = workbook.add_chart({'type': 'column'})


        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 8
        l = 0

        worksheet.set_row(0, 30)
        worksheet.set_column('A:A', 3)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 30)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 30)
        worksheet.set_column('G:G', 30)
        worksheet.set_column('H:H', 30)
        worksheet.set_column('I:I', 30)
        worksheet.set_column('J:J', 30)
        worksheet.set_column('K:K', 30)
        worksheet.set_column('L:L', 30)
        worksheet.set_column('M:M', 30)
        worksheet.set_column('N:N', 30)
        worksheet.set_column('O:O', 30)
        worksheet.set_column('P:P', 30)
        worksheet.set_column('Q:Q', 30)
        worksheet.set_column('R:R', 30)
        worksheet.set_column('S:S', 30)
        worksheet.set_column('T:T', 30)
        worksheet.set_column('U:U', 30)
        worksheet.set_column('V:V', 30)
        worksheet.set_column('W:W', 30)
        worksheet.set_column('X:X', 30)
        worksheet.set_column('Y:Y', 30)
        worksheet.set_column('Z:Z', 30)
        



        
        worksheet.write('B2', 'Directorio Empresarial de la Secretaría de Desarrollo Económico', styleT)
        
        worksheet.write('B3', 'Formato para la Captura de Información de Primer Contacto', styleT)

        date_time = datetime.now()

        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align':'left'})
       
        
        worksheet.write('B5',"Reporte correspondiente del "+str(data.date_ini), styleT2)
        worksheet.write('C5'," Al  "+str(data.date_fin), styleT)
        #worksheet.write('F4', date_time, date_format) 

        worksheet.write('A7', 'No.', styleT)
        worksheet.write('B7', 'Nombre', styleT)
        worksheet.write('C7', 'Programa, Proyecto o Acción', styleT)
        worksheet.write('D7', 'Nombre', styleT)
        worksheet.write('E7', 'RFC fisica', styleT)
        worksheet.write('F7', 'RFC moral', styleT)
        worksheet.write('G7', 'Cámara o Asociación', styleT)
        worksheet.write('H7', 'Origen', styleT)
        worksheet.write('I7', 'Año de Inicio de Operaciones', styleT)
        worksheet.write('J7', 'Domicilio', styleT)
        worksheet.write('K7', 'Código Postal', styleT)
        worksheet.write('L7', 'Localidad', styleT)
        worksheet.write('M7', 'Municipio', styleT)
        worksheet.write('N7', 'Giro', styleT)
        worksheet.write('O7', 'Principales Productos o Servicios', styleT)
        worksheet.write('P7', 'Sector', styleT)
        worksheet.write('Q7', 'Número de Trabajadores', styleT)
        worksheet.write('R7', 'Empleos Generadores', styleT)
        worksheet.write('S7', 'Actividades de Ciencia, Técnologias e Innovación ', styleT)
        worksheet.write('T7', 'Exporta', styleT)
        worksheet.write('U7', 'Teléfono 1 con Clave Lada', styleT)
        worksheet.write('V7', 'Teléfono 2 con Clave Lada', styleT)
        worksheet.write('W7', 'Correo Electrónico', styleT)
        worksheet.write('X7', 'Página Web', styleT)
        worksheet.write('Y7', 'Salutación', styleT)
        worksheet.write('Z7', 'Nombre', styleT)


        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin), ('name','!=','')], context=None)

            #pdb.set_trace()
        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
            #pdb.set_trace()
            if(row.name != ''):

                worksheet.write('A'+str(i), str(l), styleT)

                worksheet.write('D'+str(i), row.name, styleT)
                if(row.rfc != ''):
                    worksheet.write('E'+str(i), row.rfc, styleT)
                    worksheet.write('F'+str(i), row.rfc, styleT)
                if(row.Camara_Asociacion != ''):
                    worksheet.write('G'+str(i), row.Camara_Asociacion, styleT)
                if(row.country != ''):
                    worksheet.write('H'+str(i), row.country, styleT)
                if(row.operations != ''):
                    worksheet.write('K'+str(i), row.operations, styleT)
                if(row.colony != ''):
                    worksheet.write('J'+str(i), row.colony.name, styleT)
                if(row.cp != ''):
                    worksheet.write('K'+str(i), row.cp, styleT)
                if(row.town != ''):
                    worksheet.write('L'+str(i), row.town.name, styleT)
                if(row.town != ''):
                    worksheet.write('M'+str(i), row.town.name, styleT)
                if(row.sector != ''):
                    worksheet.write('N'+str(i), row.sector.name, styleT)
                if(row.Productos_Servicios != ''):
                    worksheet.write('O'+str(i), row.Productos_Servicios, styleT)
                if(row.sector != ''):
                    worksheet.write('P'+str(i), row.sector.name, styleT)
                if(row.staff != ''):
                    worksheet.write('Q'+str(i), row.staff, styleT)
                if(row.staff != ''):
                    worksheet.write('R'+str(i), row.staff, styleT)
                if(row.Tecnologia_Innovacion != ''):
                    worksheet.write('S'+str(i), row.Tecnologia_Innovacion, styleT)
                if(row.Exporta != ''):
                    worksheet.write('T'+str(i), row.Exporta, styleT)
                if(row.Asistente_Telefono1 != ''):
                    worksheet.write('U'+str(i), row.Asistente_Telefono1, styleT)
                if(row.Asistente_Telefono2 != ''):
                    worksheet.write('V'+str(i), row.Asistente_Telefono2, styleT)
                if(row.email != ''):
                    worksheet.write('W'+str(i), row.email, styleT)
                if(row.Pagina_Web != ''):
                    worksheet.write('X'+str(i), row.Pagina_Web, styleT)
                if(row.email != ''):
                    worksheet.write('Y'+str(i), row.email, styleT)
                if(row.Asistente_Nombre != ''):
                    worksheet.write('Z'+str(i), row.Asistente_Nombre, styleT)
                
                i = i + 1
                l = l + 1

        workbook.close()


        sprint_file = base64.b64encode(open("/tmp/Testing.xlsx", 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': 'Testing.xlsx',
            'datas': sprint_file,
            'datas_fname': 'Testing.xlsx',
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':'Testing.xlsx'})

        return True

    #~ Función que crea la hoja de calculo para el informe mensual
    def action_create_report2(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Informe IHCE Recepción', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, sheet_principal, data, context)
        # Creamos el nombre del archivo
        name = "Informe IHCE Recepcion.xls"
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
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        
        return True
    
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ EMPRENDIMIENTO
        sheet.write_merge(6, 6, 2, 9,("Instituto Hidalguense de Competitividad Empresarial "), styleGA)
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(7, 7, 2, 9,("Registro de entradas"), styleG)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 11
        courses_ids = self.pool.get('companies.ihce').search(cr, uid, [('write_uid','=',72),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        sheet.write(10, 2, ("Nombre"), styleGA)
        sheet.write(10, 3, ("Edad"), styleGA)
        sheet.write(10, 4, ("Email"), styleGA)
        sheet.write(10, 5, ("Telefono"), styleGA)
        sheet.write(10, 6, ("Sexo"), styleGA)
        sheet.write(10, 7, ("Fecha"), styleGA)

        for row in self.pool.get('companies.ihce').browse(cr, uid, courses_ids, context=None):
            anios = datetime.strptime(row.date, "%Y-%m-%d").date().year - datetime.strptime(row.date_birth, "%Y-%m-%d").date().year
            sheet.write(i, 2, row.name, style_n)
            sheet.write(i, 3, anios, style_n)
            sheet.write(i, 4, row.email, style_n)
            sheet.write(i, 5, row.cel_phone, style_n)
            sheet.write(i, 6, row.sexo, style_n)
            sheet.write(i, 7, row.date, style_n)
            if row.sexo == 'M':
                    hombres = hombres + 1
            
            if row.sexo == 'F':
                    mujeres = mujeres + 1

            i = i + 1

        sheet.write(10, 8, ("Total:"), styleV)
        sheet.write(10, 9, len(courses_ids), style_n)

        sheet.write(11, 8, ("Hombres:"), styleV)
        sheet.write(11, 9, hombres, style_n)

        sheet.write(12, 8, ("Mujeres:"), styleV)
        sheet.write(12, 9, mujeres, style_n)
        
        return sheet
    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
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

class reports_numeralia(osv.osv_memory):
    _name = "reports.numeralia"
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

    #~ Función que crea la hoja de calculo para el informe mensual
    def action_create_report(self, cr, uid, ids, context=None):
        uid = 1

        data = self.browse(cr, uid, ids[0], context=context)

        file_name = '/tmp/Numeralia.xlsx'

        workbook = xlsxwriter.Workbook(file_name)

        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        styleTitulosL = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12,  'left':1, 'bottom':1, 'top':1, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosR = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12,  'right':1, 'bottom':1, 'top':1, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulos = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosUp = workbook.add_format({'font_color': 'black', 'top':1, 'bottom':1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})

        styleTitulosDown = workbook.add_format({'font_color': 'black', 'top':1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bold':True})

        styleTitulosAll = workbook.add_format({'font_color': 'black', 'border': 1, 'align': 'horizontal center', 'font_size':12, 'align':'left', 'bg_color':'#d7eedb', 'bold':True})


        styleT = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 1, 'align':'left'})

        styleTa = workbook.add_format({'font_color': 'black','align': 'horizontal center', 'align':'center', 'border': 1, 'bg_color':'white', })

        styleT2 = workbook.add_format({'font_color': 'black', 'align': 'horizontal center', 'font_size':12, 'border': 0, 'align':'right', 'bold':True})

        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        # Create a new Chart object.
        chart = workbook.add_chart({'type': 'column'})


        asis_empre = 0
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        hombres = 0
        mujeres = 0
        i = 9
        l = 1
        m = 1

        worksheet.set_row(0, 30)
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 5)
        worksheet.set_column('C:C', 55)
        worksheet.set_column('D:D', 55)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 40)
        worksheet.set_column('K:K', 40)
        worksheet.set_column('L:L', 40)
        worksheet.set_column('M:M', 30)
        worksheet.set_column('N:N', 30)
        worksheet.set_column('O:O', 30)
        worksheet.set_column('P:P', 30)
        worksheet.set_column('Q:Q', 30)
        worksheet.set_column('R:R', 30)
        worksheet.set_column('S:S', 30)
        worksheet.set_column('T:T', 30)
        worksheet.set_column('U:U', 30)
        worksheet.set_column('V:V', 30)
        worksheet.set_column('W:W', 30)
        worksheet.set_column('X:X', 30)
        worksheet.set_column('Y:Y', 30)
        worksheet.set_column('Z:Z', 30)
        
        

        date_time = datetime.now()

        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align':'left'})
       
        
        worksheet.write('D2',"Reporte correspondiente del "+str(data.date_ini), styleT2)
        worksheet.write('E2'," Al  "+str(data.date_fin), styleT2)
        #worksheet.write('F4', date_time, date_format) 

        worksheet.write('A6', 'No.', styleTitulosAll)
        worksheet.write('B6', 'No.', styleTitulosAll)
        worksheet.write('C6', '', styleTitulosL)
        worksheet.write('D6', '', styleTitulosUp)
        worksheet.write('E6', 'Financiamiento(Pesos)', styleTitulosUp)
        worksheet.write('F6', '', styleTitulosUp)
        worksheet.write('G6', '', styleTitulosUp)
        worksheet.write('H6', '', styleTitulosR)
        worksheet.write('I6', '', styleTitulosL)
        worksheet.write('J6', 'Empresa o Emprendor Participante', styleTitulosUp)
        worksheet.write('K6', '', styleTitulosUp)
        worksheet.write('L6', '', styleTitulosUp)
        worksheet.write('M6', '', styleTitulosUp)
        worksheet.write('N6', '', styleTitulosUp)
        worksheet.write('O6', '', styleTitulosUp)
        worksheet.write('P6', '', styleTitulosUp)
        worksheet.write('Q6', '', styleTitulosUp)
        worksheet.write('R6', '', styleTitulosUp)
        worksheet.write('S6', '', styleTitulosUp)
        worksheet.write('T6', '', styleTitulosUp)
        worksheet.write('U6', '', styleTitulosUp)
        worksheet.write('V6', '', styleTitulosUp)
        worksheet.write('W6', '', styleTitulosR)



        worksheet.write('A7', '', styleTitulosAll)
        worksheet.write('B7', '', styleTitulosAll)
        worksheet.write('C7', 'Secretaria/Organismo', styleTitulosL)
        worksheet.write('D7', 'Nombre del curso', styleTitulosAll)
        worksheet.write('E7', 'Estatal', styleTitulosAll)
        worksheet.write('F7', 'Federal', styleTitulosAll)
        worksheet.write('G7', 'Privado', styleTitulosL)
        worksheet.write('H7', '', styleTitulosR)
        worksheet.write('I7', 'Empresario', styleTitulosL)
        worksheet.write('J7', '', styleTitulosR)
        worksheet.write('K7', 'Emprendedor', styleTitulosL)
        worksheet.write('L7', '', styleTitulosR)
        worksheet.write('M7', 'Otro', styleTitulosL)
        worksheet.write('N7', '', styleTitulosR)
        worksheet.write('O7', 'Nombre o Razon Social', styleTitulosAll)
        worksheet.write('P7', 'RFC', styleTitulosAll)
        worksheet.write('Q7', 'Municipio', styleTitulosAll)
        worksheet.write('R7', 'Giro', styleTitulosAll)
        worksheet.write('S7', 'Con actividades Cientificas', styleTitulosAll)
        worksheet.write('T7', 'Producto o Servicio Principal', styleTitulosAll)
        worksheet.write('U7', 'Empleador', styleTitulosAll)
        worksheet.write('V7', 'Subordinados', styleTitulosAll)
        worksheet.write('W7', 'Fecha del Rerporte', styleTitulosAll)
        

        worksheet.write('A8', '', styleTitulosAll)
        worksheet.write('B8', '', styleTitulosAll)
        worksheet.write('C8', '', styleTitulosL)
        worksheet.write('D8', '', styleTitulosAll)
        worksheet.write('E8', '', styleTitulosAll)
        worksheet.write('F8', '', styleTitulosAll)
        worksheet.write('G8', '', styleTitulosUp)
        worksheet.write('H8', 'Total', styleTitulosAll)

        worksheet.write('I8', 'Hombre', styleTitulosAll)
        worksheet.write('J8', 'Mujer', styleTitulosAll)

        worksheet.write('K8', 'Hombre', styleTitulosAll)
        worksheet.write('L8', 'Mujer', styleTitulosAll)

        worksheet.write('M8', 'Hombre', styleTitulosAll)
        worksheet.write('N8', 'Mujer', styleTitulosAll)
        
        worksheet.write('O8', '', styleTitulosAll)
        worksheet.write('P8', '', styleTitulosAll)
        worksheet.write('Q8', '', styleTitulosAll)
        worksheet.write('R8', '', styleTitulosAll)
        worksheet.write('S8', '', styleTitulosAll)
        worksheet.write('T8', '', styleTitulosAll)
        worksheet.write('U8', '', styleTitulosAll)
        worksheet.write('V8', '', styleTitulosAll)
        worksheet.write('W8', '', styleTitulosAll)


        hombre = 0
        mujer = 0

        hombreA = 0
        mujerA = 0


        courses_ids = self.pool.get('date.courses').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin), ('type','!=','consultoria'), ('state','=','done')], context=None)
            
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            worksheet.write('A'+str(i), str(l), styleTitulosDown)
            #pdb.set_trace()
            courses_id = self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)], context=None)
         
            for companyline in self.pool.get('company.line').browse(cr, uid, courses_id, context=None): 
                worksheet.write('B'+str(i), '', styleT)
                worksheet.write('C'+str(i), '', styleT)
                worksheet.write('D'+str(i), '', styleT)
                worksheet.write('E'+str(i), '', styleT)
                worksheet.write('F'+str(i), '', styleT)
                worksheet.write('G'+str(i), '', styleT)
                worksheet.write('H'+str(i), '', styleT)
                worksheet.write('I'+str(i), '', styleT)
                worksheet.write('J'+str(i), '', styleT)
                worksheet.write('K'+str(i), '', styleT)
                worksheet.write('L'+str(i), '', styleT)
                worksheet.write('M'+str(i), '', styleT)
                worksheet.write('N'+str(i), '', styleT)
                worksheet.write('O'+str(i), '', styleT)
                worksheet.write('P'+str(i), '', styleT)
                worksheet.write('Q'+str(i), '', styleT)
                worksheet.write('R'+str(i), '', styleT)
                worksheet.write('S'+str(i), '', styleT)
                worksheet.write('T'+str(i), '', styleT)
                worksheet.write('U'+str(i), '', styleT)
                worksheet.write('V'+str(i), '', styleT)
                worksheet.write('W'+str(i), '', styleT)






                worksheet.write('B'+str(i), str(m), styleT)
                worksheet.write('C'+str(i), ('INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL'), styleT)
                worksheet.write('D'+str(i), row.name, styleT)
                worksheet.write('Q'+str(i), row.municipio.name, styleT)
                worksheet.write('W'+str(i), row.date, styleT)
                

                if(companyline.company_id.id != False):
                    companyline.company_id.sexo
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',companyline.company_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)
                    if(company.type=='fisica'):
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT) 
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    if(company.type=='moral'):
                        worksheet.write('P'+str(i), company.rfc, styleT) 
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT)
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    if(company.type=='emprendedor'):
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT)
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    worksheet.write('O'+str(i), company.name, styleT)
                    worksheet.write('P'+str(i), ('Información no solicitada en un taller de capacitación'), styleT)
                    worksheet.write('S'+str(i), (''), styleT)
                    worksheet.write('T'+str(i), (''), styleT)
                    worksheet.write('U'+str(i), ('X'), styleT)

                else:
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',companyline.contact_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)
                    if(company.type=='fisica'):
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT)
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    if(company.type=='moral'):
                        worksheet.write('P'+str(i), company.rfc, styleT) 
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT)
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    if(company.type=='emprendedor'):
                        if(company.sexo == 'M'):
                            hombre = hombre + 1
                            worksheet.write('I'+str(i), ('X'), styleT)
                        if(company.sexo == 'F'):
                            mujer = mujer + 1
                            worksheet.write('J'+str(i), ('X'), styleT)
                    worksheet.write('O'+str(i), company.name, styleT)
                    worksheet.write('P'+str(i), ('Información no solicitada en un taller de capacitación'), styleT)
                    worksheet.write('S'+str(i), (''), styleT)
                    worksheet.write('T'+str(i), (''), styleT)
                    worksheet.write('U'+str(i), ('X'), styleT)

                m = m + 1
                i = i + 1

            courses_id = self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)], context=None)
            
            for listnewpersons in self.pool.get('list.new.persons').browse(cr, uid, courses_id, context=None):
                worksheet.write('B'+str(i), '', styleT)
                worksheet.write('C'+str(i), '', styleT)
                worksheet.write('D'+str(i), '', styleT)
                worksheet.write('E'+str(i), '', styleT)
                worksheet.write('F'+str(i), '', styleT)
                worksheet.write('G'+str(i), '', styleT)
                worksheet.write('H'+str(i), '', styleT)
                worksheet.write('I'+str(i), '', styleT)
                worksheet.write('J'+str(i), '', styleT)
                worksheet.write('K'+str(i), '', styleT)
                worksheet.write('L'+str(i), '', styleT)
                worksheet.write('M'+str(i), '', styleT)
                worksheet.write('N'+str(i), '', styleT)
                worksheet.write('O'+str(i), '', styleT)
                worksheet.write('P'+str(i), '', styleT)
                worksheet.write('Q'+str(i), '', styleT)
                worksheet.write('R'+str(i), '', styleT)
                worksheet.write('S'+str(i), '', styleT)
                worksheet.write('T'+str(i), '', styleT)
                worksheet.write('U'+str(i), '', styleT)
                worksheet.write('V'+str(i), '', styleT)
                worksheet.write('W'+str(i), '', styleT)
                worksheet.write('B'+str(i), str(m), styleT)
                worksheet.write('C'+str(i), ('INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL'), styleT)
                worksheet.write('D'+str(i), row.name, styleT)
                worksheet.write('Q'+str(i), row.municipio.name, styleT)
                worksheet.write('W'+str(i), row.date, styleT)

                #pdb.set_trace()
                if(listnewpersons.id != False):
                    if(listnewpersons.sexo == 'M'):
                        hombreA = hombreA + 1
                        worksheet.write('K'+str(i), ('X'), styleT)
                    if(listnewpersons.sexo == 'F'):
                        mujerA = mujerA + 1
                        worksheet.write('L'+str(i), ('X'), styleT)

                worksheet.write('O'+str(i), listnewpersons.name, styleT)
                worksheet.write('P'+str(i), ('Información no solicitada en un taller de capacitación'), styleT)
                worksheet.write('S'+str(i), (''), styleT)
                worksheet.write('T'+str(i), (''), styleT)
                worksheet.write('U'+str(i), ('X'), styleT)
                
                m = m + 1
                i = i + 1

            
            
            l = l + 1


        hombre = hombre + hombreA
        mujer = mujer + mujerA

        worksheet.write('C'+str(i+10), str('Hombre:  ')+str(hombre), styleT2)
        worksheet.write('C'+str(i+11), str('Mujer:  ')+str(mujer), styleT2)

        workbook.close()


        sprint_file = base64.b64encode(open("/tmp/Numeralia.xlsx", 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': 'Testing.xlsx',
            'datas': sprint_file,
            'datas_fname': 'Testing.xlsx',
            'description': 'Informe Mensual IHCE',
            'res_model': 'reports.ihce',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':'Numeralia.xlsx'})

        return True

    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
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



