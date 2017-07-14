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

class reporte_regiones(osv.osv_memory):
    _name = "reporte.regiones"

    _columns = {
        'name':fields.text('Instrucciones'),
        'type': fields.selection([('completo', 'Completo'), ('rango', 'Por región')], 'Tipo de reporte'),
        'region': fields.many2one('region.hidalgo','Región'),
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
        sheet_principal = workbook.add_sheet('Reporte de regiones', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Reporte de regiones.xls"
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
            'description': 'Reporte de regiones',
            'res_model': 'reporte.regiones',
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
        sheet.col(0).width = 5000
        sheet.col(1).width = 7000

       #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center; '))
        styleD = xlwt.easyxf(('font: height 180, bold 1, color black; alignment: horizontal center; '))
        style = xlwt.easyxf(('font: height 180, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 5,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
        
        #TITULOS
        sheet.write(4, 0, 'Región', style)
        sheet.write(4, 1, 'Municipio', style)
        sheet.write(4, 2, 'Asesorías', style)
        sheet.write(4, 3, 'Servicios', style)
        sheet.write(4, 4, 'Asistentes', style)
        sheet.write(4, 5, '', style)
        
        regiones_ids = []
        
        if data.type == 'rango':
            sheet.write_merge(1, 1, 0, 5,("Región " + data.region.name.encode('utf-8')), styleT)
            regiones_ids.append(data.region.id)
        else:
            regiones_ids = self.pool.get('region.hidalgo').search(cr, uid, [])
        
        i = 5
        
        for re in regiones_ids:
            company_asesorias = []
            company_servicios = []
            company_asistentes = []
            con = 0
            suma = 0
        
            municipios_ids = self.pool.get('town.hidalgo').search(cr, uid, [('region_id','=',re)])
            municipios = self.pool.get('town.hidalgo').browse(cr, uid, municipios_ids)
            
            asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin)])
            servicios_ids = self.pool.get('servicios.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin)])
            cursos_ids = self.pool.get('date.courses').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('state','=','done')])
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)])
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)])
            patente_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)])
            fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)])
                
            regiones = self.pool.get('region.hidalgo').browse(cr, uid, re)
        
            sheet.write(i, 0, regiones.name.encode('utf-8'), style_n)
                
            for muni in municipios:
                con = 0
                suma = 0
                sheet.write(i, 1, muni.name.encode('utf-8'), style_n)
                
                for line in self.pool.get('asesorias.ihce').browse(cr, uid, asesoria_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_asesorias.append(company_row.id)
                
                
                sheet.write(i, 2, str(con), style_n)
                
                suma = con
                con = 0
                
                for line in self.pool.get('servicios.ihce').browse(cr, uid, servicios_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_servicios:
                            if li == company_row.id:
                                ban = False
                                break
                        
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_servicios.append(company_row.id)
                
                for line in self.pool.get('register.trademark').browse(cr, uid, register_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_servicios:
                            if li == company_row.id:
                                ban = False
                                break
                        
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_servicios.append(company_row.id)
                
                for line in self.pool.get('bar.code').browse(cr, uid, bar_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_servicios:
                            if li == company_row.id:
                                ban = False
                                break
                        
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_servicios.append(company_row.id)
                
                for line in self.pool.get('patent.ihce').browse(cr, uid, patente_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_servicios:
                            if li == company_row.id:
                                ban = False
                                break
                        
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_servicios.append(company_row.id)
                            
                for line in self.pool.get('fda.ihce').browse(cr, uid, fda_ids):
                    company_row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
                    if company_row.town_company.id == muni.id:
                        ban = True
                        for li in company_servicios:
                            if li == company_row.id:
                                ban = False
                                break
                        
                        for li in company_asesorias:
                            if li == company_row.id:
                                ban = False
                                break
                    
                        if ban:
                            con = con + 1
                            company_servicios.append(company_row.id)
                            
                
                sheet.write(i, 3, str(con), style_n)
                
                suma += con
                
                con = 0
                
                for cur in self.pool.get('date.courses').browse(cr, uid, cursos_ids):
                    for per in cur.line:
                        personas_row = self.pool.get('company.line').browse(cr, uid, per.id)
                        company_row = self.pool.get('companies.ihce').browse(cr, uid, personas_row.company_id.id)
                        if company_row.town_company.id == muni.id:
                            ban = True
                            for li in company_asistentes:
                                if li == company_row.id:
                                    ban = False
                                    break
                            
                            for li in company_servicios:
                                if li == company_row.id:
                                    ban = False
                                    break
                            
                            for li in company_asesorias:
                                if li == company_row.id:
                                    ban = False
                                    break
                        
                            if ban:
                                con = con + 1
                                company_asistentes.append(company_row.id)
                
                    for per in cur.list_lines:
                        personas_row = self.pool.get('list.new.persons').browse(cr, uid, per.id)
                        if personas_row.town.id == muni.id:
                            con = con + 1
                            company_asistentes.append(personas_row.id)
                                
                
                sheet.write(i, 4, str(con), style_n)
                
                suma += con
                
                sheet.write(i, 5, str(suma), style_n)
                
                i = i + 1
            
            i = i + 1
            sheet.write(i, 2, str(len(company_asesorias)), styleD)
            sheet.write(i, 3, str(len(company_servicios)), styleD)
            sheet.write(i, 4, str(len(company_asistentes)), styleD)
            sheet.write(i, 5, str(len(company_asesorias) + len (company_servicios) + len(company_asistentes)), styleD)
            
            i = i + 2
            
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
