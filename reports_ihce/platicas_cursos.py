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
from datetime import datetime, date, timedelta
import time

class reporte_platicas_cursos(osv.osv_memory):
    _name = "reporte.platicas.cursos"
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
        sheet_principal = workbook.add_sheet('Platicas y Cursos', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "PlaticasYCursos.xls"
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
            'description': 'Reporte Platicas y Cursos',
            'res_model': 'reporte.platicas.cursos',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        return True
    
    #~ Función que llena la hoja con los datos correspondientes del reporte
    def create_principal_sheet(self, cr, uid, ids, sheet, context={}):
        data = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now().date()
        anio = fecha_actual.year
        
        # Damos tamaños a las columnas
        sheet.col(0).width = 1500
        sheet.col(1).width = 1500
        sheet.col(2).width = 10000
        sheet.col(3).width = 3000
        sheet.col(4).width = 5000
        sheet.col(5).width = 3000
        sheet.col(6).width = 5000
        sheet.col(7).width = 8000
        sheet.col(8).width = 4000
        sheet.col(9).width = 8000
        sheet.col(10).width = 4000
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        style = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour Lavender;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        style2 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour coral;'))
        style3 = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 10,("SECRETARÍA DE DESARROLLO ECONÓMICO DEL GOBIERNO DEL ESTADO DE HIDALGO"), styleT)
        sheet.write_merge(1, 1, 0, 10,("INSITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 10,("DIRECCIÓN DE ACOMPAÑAMIENTO EMPRESARIAL"), styleT)
        sheet.write_merge(3, 3, 0, 10,("CAPACITACION"), styleT)
        
        #TITULOS
        sheet.write(5, 0, 'CONTROL POR MES', style)
        sheet.write(5, 1, 'No.', style)
        sheet.write(5, 2, 'NOMBRE DE USUARIO', style)
        sheet.write(5, 3, 'SEXO', style)
        sheet.write(5, 4, 'NIVEL ESCOLAR', style)
        sheet.write(5, 5, 'EDAD', style)
        sheet.write(5, 6, 'MUNICIPIO', style)
        sheet.write(5, 7, 'IDEA DE NEGOCIO', style)
        sheet.write(5, 8, 'CAPACITACION', style)
        sheet.write(5, 9, 'NOMBRE DEL CURSO/PLATICA', style)
        sheet.write(5, 10, 'MES DE REGISTRO', style)
        
        i = 7
        a = 1
        b = 1
        
        if data.type == 'completo':
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('services','=', 'emprendimiento'),('type','!=','consultoria'),('dependence','=','ihce')], order='date ASC')
        else:
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('services','=', 'emprendimiento'),('type','!=','consultoria'),('date','>=',data.date_ini),('date','<=',data.date_fin),('dependence','=','ihce')], order='date ASC')
            
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context):
            mes1 = self.month(cr, uid, row.date[5:7], context)
            if i == 7:
                sheet.write_merge(6, 6, 0, 10,(mes1), styleG)
            else:
                if mes != mes1:
                    sheet.write_merge(i, i, 0, 10,(mes1), styleG)
                    i+=1
                    b = 1
                    
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('company.line').browse(cr, uid, line)
                ro = self.pool.get('companies.ihce').browse(cr, uid, li.contact_id.id, context)
               
                sheet.write(i, 0, a, style_n)
                sheet.write(i, 1, b, style_n)
                sheet.write(i, 2, ro.name or '', style_n)
                sheet.write(i, 3, ro.sexo or '', style_n)
                esco = self.pool.get('escolaridad').browse(cr, uid, ro.school.id, context)
                sheet.write(i, 4, esco.name or '', style_n)
                if ro.date_birth:
                    fecha_naci = datetime.strptime(ro.date_birth, "%Y-%m-%d").date().year
                    anios = anio - fecha_naci
                    sheet.write(i, 5, (str(anios) + " años") or '', style_n)
                muni = self.pool.get('town.hidalgo').browse(cr, uid, ro.town.id, context)
                sheet.write(i, 6, muni.name or '', style_n)
                sheet.write(i, 7, ro.idea_commerce or '', style_n)
                sheet.write(i, 8, row.type or '', style_n)
                sheet.write(i, 9, row.name.encode('utf-8') or '', style_n)
                sheet.write(i, 10, mes1 + '-' + str(row.date[0:4]) or '', style_n)
           
                i= i +1
                a = a + 1
                b = b + 1
                mes = mes1
                
            for line in self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('list.new.persons').browse(cr, uid, line)
               
                sheet.write(i, 0, a, style_n)
                sheet.write(i, 1, b, style_n)
                sheet.write(i, 2, li.name or '', style_n)
                sheet.write(i, 3, li.sexo or '', style_n)
                sheet.write(i, 4, '', style_n)
                sheet.write(i, 5, '', style_n)
                muni = self.pool.get('town.hidalgo').browse(cr, uid, li.town.id, context)
                sheet.write(i, 6, muni.name or '', style_n)
                sheet.write(i, 7, li.idea_commerce or '', style_n)
                sheet.write(i, 8, row.type or '', style_n)
                sheet.write(i, 9, row.name.encode('utf-8') or '', style_n)
                sheet.write(i, 10, mes1 + '-' + str(row.date[0:4]) or '', style_n)
           
                i= i +1
                a = a + 1
                b = b + 1
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
