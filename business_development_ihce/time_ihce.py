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
#    Coded by: Karen Morales(karen.morales@grupoaltegra.com)
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
############################################################################  

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import time

class time_development(osv.Model):
    _name = 'time.development'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Nombre"),
        'description': fields.char("Descripción"),
        'date': fields.date("Fecha"),
        'phonetic_search': fields.integer("Búsqueda Fonética"),
        'phonetic_search_percent': fields.integer("Porcentaje de avance"),
        'send_format': fields.integer("Envío de formato de IHCE a cliente"),
        'send_format_percent': fields.integer("Porcentaje de avance"),
        'vobo_format': fields.integer("VoBo de formato"),
        'vobo_format_percent': fields.integer("Porcentaje de avance"),
        'receiving_record_percent': fields.integer("Porcentaje de avance"),
        'impi': fields.integer("Ingreso al IMPI"),
        'impi_percent': fields.integer("Porcentaje de avance"),
        'requirements_sheet': fields.integer("Entrega de Hoja de Requisitos"),
        'requirements_sheet_percent': fields.integer("Porcentaje de avance"),
        'information_gs1': fields.integer("Llenado de información a GS1"),
        'information_gs1_percent': fields.integer("Porcentaje de avance"),
        'reception_information': fields.integer("Recepción de Información"),
        'reception_information_percent': fields.integer("Porcentaje de avance"),
        'send_information_gs1': fields.integer("Envío de Información a GS1"),
        'send_information_gs1_percent': fields.integer("Porcentaje de avance"),
        'reception_letters': fields.integer("Recepción de Cartas de asociado"),
        'reception_letters_percent': fields.integer("Porcentaje de avance"),
        'advice_company': fields.integer("Citar a empresa para asesoría"),
        'advice_company_percent': fields.integer("Porcentaje de avance"),
        'letter_company': fields.integer("Carta de parte de Empresa"),
        'letter_company_percent': fields.integer("Porcentaje de avance"),
        'send_impi': fields.integer("Enviar al IMPI"),
        'send_impi_percent': fields.integer("Porcentaje de avance"),
        'mail_company': fields.integer("Reenviar correo a empresa"),
        'mail_company_percent': fields.integer("Porcentaje de avance"),
        'request_patent': fields.integer("Solicitud de patente"),
        'request_patent_percent': fields.integer("Porcentaje de avance"),
        'ingress_impi': fields.integer("Ingreso al IMPI"),
        'ingress_impi_percent': fields.integer("Porcentaje de avance"),
        'contact_laboratory': fields.integer("Contacto laboratorio"),
        'contact_laboratory_percent': fields.integer("Porcentaje de avance"),
        'send_sale': fields.integer("Enviar a Empresa cotización"),
        'send_sale_percent': fields.integer("Porcentaje de avance"),
        'contact_company_laboratory': fields.integer("Contacto Empresa Laboratorio"),
        'contact_company_laboratory_percent': fields.integer("Porcentaje de avance"),
        'voucher_laboratory': fields.integer("Pago de empresa a laboratorio"),
        'voucher_laboratory_percent': fields.integer("Porcentaje de avance"),
        'reception_samples': fields.integer("Recepción de muestras"),
        'reception_samples_percent': fields.integer("Porcentaje de avance"),
        'send_samples': fields.integer("Enviar muestras al laboratorio IHCE"),
        'send_samples_percent': fields.integer("Porcentaje de avance"),
        'emits_table': fields.integer("Emite tabla nutrimental"),
        'emits_table_percent': fields.integer("Porcentaje de avance"),
    }

    _defaults = {
        'name': "Ingrese el número de días que se tiene para cumplir cada tarea. Y el porcentaje de avance de cada una.",
        'description': "Tiempos y porcentajes asignados a cada etapa de los servicios de Desarrollo Empresarial",
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    def create(self, cr, uid, vals, context=None):
        return super(time_development, self).create(cr, uid, vals, context)
        
    def write(self, cr, uid, ids, vals, context=None):
        return super(time_development,self).write(cr, uid, ids, vals, context=context)

    def check_percent(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        percent_mark = row.phonetic_search_percent + row.send_format_percent + row.vobo_format_percent + row.receiving_record_percent + row.impi_percent
        
        percent_code = row.requirements_sheet_percent + row.information_gs1_percent + row.reception_information_percent + row.send_information_gs1_percent + row.reception_letters_percent + row.advice_company_percent
        
        percent_patent = row.letter_company_percent + row.send_impi_percent + row.mail_company_percent + row.request_patent_percent + row.ingress_impi_percent
        
        percent_fda = row.contact_laboratory_percent + row.send_sale_percent + row.contact_company_laboratory_percent + row.voucher_laboratory_percent + row.reception_samples_percent + row.send_samples_percent + row.emits_table_percent
        
        if percent_mark == 100 and percent_code == 100 and percent_patent == 100 and percent_fda == 100:
            raise osv.except_osv(_('Correcto'), _('Los porcentajes son correctos.!!'))
        elif percent_mark != 100: 
            raise osv.except_osv(_('Verifique'), _('La suma de los percentajes de registro de marca no es el 100%'))
        elif percent_code != 100: 
            raise osv.except_osv(_('Verifique'), _('La suma de los percentajes de código de barras no es el 100%'))
        elif percent_patent != 100: 
            raise osv.except_osv(_('Verifique'), _('La suma de los percentajes de patente no es el 100%'))
        else:
            if percent_fda != 100: 
                raise osv.except_osv(_('Verifique'), _('La suma de los percentajes de FDA no es el 100%'))
        
        return True
