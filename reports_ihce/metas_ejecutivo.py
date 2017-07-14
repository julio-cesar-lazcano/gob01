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

class metas_ejecutivo(osv.osv_memory):
    _name = "metas.ejecutivo"

    _columns = {
        'name':fields.text('Instrucciones'),
        'anio': fields.selection([('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'), ('2051', '2051'), ('2052', '2052'), ('2053', '2053'), ('2054', '2054'), ('2055', '2055'), ('2056', '2056'), ('2057', '2057'), ('2058', '2058'), ('2059', '2059'), ('2060', '2060'), ('2061', '2061'), ('2062', '2062'), ('2063', '2063'), ('2064', '2064'), ('2065', '2065'), ('2066', '2066'), ('2067', '2067'), ('2068', '2068'), ('2069', '2069'), ('2070', '2070'), ('2071', '2071'), ('2072', '2072'), ('2073', '2073'), ('2074', '2074'), ('2075', '2075'), ('2076', '2076'), ('2077', '2077'), ('2078', '2078'), ('2079', '2079'), ('2080', '2080')], 'Año'),
        'xls_file_name':fields.char('xls file name', size=128),
        'xls_file':fields.binary('Archivo', readonly=True),
        'user_id': fields.many2one('res.users',"Responsable"),
    }

    _defaults = {
        'name': "Se creara un archivo .xls con el reporte seleccionado.",
        'user_id': lambda obj, cr, uid, context: uid,
    }
    
     #~ Función que crea la hoja de calculo para el reportes
    def action_create_report(self, cr, uid, ids, context=None):
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Metas Ejecutivo', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Metas Ejecutivo.xls"
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
            'description': 'Reporte Metas Ejecutivo',
            'res_model': 'metas.ejecutivo',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        return True
    
    #~ Función que llena la hoja con los datos correspondientes del reporte
    def create_principal_sheet(self, cr, uid, ids, sheet, context={}):
        data = self.browse(cr, uid, ids[0], context=context)

        sheet.col(0).width = 8000
        sheet.col(1).width = 5000
        sheet.col(2).width = 8000
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center; '))
        style = xlwt.easyxf(('font: height 180, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour gray40;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 27,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        
        sheet.write_merge(1, 1, 0, 27,("Resumen anteproyecto del programa operativo anual " + str(data.anio)), styleT)
        sheet.write_merge(2, 2, 0, 27,("PROYECTOS"), styleT)

        #TITULOS
        sheet.write_merge(5, 6, 0, 0, 'PROYECTO', style)
        sheet.write_merge(5, 6, 1, 1, 'TIPO DE INDICADOR', style)
        sheet.write_merge(5, 6, 2, 2,'UNIDAD DE MEDIDA', style)
        sheet.write_merge(5, 6, 3, 3,'META ANUAL PROGRAMADA', style)
        sheet.write_merge(5, 5, 4, 5, 'ENERO', style)
        sheet.write(6, 4, 'META', style)
        sheet.write(6, 5, 'REAL', style)
        sheet.write_merge(5, 5, 6, 7, 'FEBRERO', style)
        sheet.write(6, 6, 'META', style)
        sheet.write(6, 7, 'REAL', style)
        sheet.write_merge(5, 5, 8, 9, 'MARZO', style)
        sheet.write(6, 8, 'META', style)
        sheet.write(6, 9, 'REAL', style)
        sheet.write_merge(5, 5, 10,11, 'ABRIL', style)
        sheet.write(6, 10, 'META', style)
        sheet.write(6, 11, 'REAL', style)
        sheet.write_merge(5, 5, 12, 13, 'MAYO', style)
        sheet.write(6, 12, 'META', style)
        sheet.write(6, 13, 'REAL', style)
        sheet.write_merge(5, 5, 14, 15, 'JUNIO', style)
        sheet.write(6, 14, 'META', style)
        sheet.write(6, 15, 'REAL', style)
        sheet.write_merge(5, 5, 16, 17, 'JULIO', style)
        sheet.write(6, 16, 'META', style)
        sheet.write(6, 17, 'REAL', style)
        sheet.write_merge(5, 5, 18, 19, 'AGOSTO', style)
        sheet.write(6, 18, 'META', style)
        sheet.write(6, 19, 'REAL', style)
        sheet.write_merge(5, 5, 20, 21, 'SEPTIEMBRE', style)
        sheet.write(6, 20, 'META', style)
        sheet.write(6, 21, 'REAL', style)
        sheet.write_merge(5, 5, 22, 23, 'OCTUBRE', style)
        sheet.write(6, 22, 'META', style)
        sheet.write(6, 23, 'REAL', style)
        sheet.write_merge(5, 5, 24, 25, 'NOVIEMBRE', style)
        sheet.write(6, 24, 'META', style)
        sheet.write(6, 25, 'REAL', style)
        sheet.write_merge(5, 5, 26, 27, 'DICIEMBRE', style)
        sheet.write(6, 26, 'META', style)
        sheet.write(6, 27, 'REAL', style)
        
        sheet.write_merge(7, 9, 0, 0, 'Acompañamiento Empresarial Ejecutado', style_n)
        sheet.write(7, 1, 'Componente', style_n)
        sheet.write(7, 2, 'Servicios Empresariales', style_n)
        sheet.write(8, 1, 'Actividad', style_n)
        sheet.write(8, 2, 'Asesorías', style_n)
        sheet.write(9, 1, 'Actividad', style_n)
        sheet.write(9, 2, 'Mujeres', style_n)
        sheet.write(10, 2, 'Hombres', style_n)
        sheet.write_merge(11, 13, 0, 0, 'Formación de Capital Humano Ejecutado', style_n)
        sheet.write(11, 1, 'Componente', style_n)
        sheet.write(11, 2, 'Eventos', style_n)
        sheet.write(12, 1, 'Actividad', style_n)
        sheet.write(12, 2, 'Asistentes', style_n)
        sheet.write(13, 1, 'Actividad', style_n)
        sheet.write(13, 2, 'Mujeres', style_n)
        sheet.write(14, 2, 'Hombres', style_n)
        sheet.write_merge(15, 17, 0, 0, 'Fortalecimiento de la Red de Centros de Desarrollo Empresarial (EMPRERED)', style_n)
        sheet.write(15, 1, 'Componente', style_n)
        sheet.write(15, 2, 'Emprered en operación', style_n)
        sheet.write(16, 1, 'Actividad', style_n)
        sheet.write(16, 2, 'Asesorías', style_n)
        sheet.write(17, 1, 'Actividad', style_n)
        sheet.write(17, 2, 'Mujeres', style_n)
        sheet.write(18, 2, 'Hombres', style_n)


        anio = datetime.now().year
        #~ LEEMOS LAS METAS ANUALES SI EXISTEN
        meta_ids = self.pool.get('meta.anual.ejecutivo').search(cr, uid, [('activo','=',True),('anio_ihce','=',anio)])

        servicios  = 0
        asesorias  = 0
        hombreA = 0
        mujerA = 0
        cursos  = 0
        asistentes  = 0
        hombreC = 0
        mujerC = 0
        asesorias_emprered = 0
        hombreE = 0
        mujerE = 0

        if meta_ids:
            meta_id = self.pool.get('meta.anual.ejecutivo').browse(cr, uid, meta_ids[0], context=context)

            col = 4
            for row in meta_id.lines:
                fila = 7
                
                sheet.write(fila, col, row.servicios_empresariales, style_n)
                servicios += row.servicios_empresariales
                
                ser_id = self.pool.get('indicador.servicios.empresariales').browse(cr, uid, 1)
                sheet = self.meses(cr, uid, ser_id, row.mes, fila, (col+1), sheet, style_n, context=context)

                fila = fila + 1
                sheet.write(fila, col, row.asesoria_empresarial, style_n)
                asesorias += row.asesoria_empresarial
                
                ser_id = self.pool.get('indicador.servicios.empresariales').browse(cr, uid, 2)
                sheet = self.meses(cr, uid, ser_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                fila = fila + 1
                sheet.write(fila, col, row.mujeres_empresarial, style_n)
                mujerA += row.mujeres_empresarial

                ser_id = self.pool.get('indicador.servicios.empresariales').browse(cr, uid, 3)
                sheet = self.meses(cr, uid, ser_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                fila = fila + 1
                sheet.write(fila, col, row.hombres_empresarial, style_n)
                hombreA += row.hombres_empresarial
                
                ser_id = self.pool.get('indicador.servicios.empresariales').browse(cr, uid, 4)
                sheet = self.meses(cr, uid, ser_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                fila = fila + 1
                
                sheet.write(fila, col, row.eventos, style_n)
                curso_id = self.pool.get('indicador.capital.humano').browse(cr, uid, 3)
                cursos += row.eventos
                
                sheet = self.meses(cr, uid, curso_id, row.mes, fila, (col+1), sheet, style_n, context=context)

                fila = fila + 1

                sheet.write(fila, col, row.asistentes, style_n)
                asistentes += row.asistentes
                
                asis_id = self.pool.get('indicador.capital.humano').browse(cr, uid, 5)
                sheet = self.meses(cr, uid, asis_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                fila = fila + 1
                sheet.write(fila, col, row.mujeres_cursos, style_n)
                mujerC += row.mujeres_cursos
                
                asis_id = self.pool.get('indicador.capital.humano').browse(cr, uid, 6)
                sheet = self.meses(cr, uid, asis_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                fila = fila + 1
                
                sheet.write(fila, col, row.hombres_cursos, style_n)
                hombreC += row.hombres_cursos
                
                asis_id = self.pool.get('indicador.capital.humano').browse(cr, uid, 7)
                sheet = self.meses(cr, uid, asis_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                
                sheet.write(fila, col, row.emprereds, style_n)
                
                fila = fila + 1
                fila = fila + 1
                
                sheet.write(fila, col, row.asesoria_emprered, style_n)
                asesorias_emprered += row.asesoria_emprered
                
                ase_id = self.pool.get('indicador.total.emprered').browse(cr, uid, 5)
                sheet = self.meses(cr, uid, ase_id, row.mes, fila, (col+1), sheet, style_n, context=context)

                fila = fila + 1
                
                sheet.write(fila, col, row.mujeres_emprered, style_n)
                mujerE += row.mujeres_emprered
                
                ase_id = self.pool.get('indicador.total.emprered').browse(cr, uid, 6)
                sheet = self.meses(cr, uid, ase_id, row.mes, fila, (col+1), sheet, style_n, context=context)

                fila = fila + 1
                
                sheet.write(fila, col, row.hombres_emprered, style_n)
                hombreE += row.hombres_emprered
                
                ase_id = self.pool.get('indicador.total.emprered').browse(cr, uid, 7)
                sheet = self.meses(cr, uid, ase_id, row.mes, fila, (col+1), sheet, style_n, context=context)
                
                col = col + 2

            sheet.write(7, 3, servicios, style_n)
            sheet.write(8, 3, asesorias, style_n)
            sheet.write(9, 3, mujerA, style_n)
            sheet.write(10, 3, hombreA, style_n)
            sheet.write(11, 3, cursos, style_n)
            sheet.write(12, 3, asistentes, style_n)
            sheet.write(13, 3, mujerC, style_n)
            sheet.write(14, 3, hombreC, style_n)
            sheet.write(16, 3, asesorias_emprered, style_n)
            sheet.write(17, 3, mujerE, style_n)
            sheet.write(18, 3, hombreE, style_n)
    
        return sheet

    def meses(self, cr, uid, indi, mes, fila, col, sheet, style_n, context=None):
        if mes == 1:
            sheet.write(fila, col, str(indi.enero), style_n)
        elif mes == 2:
            sheet.write(fila, col, str(indi.febrero), style_n)
        elif mes == 3:
            sheet.write(fila, col, str(indi.marzo), style_n)
        elif mes == 4:
            sheet.write(fila, col, str(indi.abril), style_n)
        elif mes == 5:
            sheet.write(fila, col, str(indi.mayo), style_n)
        elif mes == 6:
            sheet.write(fila, col, str(indi.junio), style_n)
        elif mes == 7:
            sheet.write(fila, col, str(indi.julio), style_n)
        elif mes == 8:
            sheet.write(fila, col, str(indi.agosto), style_n)
        elif mes == 9:
            sheet.write(fila, col, str(indi.septiembre), style_n)
        elif mes == 10:
            sheet.write(fila, col, str(indi.octubre), style_n)
        elif mes == 11:
            sheet.write(fila, col, str(indi.noviembre), style_n)
        elif mes == 12:
            sheet.write(fila, col, str(indi.diciembre), style_n)

        return sheet
