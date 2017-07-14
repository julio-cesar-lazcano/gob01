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

class emprered_ejecutivo(osv.osv_memory):
    _name = "emprered.ejecutivo"
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
        sheet_principal = workbook.add_sheet('Emprered Ejecutivo', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, ids, sheet_principal, context)
        # Creamos el nombre del archivo
        name = "Emprered Ejecutivo.xls"
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
            'description': 'Reporte Emprered Ejecutivo',
            'res_model': 'emprered.ejecutivo',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        return True
    
    #~ Función que llena la hoja con los datos correspondientes del reporte
    def create_principal_sheet(self, cr, uid, ids, sheet, context={}):

        data = self.browse(cr, uid, ids[0], context=context)
        
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center; '))
        style = xlwt.easyxf(('font: height 180, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))
        #CABECERA
        sheet.write_merge(0, 0, 0, 13,("Servicios y atenciones Emprered"), styleT)
        
        sheet.write_merge(1, 1, 0, 13,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
        #TITULOS
        sheet.write(4, 0, '', style)
        sheet.write(5, 0, 'Asesorías', style_n)
        sheet.write(6, 0, 'Cursos', style_n)
        sheet.write(7, 0, 'Asistentes', style_n)
        sheet.write(8, 0, 'Horas', style_n)
        sheet.write(9, 0, 'Consultorías', style_n)
        sheet.write(10, 0, 'Horas consultorías', style_n)
        sheet.write(11, 0, 'Servicios', style_n)
        
        sheet.write(4, 1, 'Apan', style)
        sheet.write(4, 2, 'Atotonilco', style)
        sheet.write(4, 3, 'Huejutla', style)
        sheet.write(4, 4, 'Huichapan', style)
        sheet.write(4, 5, 'Ixmiquilpan', style)
        sheet.write(4, 6, 'Otomí-Tepehua', style)
        sheet.write(4, 7, 'Mixquiahuala', style)
        sheet.write(4, 8, 'Molango', style)
        sheet.write(4, 9, 'Pachuca', style)
        sheet.write(4, 10, 'Tizayuca', style)
        sheet.write(4, 11, 'Tula', style)
        sheet.write(4, 12, 'Tulancingo', style)
        sheet.write(4, 13, 'Zacualtipan', style)
        sheet.write(4, 14, 'Metztitlán', style)
        sheet.write(4, 15, 'Jacala', style)
        sheet.write(4, 16, 'Zimapan', style)#Cambio realizado por Julio Cesar Lazcano 
        sheet.write(4, 17, 'Total', style)
        

        
        asesoria = 0
        curso = 0
        asistente = 0
        hora = 0
        consultoria = 0
        horaCo = 0
        servicio = 0
        
        emprereds = self.pool.get('emprereds').search(cr, uid, [])
        
        for row in emprereds:
            asesoria_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
            
            ase = 0
            
            for line in self.pool.get('asesorias.ihce').browse(cr, uid, asesoria_ids):
                if line[0].name == 'asesoria' or line[0].name == 'marca' or line[0].name == 'patente' or line[0].name == 'codigo' or line[0].name == 'imagen' or line[0].name == 'financiamiento' or line[0].name == 'emprendimiento' or line[0].name == 'shcp' or line[0].name == 'capital' or line[0].name == 'aie' or line[0].name == 'manos' or line[0].name == 'adecuacion' or line[0].name == 'aceleracion':
                    ase = ase + 1
            
            sheet = self.carga(cr, uid, 5, ase, row, sheet, context)
            
            asesoria += ase
            
            courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('dependence','=','emprered'),('emprered','=', row),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)

            sheet = self.carga(cr, uid, 6, len(courses_ids), row, sheet, context)
            
            curso += len(courses_ids)
            #pdb.set_trace()

            asis = 0
            hor = 0
            
            for cur in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=context):
                asis += cur.number_attendees
                hor += cur.hours_training

            asistente += asis
            hora += hor
            
            sheet = self.carga(cr, uid, 7, asis, row, sheet, context)
            sheet = self.carga(cr, uid, 8, hor, row, sheet, context)
            
            consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('dependence','=','emprered'),('emprered','=', row),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)

            consul = 0
            horaC = 0
            
            for cur in self.pool.get('date.courses').browse(cr, uid, consultoria_ids, context=context):
                consul += cur.number_attendees
                horaC += cur.hours_training
                
            sheet = self.carga(cr, uid, 9, consul, row, sheet, context)
            sheet = self.carga(cr, uid, 10, horaC, row, sheet, context)
            
            consultoria += consul
            horaCo += horaC
            
            
            register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
        
            bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
            
            exp_ids = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','financiamiento'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
            
            manos_ids = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','manos'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
            
            ade_ids = self.pool.get('servicios.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','emprered'),('emprered','=', row)])
            
            servicios = len(register_ids) + len(bar_ids) + len(exp_ids) + len(manos_ids) + len(ade_ids)

            sheet = self.carga(cr, uid, 11, servicios, row, sheet, context)
            
            servicio += servicios
            
        sheet.write(5, 17, asesoria, style_n)
        sheet.write(6, 17, curso, style_n)
        sheet.write(7, 17, asistente, style_n)
        sheet.write(8, 17, hora, style_n)
        sheet.write(9, 17, consultoria, style_n)
        sheet.write(10, 17, horaCo, style_n)
        sheet.write(11, 17, servicio, style_n)
        
        return sheet
    
    def carga(self, cr, uid, i, valor, row, sheet, context={}):
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal center'))

        if row == 7:
            sheet.write(i, 1, valor, style_n)
        elif row == 16:
            sheet.write(i, 2, valor, style_n)
        elif row == 8:
            sheet.write(i, 3, valor, style_n)
        elif row == 5:
            sheet.write(i, 4, valor, style_n)
        elif row == 9:
            sheet.write(i, 5, valor, style_n)
        elif row == 17:
            sheet.write(i, 6, valor, style_n)
        elif row == 4:
            sheet.write(i, 7, valor, style_n)
        elif row == 18:
            sheet.write(i, 8, valor, style_n)
        elif row == 10:
            sheet.write(i, 9, valor, style_n)
        elif row == 2:
            sheet.write(i, 10, valor, style_n)
        elif row == 1:
            sheet.write(i, 11, valor, style_n)
        elif row == 13:
            sheet.write(i, 12, valor, style_n)
        elif row == 11:
            sheet.write(i, 13, valor, style_n)
        elif row == 19:
            sheet.write(i, 14, valor, style_n)
        elif row == 20:
            sheet.write(i, 15, valor, style_n)
        elif row == 21:
            sheet.write(i, 16, valor, style_n)

        
        
        return sheet
      
