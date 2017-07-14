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
from StringIO import StringIO
import psycopg2
import psycopg2.extras
from openerp.tools.translate import _
import time
from datetime import date
import locale
from PIL import Image
import os
import xmlrpclib
import io, StringIO
from PIL import Image


class reports_laboratory(osv.osv_memory):
    _name = "reports.laboratory"
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
        sheet_principal = workbook.add_sheet('Informe Laboratorio de Diseño', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, sheet_principal, data, context)
        # Creamos el nombre del archivo
        name = "Informe Laboratorio de Diseño.xls"
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
            'description': 'Informe Mensual Laboratorio',
            'res_model': 'reports.laboratory',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        
        return True
    
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False

        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Reporte correspondiente del " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ LABORATORIO
        sheet.write_merge(6, 6, 2, 9,("Laboratorio de Diseño y desarrollo de producto"), styleGA)
        sheet.write_merge(7, 7, 2, 9,  "Asesorías empresariales", styleG)
        
        advices_ids = self.pool.get('advices.laboratory').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        app = 0
        nami = 0
        cor = 0
        logo = 0
        eti = 0
        enva = 0
        foto = 0
        emba = 0
        empa = 0
        ven = 0
        tresd = 0
        pro = 0
        cata = 0

        hombres = 0
        mujeres = 0
        
        for line in self.pool.get('advices.laboratory').browse(cr, uid, advices_ids, context=None):
            ro = self.pool.get('companies.ihce').browse(cr, uid, line.company_id.id, context)   

            if ro.sexo == 'M':
                    hombres = hombres + 1
            
            if ro.sexo == 'F':
                    mujeres = mujeres + 1

            if line.option == '1':
                app += 1
            elif line.service.id == 17:
                nami += 1
            elif line.service.id == 1:
                cor += 1
            elif line.service.id == 2:
                logo += 1
            elif line.service.id == 12:
                logo += 1
            elif line.service.id == 5:
                eti += 1
            elif line.service.id == 15:
                eti += 1
            elif line.service.id == 11:
                enva += 1
            elif line.service.id == 9:
                foto += 1
            elif line.service.id == 6:
                emba += 1
            elif line.service.id == 16:
                empa += 1
            elif line.service.id == 4:
                ven += 1
            elif line.service.id == 7:
                tresd +=1
            elif line.service.id == 10:
                cata +=1
            else:
                if line.service.id == 3:
                    pro += 1
                    
        sheet.write_merge(8, 8, 2, 8,  "Naming", style_n)
        sheet.write(8, 9, nami, style_n)
        sheet.write_merge(9, 9, 2, 8,  "Imágen Corporativa", style_n)
        sheet.write(9, 9, cor, style_n)
        sheet.write_merge(10, 10, 2, 8,  "Diseño y rediseño de logotipo", style_n)
        sheet.write(10, 9, logo, style_n)
        sheet.write_merge(11, 11, 2, 8,  "Diseño y rediseño de etiqueta", style_n)
        sheet.write(11, 9, eti, style_n)
        sheet.write_merge(12, 12, 2, 8,  "Diseño de envase", style_n)
        sheet.write(12, 9, enva, style_n)
        sheet.write_merge(13, 13, 2, 8,  "Fotografía del producto", style_n)
        sheet.write(13, 9, foto, style_n)
        sheet.write_merge(14, 14, 2, 8,  "Embalaje", style_n)
        sheet.write(14, 9, emba, style_n)
        sheet.write_merge(15, 15, 2, 8,  "Empaque", style_n)
        sheet.write(15, 9, empa, style_n)
        sheet.write_merge(16, 16, 2, 8,  "Punto de venta", style_n)
        sheet.write(16, 9, ven, style_n)
        sheet.write_merge(17, 17, 2, 8,  "Diseño 3D", style_n)
        sheet.write(17, 9, tresd, style_n)
        sheet.write_merge(18, 18, 2, 8,  "Prototipado rápido", style_n)
        sheet.write(18, 9, pro, style_n)
        sheet.write_merge(19, 19, 2, 8,  "Diseño de Folletos y Catálogos", style_n)
        sheet.write(19, 9, cata, style_n)
        sheet.write_merge(20, 20, 2, 8,  "Aplicaciones", style_n)
        sheet.write(20, 9, app, style_n)
        sheet.write_merge(21, 21, 2, 8,  "Total", style_B)
        sheet.write(21, 9, len(advices_ids), style_B)
        

        sheet.write_merge(23, 23, 6, 9, "H: "+str(hombres)+"               M: "+ str(mujeres) , style_B)


        sheet.write_merge(25, 25, 2, 9,("Laboratorio de Diseño y desarrollo de producto"), styleGA)
        sheet.write_merge(26, 26, 2, 9,  "Servicios empresariales", styleG)
        
        services_ids = self.pool.get('desing.laboratory').search(cr, uid, [('date_fin','>=',data.date_ini),('date_fin','<=',data.date_fin)], context=None)
        app = 0
        cor = 0
        logo = 0
        eti = 0
        enva = 0
        foto = 0
        emba = 0
        empa = 0
        ven = 0
        tresd = 0
        pro = 0
        cata = 0
        total = 0

        hombres2 = 0
        mujeres2 = 0

        my_list = []

        for row in self.pool.get('desing.laboratory').browse(cr, uid, services_ids, context=None):

            if row.state == 'done' or row.state == 'pre_done':

                if row .company_id.id not in my_list:
                        my_list.append(row .company_id.id)

                        ro2 = self.pool.get('companies.ihce').browse(cr, uid, row .company_id.id, context)   

                        if ro2.sexo == 'M':
                                hombres2 = hombres2 + 1
                        
                        if ro2.sexo == 'F':
                                mujeres2 = mujeres2 + 1

                if row.app:
                    app += 1
                elif row.service.id == 1:
                    cor += 1
                elif row.service.id == 2:
                    logo += 1
                elif row.service.id == 12:
                    logo += 1
                elif row.service.id == 5:
                    eti += 1
                elif row.service.id == 15:
                    eti += 1
                elif row.service.id == 11:
                    enva += 1
                elif row.service.id == 9:
                    foto += 1
                elif row.service.id == 6:
                    emba += 1
                elif row.service.id == 16:
                    empa += 1
                elif row.service.id == 4:
                    ven += 1
                elif row.service.id == 7:
                    tresd += 1
                elif row.service.id == 10:
                    cata += 1
                else:
                    if row.service.id == 3:
                        pro += 1
                total = total + 1
                

        sheet.write_merge(27, 27, 2, 8,  "Imagen Corporativa", style_n)
        sheet.write(27, 9, cor, style_n)
        sheet.write_merge(28, 28, 2, 8,  "Diseño y rediseño de logotipo", style_n)
        sheet.write(28, 9, logo, style_n)
        sheet.write_merge(29, 29, 2, 8,  "Diseño y rediseño de etiqueta", style_n)
        sheet.write(29, 9, eti, style_n)
        sheet.write_merge(30, 30, 2, 8,  "Diseño de Envase", style_n)
        sheet.write(30, 9, enva, style_n)
        sheet.write_merge(31, 31, 2, 8,  "Fotografía de producto", style_n)
        sheet.write(31, 9, foto, style_n)
        sheet.write_merge(32, 32, 2, 8,  "Embalaje", style_n)
        sheet.write(32, 9, emba, style_n)
        sheet.write_merge(33, 33, 2, 8,  "Empaque", style_n)
        sheet.write(33, 9, empa, style_n)
        sheet.write_merge(34, 34, 2, 8,  "Punto de Venta", style_n)
        sheet.write(34, 9, ven, style_n)
        sheet.write_merge(35, 35, 2, 8,  "Diseño 3D", style_n)
        sheet.write(35, 9, tresd, style_n)
        sheet.write_merge(36, 36, 2, 8,  "Prototipado rápido", style_n)
        sheet.write(36, 9, pro, style_n)
        sheet.write_merge(37, 37, 2, 8,  "Diseño de Folletos y Catálogosjkjk", style_n)
        sheet.write(37, 9, cata, style_n)
        sheet.write_merge(38, 38, 2, 8,  "Aplicaciones opo", style_n)
        sheet.write(38, 9, app, style_n)
        sheet.write_merge(39, 39, 2, 8,  "Total", style_B)
        sheet.write(39, 9, total, style_B)

        sheet.write_merge(40, 40, 6, 9, "H: "+str(hombres2)+"               M: "+ str(mujeres2) , style_B)
        
        
        #~ A prtir de aqui se agregan las notas del crm que son marcadas como importantes y las fotografias que se hayan adjuntado al proyecto de crm
        actividades = self.pool.get('crm.project.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('priority','=','1'),('area','=',10),('state','=','d-done')], context=None)
        
        if actividades:
            sheet.write_merge(42, 42, 1, 10, "ACTIVIDADES RELEVANTES", styleTT)
            
            con = 1
            col = 43
            style_na = xlwt.easyxf(('font: height 175, color black; alignment: horizontal left'))

            for row in self.pool.get('crm.project.ihce').browse(cr, uid, actividades, context=None):
                if not row.notes:
                    sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + row.name.encode('utf-8') + "    " + str(row.date), style_na)
                else:
                    sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + row.name.encode('utf-8') + "    " + str(row.date) + "   " + row.notes.encode('utf-8'), style_na)
                
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
