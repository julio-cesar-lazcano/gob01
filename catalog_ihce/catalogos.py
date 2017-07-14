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
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from datetime import datetime, date, timedelta
import time
from openerp import workflow

#~ DATOS DE ATENCIÓN
class atention_area(osv.Model):
    _name = 'atention.area'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Area de atención", size=200, required=True),
    }

class convocatoria(osv.Model):
    _name = 'convocatoria'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Convocatoria", size=200, required=True),
    }


class responsible_area(osv.Model):
    _name = 'responsible.area'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Departamento", size=200, required=True),
    }


class emprereds(osv.Model):
    _name = 'emprereds'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Emprered", size=200, required=True),
        'town_id': fields.many2one('town.hidalgo', "Municipio"),
    }

#~ DATOS GENERALES
class states_mexico(osv.Model):
    _name = 'states.mexico'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Estado", size=100),
        'country_id': fields.char("País", size=64)
    }
    
    _defaults = {
        'country_id':'México',
    }
    
class town_hidalgo(osv.Model):
    _name = 'town.hidalgo'
    
    _columns = {
        'name': fields.char("Municipio", size=100),
        'state_id': fields.many2one('states.mexico', "Estado"),
        'region_id': fields.many2one('region.hidalgo', "Región"),
    }
    
class colony_hidalgo(osv.Model):
    _name = 'colony.hidalgo'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'town_id': fields.many2one('town.hidalgo', "Municipio"),
        'name': fields.char("Colonia/Localidad", size=100),
    }
    
class region_hidalgo(osv.Model):
    _name = 'region.hidalgo'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Región", size=100),
    }
    
class escolaridad(osv.Model):
    _name = 'escolaridad'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Escolaridad", size=200, required=True),
    }

class caracteristica_poblacional(osv.Model):
    _name = 'caracteristica.poblacional'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Característica Poblacional", size=200, required=True),
        'priority': fields.integer("Prioridad", required=True),
    }
    
    def create(self, cr, uid, vals, context=None):
        #~ ban = False
        #~ if vals.get('priority') => 0:
            #~ vals.update({'priority': vals.get('priority')})
        #~ else:
            #~ raise osv.except_osv(_('Verifique'), _('Asigne una prioridad mayor a 0'))
        
        return super(caracteristica_poblacional, self).create(cr, uid, vals, context)
        
    def write(self, cr, uid, ids, vals, context=None):
        #~ ban = False
        #~ if vals.get('priority') > 0:
            #~ vals.update({'priority': vals.get('priority')})
        #~ else:
            #~ raise osv.except_osv(_('Verifique'), _('Asigne una prioridad mayor a 0'))
        
        return super(caracteristica_poblacional,self).write(cr, uid, ids, vals, context=context)


    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)
        unlink_ids = []

        for row in data:
            rows_ids = self.pool.get('companies.ihce').search(cr, uid, [('population_characteristics','=',row['id'])])
            if not rows_ids:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar una característica poblacional que está siendo utilizada!'))

        return super(caracteristica_poblacional, self).unlink(cr, uid, unlink_ids, context=context)

#~ ACTIVIDAD ECONOMICA
class tamano_actividad_economica(osv.Model):
    _name = 'tamano.actividad.economica'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Tamaño", size=100,required=True),
    }
    
class sector_actividad_economica(osv.Model):
    _name = 'sector.actividad.economica'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Sector", size=100,required=True),
    }

    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)
        unlink_ids = []

        for row in data:
            rows_ids = self.pool.get('companies.ihce').search(cr, uid, [('sector','=',row['id'])])
            if not rows_ids:
                unlink_ids.append(row['id'])
            else:
                raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar un sector que está siendo utilizado!'))

        return super(sector_actividad_economica, self).unlink(cr, uid, unlink_ids, context=context)
    
class ventas_anuales_actividad_economica(osv.Model):
    _name = 'ventas.anuales.actividad.economica'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Ventas anuales", size=100, required=True),
    }
    
class emprendedor_actividad_economica(osv.Model):
    _name = 'emprendedor.actividad.economica'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Emprendedor con", size=100, required=True),
    }

class tipo_emprendedor_actividad_economica(osv.Model):
    _name = 'tipo.emprendedor.actividad.economica'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Tipo de actividad", size=100, required=True),
    }



#~ AREAS DE DESARROLLO
class development_areas(osv.Model):
    _name = 'development.areas'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'administration': fields.boolean("Administración"),
        'finance': fields.boolean("Finanzas"),
        'legal': fields.boolean("Legal"),
        'sales': fields.boolean("Ventas"),
        'advice': fields.boolean("Asesoría físcal"),
        'development': fields.boolean("Desarrollo humano"),
        'production': fields.boolean("Producción"),
        'marketing': fields.boolean("Mercadotecnia"),
        'business_plan': fields.boolean("Plan de negocios"),
        'entrepreneurship': fields.boolean("Asesoría emprendimiento"),
        'innovation': fields.boolean("Innovación del producto"),
        'market': fields.boolean("Ampliar mercado"),
        'company': fields.boolean("Constitución de empresa"),
        'funding': fields.boolean("Financiamiento"),
        'incubation': fields.boolean("Incubación "),
        'design': fields.boolean("Diseño "),
        'company_id': fields.many2one('companies.ihce',"Empresa"),
    }


#~ MERCADOTECNIA
class services_development_bussines(osv.Model):
    _name = 'services.development.bussines'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Servicio", size=100),
    }


class services_laboratory(osv.Model):
    _name = 'services.laboratory'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Servicio", size=100),
    }

class debilidades(osv.Model):
    _name = 'debilidades'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Debilidades", size=100, required=True),
        'mercadotecnia_id': fields.many2one('marketing', "Mercadotecnia"),
    }

class competencias(osv.Model):
    _name = 'competencias'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Competencias", size=100, required=True),
        'mercadotecnia_id': fields.many2one('marketing', "Mercadotecnia"),
    }
    
class necesidades_mercado(osv.Model):
    _name = 'necesidades.mercado'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Necesidades del mercado", size=100, required=True),
        'mercadotecnia_id': fields.many2one('marketing', "Mercadotecnia"),
    }
    
class satisfaccion_cliente(osv.Model):
    _name = 'satisfaccion.cliente'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Nivel de satisfacción del cliente", size=100, required=True),
        'mercadotecnia_id': fields.many2one('marketing', "Mercadotecnia"),
    }

class publicidad(osv.Model):
    _name = 'publicidad'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    #~ 
    _columns = {
        'name': fields.char("Publicidad", size=100, required=True),
        'mercadotecnia_id': fields.many2one('marketing', "Mercadotecnia"),
    }
    

#~ FINANZAS
class financiamiento(osv.Model):
    _name = 'financiamiento'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Financiamiento", size=100, required=True),
    }

class puntos_equilibrio(osv.Model):
    _name = 'puntos.equilibrio'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Punto de equilibrio", size=100, required=True),
    }

class nivel_deuda(osv.Model):
    _name = 'nivel.deuda'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Nivel de deuda", size=100, required=True),
    }


#~ RECURSOS HUMANOS
class frecuencia_capacitacion(osv.Model):
    _name = 'frecuencia.capacitacion'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Frecuencia de capacitación", size=100, required=True),
    }
    

#~ OTROS CATALOGOS PARA LA EMPRESA EN ODOO
class level_knowledge(osv.Model):
    _name = 'level.knowledge'
    #~ _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.char("Nivel de conocimiento", size=64, required=True),
    }


