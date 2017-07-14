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

class reporte_resultados(osv.osv_memory):
    _name = "reporte.resultados"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _columns = {
        'name':fields.text('Instrucciones'),
        'type': fields.selection([('completo', 'Completo'), ('rango', 'Por fecha')], 'Tipo de reporte'),
        'date': fields.date('Fecha de reporte'),
        'anio': fields.selection([('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'), ('2051', '2051'), ('2052', '2052'), ('2053', '2053'), ('2054', '2054'), ('2055', '2055'), ('2056', '2056'), ('2057', '2057'), ('2058', '2058'), ('2059', '2059'), ('2060', '2060'), ('2061', '2061'), ('2062', '2062'), ('2063', '2063'), ('2064', '2064'), ('2065', '2065'), ('2066', '2066'), ('2067', '2067'), ('2068', '2068'), ('2069', '2069'), ('2070', '2070'), ('2071', '2071'), ('2072', '2072'), ('2073', '2073'), ('2074', '2074'), ('2075', '2075'), ('2076', '2076'), ('2077', '2077'), ('2078', '2078'), ('2079', '2079'), ('2080', '2080')], 'Año'),
        'xls_file_name':fields.char('xls file name', size=128),
        'xls_file':fields.binary('Archivo', readonly=True),
    }

    _defaults = {
        'name': "Control de Indicadores",
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    #~ Función que crea la hoja de calculo para el reportes
    def action_create_report(self, cr, uid, ids, context=None):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Resultados', cell_overwrite_ok=True)
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        name = "Resultados.xls"
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
            'description': 'Resultados',
            'res_model': 'reporte.resultados',
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
        sheet.col(0).width = 8000
        sheet.col(1).width = 2000
        sheet.col(2).width = 2000
        sheet.col(3).width = 2000
        sheet.col(4).width = 2000
        sheet.col(5).width = 2000
        sheet.col(6).width = 2000
        sheet.col(7).width = 2000
        sheet.col(8).width = 2000
        sheet.col(9).width = 2000
        sheet.col(10).width = 2000
        sheet.col(11).width = 2000
        sheet.col(12).width = 2000
        sheet.col(13).width = 2000
        sheet.col(14).width = 2000
        sheet.col(15).width = 2000
        sheet.col(16).width = 2000
        sheet.col(17).width = 2000
        sheet.col(18).width = 2000
        sheet.col(19).width = 2000
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleG = xlwt.easyxf(('font: height 200, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 19,("Resultados de la Dirección de Acompañamiento y Formación Empresarial"), styleT)
        sheet.write_merge(1, 1, 0, 19, str(data.anio), styleT)
        
        fila = 2
        
        anio = datetime.now().year
        #~ LEEMOS LAS METAS ANUALES SI EXISTEN
        meta_ids = self.pool.get('meta.anual.ihce').search(cr, uid, [('activo','=',True),('anio_ihce','=',anio)])
        
        if meta_ids:
            
            meta_row = self.pool.get('meta.anual.ihce').browse(cr, uid, meta_ids[0])
            
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRENDIMIENTO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            sheet.write(fila, 0, 'EMPRENDIMIENTO', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Diagnósticos', style_n)
            sheet.write(fila, 1, meta_row.diagnosticos, style_n)
            
            company_ids_ase = self.pool.get('companies.ihce').search(cr, uid, [('dependence','=','0'),('state','=','done'),('company','=',True),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], order='date ASC')
            
            
            if company_ids_ase:
                sheet = self.sumando(cr, uid, 'companies.ihce', company_ids_ase, fila, sheet, meta_row.diagnosticos, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Emprendedores de Alto Impacto', style_n)
            sheet.write(fila, 1, 0, style_n)
            sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asesoría a Emprendedores', style_n)
            sheet.write(fila, 1, meta_row.asesoria_emprendedores, style_n)
            
            asesorias_empre_ids = self.pool.get('entrepreneurship.ihce').search(cr, uid, [('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce'),('asesoria','!=',0)], order='date ASC')
            
            if asesorias_empre_ids:
                sheet = self.sumando(cr, uid, 'entrepreneurship.ihce', asesorias_empre_ids, fila, sheet, meta_row.asesoria_emprendedores, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ ---------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos, Talleres, Diplomados', style_n)
            sheet.write(fila, 1, meta_row.cursos_emprendimiento, style_n)
            
            courses_empre_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','emprendimiento'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('type','in',('curso','taller','diplomado'))], context=None)
            
            if courses_empre_ids:
                sheet = self.sumando(cr, uid, 'date.courses', courses_empre_ids, fila, sheet, meta_row.cursos_emprendimiento, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ ----------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asistentes', style_n)
            sheet.write(fila, 1, meta_row.asistentes_emprendimiento, style_n)
            
            if courses_empre_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', courses_empre_ids, fila, sheet, meta_row.asistentes_emprendimiento, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
                
            
            #~ ---------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Pláticas', style_n)
            sheet.write(fila, 1, meta_row.platicas_emprendimiento, style_n)
            
            plati_empre_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','emprendimiento'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('type','=','platica')], context=None)
            
            if plati_empre_ids:
                sheet = self.sumando(cr, uid, 'date.courses', plati_empre_ids, fila, sheet, meta_row.platicas_emprendimiento, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ ----------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asistentes', style_n)
            sheet.write(fila, 1, meta_row.asistentes_platicas_emprendimiento, style_n)
            
            if plati_empre_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', plati_empre_ids, fila, sheet, meta_row.asistentes_platicas_emprendimiento, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DESARROLLO EMPRESARIAL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'DESARROLLO EMPRESARIAL', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            #~ ----------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'ASESORÍAS EMPRESARIALES', style_n)
            sheet.write_merge(fila, fila, 1, 19, '', style_n)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Registro de Marca', style_n)
            sheet.write(fila, 1, meta_row.asesoria_registro_marca, style_n)
            
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('asesoria','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if register_ids:
                sheet = self.sumando(cr, uid, 'register.trademark', register_ids, fila, sheet, meta_row.asesoria_registro_marca, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Patentes', style_n)
            sheet.write(fila, 1, meta_row.asesoria_patente, style_n)
            
            patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('asesoria','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if patent_ids:
                sheet = self.sumando(cr, uid, 'patent.ihce', patent_ids, fila, sheet, meta_row.asesoria_patente, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Códigos de Barras', style_n)
            sheet.write(fila, 1, meta_row.asesoria_codigo, style_n)
            
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('asesoria','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if bar_ids:
                sheet = self.sumando(cr, uid, 'bar.code', bar_ids, fila, sheet, meta_row.asesoria_codigo, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'SERVICIOS EMPRESARIALES', style_n)
            sheet.write_merge(fila, fila, 1, 19, '', style_n)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Registro de Marca', style_n)
            sheet.write(fila, 1, meta_row.servicio_registro_marca, style_n)
            
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if register_ids:
                sheet = self.sumando(cr, uid, 'register.trademark', register_ids, fila, sheet, meta_row.servicio_registro_marca, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Patentes', style_n)
            sheet.write(fila, 1, meta_row.servicio_patente, style_n)
            
            patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if patent_ids:
                sheet = self.sumando(cr, uid, 'patent.ihce', patent_ids, fila, sheet, meta_row.servicio_patente, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Códigos de Barras', style_n)
            sheet.write(fila, 1, meta_row.servicio_membresias, style_n)
            
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if bar_ids:
                sheet = self.sumando(cr, uid, 'bar.code', bar_ids, fila, sheet, meta_row.servicio_membresias, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
                
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Pruebas de laboratorio/tabla nutrimental', style_n)
            sheet.write(fila, 1, meta_row.servicio_tabla_nutrimental, style_n)
            
            fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','ihce')], order='date ASC')
            
            if fda_ids:
                sheet = self.sumando(cr, uid, 'fda.ihce', fda_ids, fila, sheet, meta_row.servicio_tabla_nutrimental, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)

            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos en temas Registro de marca, Código de barras, Patentes, etc. - Región I IHCE', style_n)
            sheet.write(fila, 1, meta_row.cursos_servicios_empresariales_ihce, style_n)
            
            cursos_desa_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','in',('RM','CB','P','FDA')),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('type','=','curso')], context=None)
            
            if cursos_desa_ids:
                sheet = self.sumando(cr, uid, 'date.courses', cursos_desa_ids, fila, sheet, meta_row.cursos_servicios_empresariales_ihce, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
                
            #~ -------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos en temas Registro de marca, Código de barras, Patentes, etc. - Emprered -', style_n)
            sheet.write(fila, 1, meta_row.cursos_servicios_empresariales_emprered, style_n)
            
            cursos_desa_emp_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','emprered'),('services','in',('RM','CB','P','FDA')),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('type','=','curso')], context=None)
            
            if cursos_desa_emp_ids:
                sheet = self.sumando(cr, uid, 'date.courses', cursos_desa_emp_ids, fila, sheet, meta_row.cursos_servicios_empresariales_emprered, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ACELERACIÓN EMPRESARIAL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'ACELERACIÓN EMPRESARIAL', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            #~ ---------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Consultoría Especializada', style_n)
            sheet.write(fila, 1, meta_row.consultoria_especializada, style_n)
            
            courses_ace_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','aceleracion'),('type','=','consultoria'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], context=None)
            
            if courses_ace_ids:
                sheet = self.sumando(cr, uid, 'date.courses', courses_ace_ids, fila, sheet, meta_row.consultoria_especializada, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos, Talleres, diplomados, etc,', style_n)
            sheet.write(fila, 1, meta_row.cursos_aceleracion, style_n)
            
            courses_acele_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','aceleracion'),('type','!=','consultoria'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], context=None)
            
            if courses_acele_ids:
                sheet = self.sumando(cr, uid, 'date.courses', courses_acele_ids, fila, sheet, meta_row.cursos_aceleracion, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ --------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asistentes', style_n)
            sheet.write(fila, 1, meta_row.asistentes_aceleracion, style_n)
            
            if courses_acele_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', courses_acele_ids, fila, sheet, meta_row.asistentes_aceleracion, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ ---------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Empresas Certificadas', style_n)
            sheet.write(fila, 1, meta_row.empresas_certificadas, style_n)
            
            certi_ace_ids = self.pool.get('acceleration.ihce').search(cr, uid, [('option','=','ihce'),('state_ace','in',('process','out_time','done')),('date_ini','>=','01-01-'+str(data.anio)),('date_ini','<=','31-12-'+str(data.anio)), ('date_fin','>=','01-01-'+str(data.anio)),('date_fin','<=','31-12-'+str(data.anio))], context=None)
            
            if certi_ace_ids:
                sheet = self.certificadas(cr, uid, 'acceleration.ihce', certi_ace_ids, fila, sheet, meta_row.empresas_certificadas, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FORMACIÓN DE CAPITAL HUMANO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'FORMACIÓN DE CAPITAL HUMANO', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            #~ ----------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Empresas que recibieron consultoría individual para resolver problemas empresariales específicos ', style_n)
            sheet.write(fila, 1, meta_row.consultoria_servicios_empresariales, style_n)
            
            consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('services','in',('RM','CB','P','FDA')),('dependence','=','ihce'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], context=None)
            
            if consultoria_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', consultoria_ids, fila, sheet, meta_row.consultoria_servicios_empresariales, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            #~ -----------------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Horas', style_n)
            sheet.write(fila, 1, meta_row.horas, style_n)
            
            if consultoria_ids:
                sheet = self.horas(cr, uid, 'date.courses', consultoria_ids, fila, sheet, meta_row.horas, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -----------------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos, Talleres, Diplomados, etc.', style_n)
            sheet.write(fila, 1, meta_row.cursos_fch, style_n)
            
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('services','=','ninguno'),('dependence','=','ihce'),('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], context=None)
            
            if courses_ids:
                sheet = self.sumando(cr, uid, 'date.courses', courses_ids, fila, sheet, meta_row.cursos_fch, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -----------------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Horas', style_n)
            sheet.write(fila, 1, meta_row.horas_cursos, style_n)
            
            if courses_ids:
                sheet = self.horas(cr, uid, 'date.courses', courses_ids, fila, sheet, meta_row.horas_cursos, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -----------------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asistentes', style_n)
            sheet.write(fila, 1, meta_row.asistentes_fch, style_n)
            
            if courses_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', courses_ids, fila, sheet, meta_row.asistentes_fch, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPREREDS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED TIZAYUCA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED TIZAYUCA', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 2, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED TULA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED TULA', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 1, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED HUEJUTLA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED HUEJUTLA', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 8, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED HUICHAPAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED HUICHAPAN', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 5, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED APAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED APAN', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 7, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED PACHUCA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED PACHUCA', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 10, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+EMPRERED TULANCINGO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED TULANCINGO', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 13, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED IXMIQUILPAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED IXMIQUILPAN', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 9, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED ZACUALTIPAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED ZACUALTIPAN', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 11, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED MIXQUIAHUALA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED MIXQUIAHUALA', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 4, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EMPRERED ZIMAPAN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
            fila = fila + 1
            sheet.write(fila, 0, 'EMPRERED ZIMAPÁN', styleG)
            self.titulos(cr, uid, fila, sheet, context)
            
            tup = self.emprered(cr, uid, 6, fila, data, sheet, context)
            sheet = tup[0]
            fila = tup[1]
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TOTAL EMPREREDS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
            #~ fila = fila + 1
            #~ sheet.write(fila, 0, 'TOTAL EMPREREDS', styleG)
            #~ self.titulos(cr, uid, fila, sheet, context)
            
            #~ tup = self.total_emprered(cr, uid, fila, data, sheet, context)
            #~ sheet = tup[0]
            #~ fila = tup[1]
        
        else:
            return False
            raise osv.except_osv(_('Acción Inválida!'), _('No hay registro de metas anuales, no es posible imprimir el reporte.'))
        
        return sheet
        
    
    def emprered(self, cr, uid, empre, fila, data, sheet, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        
        anio = datetime.now().year
        meta2_ids = self.pool.get('meta.anual.emprered').search(cr, uid, [('activo','=',True),('anio_emprered','=',anio),('emprered_meta','=',empre)], limit=1, order='id DESC')
        
        if meta2_ids:
            metas_row = self.pool.get('meta.anual.emprered').browse(cr, uid, meta2_ids[0])
            
            #~ ------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Registro de Marca', style_n)
            sheet.write(fila, 1, metas_row.marca, style_n)
            
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered'),('emprered','=',empre)], order='date ASC')

            if register_ids:
                sheet = self.sumando(cr, uid, 'register.trademark', register_ids, fila, sheet, metas_row.marca, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Patentes', style_n)
            sheet.write(fila, 1, metas_row.patente, style_n)
            
            patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered'),('emprered','=',empre)], order='date ASC')
            
            if patent_ids:
                sheet = self.sumando(cr, uid, 'patent.ihce', patent_ids, fila, sheet, metas_row.patente, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Código de Barras', style_n)
            sheet.write(fila, 1, metas_row.codigo, style_n)
            
            code_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered'),('emprered','=',empre)], order='date ASC')
            
            if code_ids:
                sheet = self.sumando(cr, uid, 'bar.code', code_ids, fila, sheet, metas_row.codigo, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ -------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Cursos', style_n)
            sheet.write(fila, 1, metas_row.cursos, style_n)
            
            courses_emp_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','curso'),('emprered','=',empre)], order='date ASC')
            
            if courses_emp_ids:
                sheet = self.sumando(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, metas_row.cursos, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
                
            #~ ------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Asistentes', style_n)
            sheet.write(fila, 1, metas_row.asistentes, style_n)
            
            if courses_emp_ids:
                sheet = self.asistentes(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, metas_row.asistentes, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            #~ ------------------------------------------------------------------------------
            fila = fila + 1
            sheet.write(fila, 0, 'Horas', style_n)
            sheet.write(fila, 1, metas_row.horas, style_n)
            
            if courses_emp_ids:
                sheet = self.horas(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, metas_row.horas, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Total Asesorías', style_n)
            sheet.write(fila, 1, 0, style_n)
            sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            
            fila = fila + 1
            sheet.write(fila, 0, 'Consultoría Especializada', style_n)
            sheet.write(fila, 1, metas_row.consultoria_especializada, style_n)
            
            consul_empre = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','consultoria'),('emprered','=',empre)], order='date ASC')
            
            if consul_empre:
                sheet = self.sumando(cr, uid, 'date.courses', consul_empre, fila, sheet, metas_row.consultoria_especializada, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Horas de Consultoría', style_n)
            sheet.write(fila, 1, metas_row.horas_consultoria, style_n)
            
            if consul_empre:
                sheet = self.horas(cr, uid, 'date.courses', consul_empre, fila, sheet, metas_row.horas_consultoria, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Empresas dentro de un proyecto de aceleración empresarial', style_n)
            sheet.write(fila, 1, metas_row.empresas_proyecto_aceleracion, style_n)
            
            empresas_ace_emp = self.pool.get('acceleration.ihce').search(cr, uid, [('state_ace','in',('process','out_time','done')),('date_ini','>=','01-01-'+str(data.anio)),('date_ini','<=','31-12-'+str(data.anio)),('date_fin','>=','01-01-'+str(data.anio)),('date_fin','<=','31-12-'+str(data.anio)),('option','=','emprered'),('emprered','=',empre)])
            
            if empresas_ace_emp:
                sheet = self.aceleracion(cr, uid, 'acceleration.ihce', empresas_ace_emp, fila, sheet, metas_row.empresas_proyecto_aceleracion, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Eventos', style_n)
            sheet.write(fila, 1, 0, style_n)
            
            eventos_empre = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','evento'),('emprered','=',empre)], order='date ASC')
            
            if eventos_empre:
                sheet = self.sumando(cr, uid, 'date.courses', eventos_empre, fila, sheet, 0, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
            
            fila = fila + 1
            sheet.write(fila, 0, 'Diagnósticos Empresariales', style_n)
            sheet.write(fila, 1, metas_row.diagnosticos_empresariales, style_n)
            
            company_ids_empre = self.pool.get('companies.ihce').search(cr, uid, [('dependence','=','1'),('emprered','=',empre),('state','=','done'),('company','=',True),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], order='date ASC')
            
            if company_ids_empre:
                sheet = self.sumando(cr, uid, 'companies.ihce', company_ids_empre, fila, sheet, metas_row.diagnosticos_empresariales, context)
            else:
                sheet = self.trimestres(cr, uid, fila, sheet, context)
        else:
            return sheet, fila
            raise osv.except_osv(_('Acción Inválida!'), _('No hay registro de metas anuales para emprered, no es posible imprimir el reporte. Por favor configure las metas anuales.'))
            
        return sheet, fila
        
    def total_emprered(self, cr, uid, fila, data, sheet, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        
        #~ ------------------------------------------------------------------------
        fila = fila + 1
        sheet.write(fila, 0, 'Registro de Marca', style_n)
        
        register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered')], order='date ASC')

        if register_ids:
            sheet = self.sumando(cr, uid, 'register.trademark', register_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Patentes', style_n)
        
        patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered')], order='date ASC')
        
        if patent_ids:
            sheet = self.sumando(cr, uid, 'patent.ihce', patent_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Código de Barras', style_n)
        
        code_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('option','=','emprered')], order='date ASC')
        
        if code_ids:
            sheet = self.sumando(cr, uid, 'bar.code', code_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        #~ -------------------------------------------------------------------------------
        fila = fila + 1
        sheet.write(fila, 0, 'Cursos', style_n)
        courses_emp_ids = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','curso')], order='date ASC')
        
        if courses_emp_ids:
            sheet = self.sumando(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
            
        #~ ------------------------------------------------------------------------------
        fila = fila + 1
        sheet.write(fila, 0, 'Asistentes', style_n)
        
        if courses_emp_ids:
            sheet = self.asistentes(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        #~ ------------------------------------------------------------------------------
        fila = fila + 1
        sheet.write(fila, 0, 'Horas', style_n)
        
        if courses_emp_ids:
            sheet = self.horas(cr, uid, 'date.courses', courses_emp_ids, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Total Asesorías', style_n)
        sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        
        fila = fila + 1
        sheet.write(fila, 0, 'Consultoría Especializada', style_n)
        consul_empre = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','consultoria')], order='date ASC')
        
        if consul_empre:
            sheet = self.sumando(cr, uid, 'date.courses', consul_empre, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Horas de Consultoría', style_n)
        
        if consul_empre:
            sheet = self.horas(cr, uid, 'date.courses', consul_empre, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Empresas dentro de un proyecto de aceleración empresarial', style_n)
        
        empresas_ace_emp = self.pool.get('acceleration.ihce').search(cr, uid, [('state_ace','in',('process','out_time','done')),('date_ini','>=','01-01-'+str(data.anio)),('date_ini','<=','31-12-'+str(data.anio)),('date_fin','>=','01-01-'+str(data.anio)),('date_fin','<=','31-12-'+str(data.anio)),('option','=','emprered')])
        
        if empresas_ace_emp:
            sheet = self.aceleracion(cr, uid, 'acceleration.ihce', empresas_ace_emp, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Eventos', style_n)
        eventos_empre = self.pool.get('date.courses').search(cr, uid, [('state','=','done'),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio)),('dependence','=','emprered'),('type','=','evento')], order='date ASC')
        
        if eventos_empre:
            sheet = self.sumando(cr, uid, 'date.courses', eventos_empre, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        fila = fila + 1
        sheet.write(fila, 0, 'Diagnósticos Empresariales', style_n)
        company_ids_empre = self.pool.get('companies.ihce').search(cr, uid, [('dependence','=','1'),('state','=','done'),('company','=',True),('date','>=','01-01-'+str(data.anio)),('date','<=','31-12-'+str(data.anio))], order='date ASC')
        
        if company_ids_empre:
            sheet = self.sumando(cr, uid, 'companies.ihce', company_ids_empre, fila, sheet, context)
        else:
            sheet = self.trimestres(cr, uid, fila, sheet, context)
        
        return sheet, fila
    
    
    def trimestres(self, cr, uid, fila, sheet, context={}):
        style = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        styleR = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour red;'))
        sheet.write(fila, 5, 0, style)
        sheet.write(fila, 9, 0, style)
        sheet.write(fila, 13, 0, style)
        sheet.write(fila, 17, 0, style)
        sheet.write(fila, 18, 0, style)
        sheet.write(fila, 19, 0, styleR)
        
        return sheet
        
        
    def totales(self, cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context={}):
        style = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        styleV = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        styleA = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleR = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour red;'))
        
        sheet.write(fila, 5, (ene+feb+mar), style)
        sheet.write(fila, 9, (abri+may+jun), style)
        sheet.write(fila, 13, (jul+ago+sep), style)
        sheet.write(fila, 17, (octu+nov+dic), style)
        sheet.write(fila, 18, (ene+feb+mar+abri+may+jun+jul+ago+sep+octu+nov+dic), style)
        porcentaje = ((ene+feb+mar+abri+may+jun+jul+ago+sep+octu+nov+dic)*100) / valor
        if valor < 30:
            sheet.write(fila, 19, valor , styleR)
        else:
            if valor > 30 and valor < 60:
                sheet.write(fila, 19, valor, styleA)
            else:
                sheet.write(fila, 19, valor, styleV)
        
        return sheet
        
    def sumando(self, cr, uid, objeto, values, fila, sheet, valor, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        ene= 0
        feb = 0
        mar = 0
        abri = 0
        may = 0
        jun = 0
        jul = 0
        ago = 0
        sep = 0
        octu = 0
        nov = 0
        dic = 0
        
        for row in self.pool.get(objeto).browse(cr, uid, values, context=context):
            mes = self.month(cr, uid, str(row.date[5:7]), context=context)
            if mes == 1:
                ene += 1
                sheet.write(fila, 2, ene, style_n)
            elif mes == 2:
                feb += 1
                sheet.write(fila, 3, feb, style_n)
            elif mes == 3:
                mar +=  1
                sheet.write(fila, 4, mar, style_n)
            elif mes == 4:
                abri += 1
                sheet.write(fila, 6, abri, style_n)
            elif mes == 5:
                may += 1
                sheet.write(fila, 7, may, style_n)
            elif mes == 6:
                jun += 1
                sheet.write(fila, 8, jun, style_n)
            elif mes == 7:
                jul += 1
                sheet.write(fila, 10, jul, style_n)
            elif mes == 8:
                ago += 1
                sheet.write(fila, 11, ago, style_n)
            elif mes == 9:
                sep += 1
                sheet.write(fila, 12, sep, style_n)
            elif mes == 10:
                octu += 1
                sheet.write(fila, 14, octu, style_n)
            elif mes == 11:
                nov += 1
                sheet.write(fila, 15, nov, style_n)
            else:
                if mes == 12:
                    dic += 1
                    sheet.write(fila, 16, dic, style_n)
        
        sheet = self.totales(cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context)
    
        return sheet
    
    def asistentes(self, cr, uid, objeto, values, fila, sheet, valor, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        ene = 0
        feb = 0
        mar = 0
        abri = 0
        may = 0
        jun = 0
        jul = 0
        ago = 0
        sep = 0
        octu = 0
        nov = 0
        dic = 0
        
        for row in self.pool.get(objeto).browse(cr, uid, values, context=context):
            mes = self.month(cr, uid, str(row.date[5:7]), context=context)
            if mes == 1:
                ene += row.number_attendees
                sheet.write(fila, 2, ene, style_n)
            elif mes == 2:
                feb += row.number_attendees
                sheet.write(fila, 3, feb, style_n)
            elif mes == 3:
                mar += row.number_attendees
                sheet.write(fila, 4, mar, style_n)
            elif mes == 4:
                abri += row.number_attendees
                sheet.write(fila, 6, abri, style_n)
            elif mes == 5:
                may += row.number_attendees
                sheet.write(fila, 7, may, style_n)
            elif mes == 6:
                jun += row.number_attendees
                sheet.write(fila, 8, jun, style_n)
            elif mes == 7:
                jul += row.number_attendees
                sheet.write(fila, 10, jul, style_n)
            elif mes == 8:
                ago += row.number_attendees
                sheet.write(fila, 11, ago, style_n)
            elif mes == 9:
                sep += row.number_attendees
                sheet.write(fila, 12, sep, style_n)
            elif mes == 10:
                octu += row.number_attendees
                sheet.write(fila, 14, octu, style_n)
            elif mes == 11:
                nov += row.number_attendees
                sheet.write(fila, 15, nov, style_n)
            else:
                if mes == 12:
                    dic += row.number_attendees
                    sheet.write(fila, 16, dic, style_n)
        
        sheet = self.totales(cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context)
        
        return sheet
        
    def horas(self, cr, uid, objeto, values, fila, sheet, valor, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        ene = 0
        feb = 0
        mar = 0
        abri = 0
        may = 0
        jun = 0
        jul = 0
        ago = 0
        sep = 0
        octu = 0
        nov = 0
        dic = 0
        
        for row in self.pool.get(objeto).browse(cr, uid, values, context=context):
            mes = self.month(cr, uid, str(row.date[5:7]), context=context)
            if mes == 1:
                ene += row.hours_training
                sheet.write(fila, 2, ene, style_n)
            elif mes == 2:
                feb += row.hours_training
                sheet.write(fila, 3, feb, style_n)
            elif mes == 3:
                mar += row.hours_training
                sheet.write(fila, 4, mar, style_n)
            elif mes == 4:
                abri += row.hours_training
                sheet.write(fila, 6, abri, style_n)
            elif mes == 5:
                may += row.hours_training
                sheet.write(fila, 7, may, style_n)
            elif mes == 6:
                jun += row.hours_training
                sheet.write(fila, 8, jun, style_n)
            elif mes == 7:
                jul += row.hours_training
                sheet.write(fila, 10, jul, style_n)
            elif mes == 8:
                ago += row.hours_training
                sheet.write(fila, 11, ago, style_n)
            elif mes == 9:
                sep += row.hours_training
                sheet.write(fila, 12, sep, style_n)
            elif mes == 10:
                octu += row.hours_training
                sheet.write(fila, 14, octu, style_n)
            elif mes == 11:
                nov += row.hours_training
                sheet.write(fila, 15, nov, style_n)
            else:
                if mes == 12:
                    dic += row.hours_training
                    sheet.write(fila, 16, dic, style_n)
        
        sheet = self.totales(cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context)
        
        return sheet
        
    def certificadas(self, cr, uid, objeto, values, fila, sheet, valor, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        ene = 0
        feb = 0
        mar = 0
        abri = 0
        may = 0
        jun = 0
        jul = 0
        ago = 0
        sep = 0
        octu = 0
        nov = 0
        dic = 0
        
        for row in self.pool.get(objeto).browse(cr, uid, values, context=context):
            for line in row.company_list_ids:
                li = self.pool.get('company.list.acceleration').browse(cr, uid, line.id, context=context)
                if li.certificate:
                    mes = self.month(cr, uid, str(li.date_fin_cer[5:7]), context=context)
                    if mes == 1:
                        ene += 1
                        sheet.write(fila, 2, ene, style_n)
                    elif mes == 2:
                        feb += 1
                        sheet.write(fila, 3, feb, style_n)
                    elif mes == 3:
                        mar += 1
                        sheet.write(fila, 4, mar, style_n)
                    elif mes == 4:
                        abri += 1
                        sheet.write(fila, 6, abri, style_n)
                    elif mes == 5:
                        may += 1
                        sheet.write(fila, 7, may, style_n)
                    elif mes == 6:
                        jun += 1
                        sheet.write(fila, 8, jun, style_n)
                    elif mes == 7:
                        jul += 1
                        sheet.write(fila, 10, jul, style_n)
                    elif mes == 8:
                        ago += 1
                        sheet.write(fila, 11, ago, style_n)
                    elif mes == 9:
                        sep += 1
                        sheet.write(fila, 12, sep, style_n)
                    elif mes == 10:
                        octu += 1
                        sheet.write(fila, 14, octu, style_n)
                    elif mes == 11:
                        nov += 1
                        sheet.write(fila, 15, nov, style_n)
                    else:
                        if mes == 12:
                            dic += 1
                            sheet.write(fila, 16, dic, style_n)
            
            sheet = self.totales(cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context)
        
        return sheet
        
    def aceleracion(self, cr, uid, objeto, values, fila, sheet, valor, context={}):
        style_n = xlwt.easyxf(('font: height 150, color black; alignment: horizontal center'))
        ene = 0
        feb = 0
        mar = 0
        abri = 0
        may = 0
        jun = 0
        jul = 0
        ago = 0
        sep = 0
        octu = 0
        nov = 0
        dic = 0
        
        for row in self.pool.get(objeto).browse(cr, uid, values, context=context):
            for line in row.company_list_ids:
                li = self.pool.get('company.list.acceleration').browse(cr, uid, line.id, context=context)
                mes = self.month(cr, uid, str(li.date_fin_diag[5:7]), context=context)
                if mes == 1:
                    ene += 1
                    sheet.write(fila, 2, ene, style_n)
                elif mes == 2:
                    feb += 1
                    sheet.write(fila, 3, feb, style_n)
                elif mes == 3:
                    mar += 1
                    sheet.write(fila, 4, mar, style_n)
                elif mes == 4:
                    abri += 1
                    sheet.write(fila, 6, abri, style_n)
                elif mes == 5:
                    may += 1
                    sheet.write(fila, 7, may, style_n)
                elif mes == 6:
                    jun += 1
                    sheet.write(fila, 8, jun, style_n)
                elif mes == 7:
                    jul += 1
                    sheet.write(fila, 10, jul, style_n)
                elif mes == 8:
                    ago += 1
                    sheet.write(fila, 11, ago, style_n)
                elif mes == 9:
                    sep += 1
                    sheet.write(fila, 12, sep, style_n)
                elif mes == 10:
                    octu += 1
                    sheet.write(fila, 14, octu, style_n)
                elif mes == 11:
                    nov += 1
                    sheet.write(fila, 15, nov, style_n)
                else:
                    if mes == 12:
                        dic += 1
                        sheet.write(fila, 16, dic, style_n)
            
            sheet = self.totales(cr, uid, fila, sheet, ene, feb, mar, abri, may, jun, jul, ago, sep, octu, nov, dic, valor, context)
        
        return sheet
        
    #~ Función para obtener el nombre del mes
    def month(self, cr, uid, val, context=None):
        mes = 0
        if val == '01':
            mes = 1
        elif val == '02':
            mes = 2
        elif val == '03':
            mes = 3
        elif val == '04':
            mes = 4
        elif val == '05':
            mes = 5
        elif val == '06':
            mes = 6
        elif val == '07':
            mes = 7
        elif val == '08':
            mes = 8
        elif val == '09':
            mes = 9
        elif val == '10':
            mes = 10
        elif val == '11':
            mes = 11
        elif val == '12':
            mes = 12
        
        return mes
    
    def titulos(self, cr, uid, fila, sheet, context={}):
        style = xlwt.easyxf(('font: height 170, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour gray25;'))
        sheet.write(fila, 1, 'META', style)
        sheet.write(fila, 2, 'ENE', style)
        sheet.write(fila, 3, 'FEB', style)
        sheet.write(fila, 4, 'MAR', style)
        sheet.write(fila, 5, 'TRIM1', style)
        sheet.write(fila, 6, 'ABR', style)
        sheet.write(fila, 7, 'MAY', style)
        sheet.write(fila, 8, 'JUN', style)
        sheet.write(fila, 9, 'TRIM2', style)
        sheet.write(fila, 10, 'JUL', style)
        sheet.write(fila, 11, 'AGO', style)
        sheet.write(fila, 12, 'SEPT', style)
        sheet.write(fila, 13, 'TRIM3', style)
        sheet.write(fila, 14, 'OCT', style)
        sheet.write(fila, 15, 'NOV', style)
        sheet.write(fila, 16, 'DIC', style)
        sheet.write(fila, 17, 'TRIM4', style)
        sheet.write(fila, 18, 'TOTAL', style)
        sheet.write(fila, 19, '%', style)
        
        return sheet
