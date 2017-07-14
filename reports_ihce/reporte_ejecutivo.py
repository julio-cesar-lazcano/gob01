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
import pdb

class reporte_ejecutivo(osv.osv_memory):
    _name = "reporte.ejecutivo"
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
    
    #~ Función que crea la hoja de calculo para el reportes
    def action_create_report(self, cr, uid, ids, context=None):
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Reporte Ejecutivo', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Reporte-Ejecutivo.xls"
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
            'description': 'Reporte Ejecutivo',
            'res_model': 'reporte.ejecutivo',
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
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleEm = xlwt.easyxf(('font: height 200, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue;'))
        styleAcom = xlwt.easyxf(('font: height 200, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        styleCap = xlwt.easyxf(('font: height 200, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour red;'))
        styleEmpre = xlwt.easyxf(('font: height 200, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour orange;'))
        styleLab = xlwt.easyxf(('font: height 200, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour dark_purple;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal center'))
        
        #LOGOS
        try:
            sheet.insert_bitmap("/tmp/logo.bmp", 0, 0)
            sheet.insert_bitmap("/tmp/logo1.bmp", 0, 10)
        except:
            print ""
        
        #CABECERA
        sheet.write_merge(0, 0, 0, 10,("ACOMPAÑAMIENTO EMPRESARIAL"), styleT)
        sheet.write_merge(1, 1, 0, 10,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
        
        
        #~~~~~~~~~~~~~~~~~~~~~~ EMPRENDIMIENTO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(4, 4, 1, 9,("EMPRENDIMIENTO"), styleEm)
        
        sheet.write_merge(5, 5, 1, 5,  "Asesorías", style_n)
        asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','emprendimiento')], order='date ASC')
        sheet.write_merge(5, 5, 6, 9, len(asesoria_ids), style_n)
        
        sheet.write_merge(6, 6, 1, 5,  "Pláticas/Cursos/Eventos, etc", style_n)
        courses_empre_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','emprendimiento'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin),('type','!=','consultoria')], context=None)
        sheet.write_merge(6, 6, 6, 9,  len(courses_empre_ids), style_n)
        
        sheet.write_merge(7, 7, 1, 5,  "Asistentes", style_n)
        asis_empre = 0
        for row_asi in self.pool.get('date.courses').browse(cr, uid, courses_empre_ids, context=None):
            asis_empre += row_asi.number_attendees
        sheet.write_merge(7, 7, 6, 9, asis_empre, style_n)
    
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~ ACOMPAÑAMIENTO ~~~~~~~~~~~~~~~~~~~~~~~~~~+
        sheet.write_merge(8, 8, 1, 9,("DESARROLLO EMPRESARIAL"), styleAcom)
        sheet.write_merge(9, 9, 6, 7,("Asesorías"), style_n)
        sheet.write_merge(9, 9, 8, 9,("Servicios"), style_n)
        
        companies = []
        companiesS = []
        hombreA = 0
        hombreS = 0
        mujerA = 0
        mujerS = 0
        
        sheet.write_merge(10, 10, 1, 5,("Registro de Marca"), style_n)
        register_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','marca'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(10, 10, 6, 7, len(register_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', register_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', register_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', register_ids, mujerA, context=context)
        
        register_idss = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(10, 10, 8, 9, len(register_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'register.trademark', register_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'register.trademark', register_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'register.trademark', register_idss, mujerS, context=context)
        
        
        sheet.write_merge(11,11, 1, 5,("Patente"), style_n)
        patent_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','patente')], order='date ASC')
        sheet.write_merge(11,11, 6, 7, len(patent_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', patent_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', patent_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', patent_ids, mujerA, context=context)
        
        patent_idss = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write_merge(11,11, 8, 9, len(patent_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'patent.ihce', patent_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'patent.ihce', patent_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'patent.ihce', patent_idss, mujerS, context=context)
        
        sheet.write_merge(12, 12, 1, 5,("Código de Barras"), style_n)
        bar_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','codigo'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(12, 12, 6, 7, len(bar_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', bar_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', bar_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', bar_ids, mujerA, context=context)
        #~ 
        bar_idss = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(12, 12, 8, 9, len(bar_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'bar.code', bar_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'bar.code', bar_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'bar.code', bar_idss, mujerS, context=context)
        #~ 
        sheet.write_merge(13, 13, 1, 5,("Adecuación de Productos"), style_n)
        adec_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(13, 13, 6, 7, len(adec_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', adec_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', adec_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', adec_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(13, 13, 8, 9, 0, style_n)
        
        sheet.write_merge(14, 14, 1, 5,("Normatividad Nacional"), style_n)
        norm_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','normatividad'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(14, 14, 6, 7, len(norm_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', norm_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', norm_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', norm_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(14, 14, 8, 9, 0, style_n)
        
        sheet.write_merge(15, 15, 1, 5,("Pruebas de laboratorio/Tabla Nutrimental"), style_n)
        fda_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','tabla'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write_merge(15, 15, 6, 7, len(fda_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', fda_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', fda_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', fda_ids, mujerA, context=context)
        
        fda_idss = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write_merge(15, 15, 8, 9, len(fda_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'fda.ihce', fda_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'fda.ihce', fda_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'fda.ihce', fda_idss, mujerS, context=context)
        
        sheet.write_merge(16, 16, 1, 5,("Total"), style_B)
        total_ase = len(register_ids) + len(patent_ids) + len(bar_ids) + len(adec_ids) + len(norm_ids) + len(fda_ids)
        sheet.write_merge(16, 16, 6, 7, total_ase, style_B)
        
        total_ser = len(register_idss) + len(patent_idss) + len(bar_idss) + len(fda_idss)
        sheet.write_merge(16, 16, 8, 9, total_ser, style_B)
        
        sheet.write_merge(17, 17, 6, 6,("H"), style_B)
        sheet.write_merge(17, 17, 7, 7, hombreA, style_B)
        sheet.write_merge(17, 17, 8, 8,("H"), style_B)
        sheet.write_merge(17, 17, 9, 9, hombreS, style_B)
        sheet.write_merge(18, 18, 6, 6,("M"), style_B)
        sheet.write_merge(18, 18, 7, 7, mujerA, style_B)
        sheet.write_merge(18, 18, 8, 8,("M"), style_B)
        sheet.write_merge(18, 18, 9, 9, mujerS, style_B)
        
       
        #~ ~~~~~~~~~~~~~~~~~~~~ CAPITAL HUMANO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(19, 19, 1, 9,("FORMACIÓN DE CAPITAL HUMANO"), styleCap)
        sheet.write_merge(20, 20, 1, 5,("Empresas que recibieron consultoría"), style_n)
        sheet.write_merge(21, 21, 1, 5,("Horas"), style_n)
        sheet.write_merge(22, 22, 1, 5,("Cursos, Talleres, Diplomados, platicas, etc"), style_n)
        sheet.write_merge(23, 23, 1, 5,("Horas"), style_n)
        sheet.write_merge(24, 24, 1, 5,("Asistentes"), style_n)
        sheet.write_merge(25, 25, 1, 5,(""), style_n)
        
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        
        #~ Consultoria, horas y empresas
        consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        for row in self.pool.get('date.courses').browse(cr, uid, consultoria_ids, context=None):
            horas_con += row.hours_training
            invitados_ids = self.pool.get('company.line').search(cr, uid, [('course_id','=', row.id)], context=None)
            for line in self.pool.get('company.line').browse(cr, uid, invitados_ids, context=None):
                ban = False
                for li in company_ids:
                    if li == line.company_id.id:
                        ban = True
                        break 
                if not ban:
                    company_ids.append(line.company_id.id)
        
        sheet.write_merge(20, 20, 6, 9, len(consultoria_ids), style_n)
        #sheet.write_merge(20, 20, 6, 9, len(company_ids), style_n)
        sheet.write_merge(21, 21, 6, 9, horas_con, style_n)
        
        #~ Cursos, talleres, etc
        courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        #courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('services','=','formacion'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        sheet.write_merge(22, 22, 6, 9, len(courses_ids), style_n)
        
        hombres = 0
        mujeres = 0
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            horas += row.hours_training
            asistentes += row.number_attendees
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('company.line').browse(cr, uid, line)
                ro = self.pool.get('companies.ihce').browse(cr, uid, li.contact_id.id, context)
                if ro.sexo == 'M':
                    hombres = hombres + 1
                else:
                    if ro.sexo == 'F':
                        mujeres = mujeres + 1
            
            for line in self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)]):
                li = self.pool.get('list.new.persons').browse(cr, uid, line)
                if li.sexo == 'M':
                    hombres = hombres + 1
                else:
                    if li.sexo == 'F':
                        mujeres = mujeres + 1
        
        sheet.write_merge(23, 23, 6, 9, horas, style_n)
        sheet.write_merge(24, 24, 6, 9, asistentes, style_n)
        
        sheet.write_merge(25, 25, 6, 9, "H: "+str(hombres)+"               M: "+ str(mujeres) , style_B)
        
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~ LABORATORIO DE DISEÑO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~ EMPRERED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(43, 43, 1, 9,("EMPRERED"), styleEmpre)
        sheet.write_merge(44, 44, 6, 7,("Asesorías"), style_n)
        sheet.write_merge(44, 44, 8, 9,("Servicios"), style_n)
        
        companies = []
        companiesS = []
        hombreA = 0
        mujerA = 0
        hombreS = 0
        mujerS = 0

        sheet.write_merge(45, 45, 1, 5,("Asesoría General en Servicios IHCE"), style_n)
        asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','asesoria'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(45, 45, 6, 7, len(asesoria_ids), style_n)

        sheet.write_merge(45, 45, 8, 9, 0, style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', asesoria_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]

        sheet.write_merge(46, 46, 1, 5,("Registro de Marca"), style_n)
        register_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','marca'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(46, 46, 6, 7, len(register_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', register_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        register_idss = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','!=','ihce')], order='date ASC')
        sheet.write_merge(46, 46, 8, 9, len(register_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'register.trademark', register_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'register.trademark', register_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'register.trademark', register_idss, mujerS, context=context)
        
        sheet.write_merge(47, 47, 1, 5,("Patente"), style_n)
        patent_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','patente'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(47, 47, 6, 7, len(patent_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', patent_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', patent_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', patent_ids, mujerA, context=context)
        
        sheet.write_merge(47, 47, 8, 9, 0, style_n)
        
        sheet.write_merge(48, 48, 1, 5,("Código de Barras"), style_n)
        bar_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','codigo'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(48, 48, 6, 7, len(bar_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', bar_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', bar_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', bar_ids, mujerA, context=context)
        
#        bar_idss = self.pool.get('bar.code').search(cr, uid, [('type_membership','!=','False'),('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        bar_idss = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')

        sheet.write_merge(48, 48, 8, 9, len(bar_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'bar.code', bar_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'bar.code', bar_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'bar.code', bar_idss, mujerS, context=context)
        #~ 
        sheet.write_merge(49, 49, 1, 5,("Imágen Corporativa y Etiquetado"), style_n)
        img_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','imagen'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(49, 49, 6, 7, len(img_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', img_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', img_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', img_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(49, 49, 8, 9, 0, style_n)
        
        sheet.write_merge(50, 50, 1, 5,("Financiamiento"), style_n)
        fin_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','financiamiento'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(50, 50, 6, 7, len(fin_ids), style_n)
        
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', fin_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', fin_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', fin_ids, mujerA, context=context)
        
        exp_idss = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','financiamiento'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(50, 50, 8, 9, len(exp_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'servicios.ihce', exp_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'servicios.ihce', exp_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'servicios.ihce', exp_idss, mujerS, context=context)
        
        sheet.write_merge(51, 51, 1, 5,("Emprendimiento"), style_n)
        empre_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','emprendimiento'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(51, 51, 6, 7, len(empre_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', empre_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', empre_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', empre_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(51, 51, 8, 9, 0, style_n)
        
        sheet.write_merge(52, 52, 1, 5,("Registro ente la SHCP"), style_n)
        reg_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','shcp'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(52, 52, 6, 7, len(reg_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', reg_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', reg_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', reg_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(52, 52, 8, 9, 0, style_n)
        
        sheet.write_merge(53, 53, 1, 5,("Formación de Capital Humano"), style_n)
        capital_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','capital'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(53, 53, 6, 7, len(capital_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', capital_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', capital_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', capital_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(53, 53, 8, 9, 0, style_n)
        
        sheet.write_merge(54, 54, 1, 5,("AIE"), style_n)
        aie_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','aie'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(54, 54, 6, 7, len(aie_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', aie_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', aie_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', aie_ids, mujerA, context=context)
        
        sheet.write_merge(54, 54, 8, 9, 0, style_n)
        
        sheet.write_merge(55, 55, 1, 5,("Manos a la obra"), style_n)
        manos_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','manos'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(55, 55, 6, 7, len(manos_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', manos_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', manos_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', manos_ids, mujerA, context=context)
        
        manos_idss = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','manos'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(55, 55, 8, 9, len(manos_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'servicios.ihce', manos_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'servicios.ihce', manos_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'servicios.ihce', manos_idss, mujerS, context=context)
        #~ 
        sheet.write_merge(56, 56, 1, 5,("Adecuación de producto"), style_n)
        ade_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(56, 56, 6, 7, len(ade_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', ade_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', ade_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', ade_ids, mujerA, context=context)
        #~ 
        ade_idss = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(56, 56, 8, 9, len(ade_idss), style_n)
        
        arregloS = self.companies(cr, uid, 'servicios.ihce', ade_idss, companiesS, mujerS, hombreS, context=context)
        
        companiesS = arregloS[0]
        mujerS = arregloS[1]
        hombreS = arregloS[2]
        
        #~ hombreS = self.conteoH(cr, uid, 'servicios.ihce', ade_idss, hombreS, context=context)
        #~ mujerS = self.conteoM(cr, uid, 'servicios.ihce', ade_idss, mujerS, context=context)
        #~ 
        
        sheet.write_merge(57, 57, 1, 5,("Aceleración Empresarial"), style_n)
        ace_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','aceleracion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered')], order='date ASC')
        sheet.write_merge(57, 57, 6, 7, len(ace_ids), style_n)
        
        arreglo = self.companies(cr, uid, 'asesorias.ihce', ace_ids, companies, mujerA, hombreA, context=context)
        
        companies = arreglo[0]
        mujerA = arreglo[1]
        hombreA = arreglo[2]
        
        #~ hombreA = self.conteoH(cr, uid, 'asesorias.ihce', ace_ids, hombreA, context=context)
        #~ mujerA = self.conteoM(cr, uid, 'asesorias.ihce', ace_ids, mujerA, context=context)
        #~ 
        sheet.write_merge(57, 57, 8, 9, 0, style_n)
        
        
        sheet.write_merge(58, 58, 1, 5,("Total"), style_B)

        total_aseso = len(asesoria_ids) + len(register_ids) + len(patent_ids) + len(bar_ids) + len(img_ids) + len(fin_ids) + len(empre_ids) + len(reg_ids) + len(capital_ids) + len(aie_ids) + len(manos_ids)+ len(ace_ids) + len(ade_ids)

        sheet.write_merge(58, 58, 6, 7, total_aseso, style_B)
        
        total_servi = len(register_idss) + len(bar_idss) + len(exp_idss) + len(manos_idss) + len(ade_idss)
        sheet.write_merge(58, 58, 8, 9, total_servi, style_B)
        
        sheet.write_merge(59, 59, 6, 6,("H"), style_B)
        sheet.write_merge(59, 59, 7, 7, hombreA, style_B)
        sheet.write_merge(59, 59, 8, 8,("H"), style_B)
        sheet.write_merge(59, 59, 9, 9, hombreS, style_B)
        sheet.write_merge(60, 60, 6, 6,("M"), style_B)
        sheet.write_merge(60, 60, 7, 7, mujerA, style_B)
        sheet.write_merge(60, 60, 8, 8,("M"), style_B)
        sheet.write_merge(60, 60, 9, 9, mujerS, style_B)
        
        sheet.write_merge(61, 61, 1, 5,("Empresas que recibieron consultoría"), style_n)
        sheet.write_merge(62, 62, 1, 5,("Horas"), style_n)
        sheet.write_merge(63, 63, 1, 5,("Cursos, Talleres, Diplomados, Platicas, etc."), style_n)
        sheet.write_merge(64, 64, 1, 5,("Horas"), style_n)
        sheet.write_merge(65, 65, 1, 5,("Asistentes"), style_n)
        
        horas = 0
        horas_con = 0
        empresas = 0
        asistentes = 0
        company_ids = []
        ban = False
        
        #~ Consultoria, horas y empresas
        consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('dependence','=','emprered'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        for row in self.pool.get('date.courses').browse(cr, uid, consultoria_ids, context=None):
            empresas += row.number_attendees
            horas_con += row.hours_training
        
        sheet.write_merge(61, 61, 6, 9, empresas, style_n)
        sheet.write_merge(62, 62, 6, 9, horas_con, style_n)
        
        #~ Cursos, talleres, etc
        #courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('dependence','=','emprered'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        sheet.write_merge(63, 63, 6, 9, len(courses_ids), style_n)

        #pdb.set_trace()
        
        hombre = 0
        mujer = 0


        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            horas += row.hours_training
            asistentes += row.number_attendees
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)], context=None):
                li = self.pool.get('company.line').browse(cr, uid, line)


                if li.company_id.id != False:
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',li.company_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)
                    if(company.sexo == 'M'):
                        hombre = hombre + 1
                    if(company.sexo == 'F'):
                        mujer = mujer + 1
                else:
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',li.contact_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)

                    if(company.sexo == 'M'):
                        hombre = hombre + 1
                        
                    if(company.sexo == 'F'):
                        mujer = mujer + 1

           
            courses_id = self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)], context=None)
            for listnewpersons in self.pool.get('list.new.persons').browse(cr, uid, courses_id, context=None):
                
                if(listnewpersons.id != False):
                    if(listnewpersons.sexo == 'M'):
                        hombre = hombre + 1
                    if(listnewpersons.sexo == 'F'):
                        mujer = mujer + 1

        sheet.write_merge(64, 64, 6, 9, horas, style_n)
        sheet.write_merge(65, 65, 6, 9, asistentes, style_n)
        sheet.write_merge(66, 66, 6, 9, "H: "+str(hombre)+"               M: " + str(mujer) , style_B)






        courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        #courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('dependence','=','emprered'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        sheet.write_merge(63, 63, 6, 9, len(courses_ids), style_n)

        #pdb.set_trace()
        
        hombre = 0
        mujer = 0


        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            horas += row.hours_training
            asistentes += row.number_attendees
            
            for line in self.pool.get('company.line').search(cr, uid, [('course_id','=',row.id)], context=None):
                li = self.pool.get('company.line').browse(cr, uid, line)


                if li.company_id.id != False:
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',li.company_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)
                    if(company.sexo == 'M'):
                        hombre = hombre + 1
                    if(company.sexo == 'F'):
                        mujer = mujer + 1
                else:
                    com = self.pool.get('companies.ihce').search(cr, uid, [('id','=',li.contact_id.id)], context=None)
                    company = self.pool.get('companies.ihce').browse(cr, uid, com, context=None)

                    if(company.sexo == 'M'):
                        hombre = hombre + 1
                        
                    if(company.sexo == 'F'):
                        mujer = mujer + 1

           
            courses_id = self.pool.get('list.new.persons').search(cr, uid, [('course_id','=',row.id)], context=None)
            for listnewpersons in self.pool.get('list.new.persons').browse(cr, uid, courses_id, context=None):
                
                if(listnewpersons.id != False):
                    if(listnewpersons.sexo == 'M'):
                        hombre = hombre + 1
                    if(listnewpersons.sexo == 'F'):
                        mujer = mujer + 1

        #sheet.write_merge(70, 70, 6, 9, horas, style_n)
        sheet.write_merge(71, 71, 6, 9, 'Valores Numeralia', style_B)
        sheet.write_merge(72, 72, 6, 9, "H: "+str(hombre)+"               M: " + str(mujer) , style_B)
    
        #pdb.set_trace()
        return sheet
        
    def companies(self, cr, uid, obj, ids, companies, mujeres, hombres, context=None):
        
        for line in self.pool.get(obj).browse(cr, uid, ids):
            company = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
            
            ban = False
            
            for li in companies:
                if li == company.id:
                    ban = True
                    break 
            if not ban:
                companies.append(company.id)
 
                if company.sexo == 'F':
                    mujeres = mujeres + 1
                else:
                    if company.sexo == 'M':
                        hombres = hombres + 1
            
       
        return companies, mujeres, hombres
        
    def conteoH(self, cr, uid, obj, ids, hombre, context=None):

        for line in self.pool.get(obj).browse(cr, uid, ids):
            row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
            if row.sexo == 'M':
                hombre = hombre + 1
                    
        return hombre
        
    def conteoM(self, cr, uid, obj, ids, mujer, context=None):
        
        for line in self.pool.get(obj).browse(cr, uid, ids):
            row = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id)
            if row.sexo == 'F':
                mujer = mujer + 1
                    
        return mujer
        
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
