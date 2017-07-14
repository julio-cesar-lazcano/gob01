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
from datetime import datetime, date, timedelta
import time 
import pdb 


class login_ihce(osv.Model):
    _name = 'login.ihce'
    
    _columns = {
        'name': fields.char("Nombre de usuario", size=200),
        'password': fields.char("Contraseña", size=25),
        'code': fields.char("Codigo", size=250),
    }

    def create(self, vals):

        rec = super(login_ihce, self).create(vals)
        return rec


class companies_ihce(osv.Model):
    _name = 'companies.ihce'
    
    _columns = {
        #~ Datos de atención
        'registro_inadem': fields.boolean("Registrado en INADEM"),
        'dependence': fields.selection([('0','IHCE'),('1','Emprered')], "Dependencia"),
        'ihce': fields.many2one('responsible.area', "Área ihce"),
        'emprered': fields.many2one('emprereds', "Emprered"),
        'type': fields.selection([('emprendedor','Emprendedor'),('fisica','Persona fisica'),('moral','Persona moral')], "Estatus legal",help="Tipo de registro: Emprendedor, Persona física o Persona moral"),
        #~ Datos generales empresa
        'company_name': fields.char("Razón social", size=200),
        'name_commercial': fields.char("Nombre comercial", size=200),
        'rfc_company': fields.char("RFC Empresa", size=20),
        'phone_company': fields.char("Teléfono fijo", size=15),
        'fax_company': fields.char("Fax", size=15),
        'street_company': fields.char("Calle", size=100),
        'external_number_company': fields.char("Número exterior", size=10),
        'internal_number_company': fields.char("Número interior", size=10),
        'colony_company': fields.many2one('colony.hidalgo',"Colonia"),
        'city_company': fields.many2one('states.mexico',"Estado"),
        'town_company': fields.many2one('town.hidalgo',"Municipio"),
        'cp_company': fields.char("Código postal", size=5),
        'country_company': fields.char("País", size=100),
        'region_company': fields.many2one('region.hidalgo',"Región"),
        'web': fields.char("Sitio web", size=64),
        #~ Datos generales personas
        'name': fields.char("Nombre Completo", size=200),
        'name_people': fields.char("Nombre", size=200),
        'apaterno': fields.char("Apellido paterno", size=100),
        'amaterno': fields.char("Apellido materno", size=100),
        'rfc': fields.char("RFC", size=20),
        'date_birth': fields.date("Fecha de nacimiento"),
        'place_birth': fields.many2one('states.mexico',"Lugar de nacimiento"),
        'sexo': fields.selection([('F','Femenino'),('M','Masculino')], "Sexo"),
        'civil_status': fields.selection([('1','Soltero (a)'),('2','Casado (a)'),('3','Divorciado (a)'),('4','Viudo (a)'),('5','Unión libre'),('6','Separado (a)')], "Estado civil"),
        'school': fields.many2one('escolaridad', "Escolaridad"),
        'population_characteristics': fields.many2one('caracteristica.poblacional',"Característica poblacional"),
        'phone': fields.char("Teléfono fijo", size=30),
        'cel_phone': fields.char("Teléfono móvil", size=30),
        'street': fields.char("Calle", size=100),
        'external_number': fields.char("Número exterior", size=10),
        'internal_number': fields.char("Número interior", size=10),
        'colony': fields.many2one('colony.hidalgo',"Colonia"),
        'city': fields.many2one('states.mexico',"Estado"),
        'town': fields.many2one('town.hidalgo',"Municipio"),
        'cp': fields.char("Código postal", size=5),
        'country': fields.char("País", size=100),
        'region': fields.many2one('region.hidalgo',"Región"),
        'curp': fields.char("CURP", size=25),
        'fax': fields.char("Fax", size=15),
        'occupation': fields.char("Ocupación", size=64),
        'email': fields.char("Correo electrónico", size=100),
        'disabled': fields.boolean("Es discapacitado"),
        'indian': fields.boolean("Es indígena"),
        #~ Actividad Económica
        'size': fields.many2one('tamano.actividad.economica',"Tipo",help="Tipo de empresa de acuerdo a su tamaño"),
        'sector': fields.many2one('sector.actividad.economica',"Sector",help="Sector económico"),
        'sales_year': fields.many2one('ventas.anuales.actividad.economica',"Ventas anuales"),
        'enmprendedor_activity': fields.many2one('emprendedor.actividad.economica',"Emprendedor con"),
        'type_activity_empre': fields.many2one('tipo.emprendedor.actividad.economica',"Tipo de Actividad Económica de Emprendedor"),
        'staff': fields.integer("No. de Empleados"),
        'staff_imss': fields.integer("No. de Empleados con IMSS"),
        'men': fields.integer("No. de Hombres"),
        'woman': fields.integer("No. de Mujeres"),
        'indians': fields.integer("No. de Indígenas"),
        'disableds': fields.integer("No. de Discapacitados"),
        'operations': fields.date("Inicio de operaciones"),
        'branches': fields.integer("No. de sucursales"),
        'product': fields.char("Productos", size=25),


        #~ Areas de Desarrollo
        'area_development': fields.one2many('development.areas', 'company_id', 'Áreas de Interés'),
        #~ Negocio
        'mission_bo': fields.boolean("Misión"),
        'vision_bo': fields.boolean("Visión"),
        'values_bo': fields.boolean("Valores"),
        'mission': fields.text("Misión"),
        'vision': fields.text("Visión"),
        'values': fields.text("Valores"),
        'procedures': fields.boolean("Manual de procedimientos"),
        'organization': fields.boolean("Manual de organización"),
        'family_business': fields.boolean("Empresa familiar"),
        'increase': fields.boolean("Plan de crecimiento"),
        'alternatives': fields.boolean("Alternativas para su crecimiento"),
        'business': fields.boolean("Plan de negocios"),
        'market': fields.boolean("Estudio de mercados"),
        'model_business': fields.boolean("Modelo de negocios"),
        #~ Mercadotecnia
        'marketing_de_lines': fields.one2many('services.de.lines', 'company_id', 'Servicios de Desarrollo Empresarial'),
        'marketing_lab_lines': fields.one2many('services.lab.lines', 'company_id', 'Servicios de Laboratorio'),
        'merchandising': fields.selection([('local','Local'),('estatal','Estatal'),('nacional','Nacional'),('internacional','Internacional')], "Comercialización"),
        'promotions': fields.text("Promociones"),
        'internet': fields.boolean("Presencia en internet"),
        'social_media': fields.boolean("Plan de medios sociales"),
        #~ Finanzas
        'funding': fields.many2one('financiamiento',"Financiamiento"),
        'costs': fields.boolean("Costos de producción"),
        'breakeven': fields.many2one('puntos.equilibrio',"Punto de equilibrio"),
        'margin': fields.boolean("Margen de utilidad "),
        'credit': fields.boolean("Cuenta con crédito"),
        'debt': fields.many2one('nivel.deuda',"Nivel de deuda"),
        'required_credit': fields.boolean("Requiere un crédito"),
        'capital': fields.boolean("Requiere capital (socios)"),
        #~ Recursos Humanos
        'booking': fields.boolean("Procedimiento de contratación"),
        'contracts': fields.boolean("Contratos individuales de trabajo"),
        'training': fields.boolean("Programa de capacitación"),
        'frequency': fields.many2one('frecuencia.capacitacion',"Frecuencia de capacitación"),
        #~ Producción
        'quantity': fields.integer("Cantidad de producción anual"),
        'unit': fields.char("Unidad", size=64),
        #~ 'machine_old': fields.integer("Antiguedad de la maquinaria"),
        'rule': fields.boolean("Requiere norma de certificación"),
        #~ 'rule_required': fields.char("Norma de Certificación que requiere"),
        'certification': fields.boolean("Cuenta con la certificación"),
        #~ Otros datos
        'increase_annual_sales': fields.integer("Incremento en ventas anuales (%)"),
        'old_tax': fields.integer("Antiguedad fiscal"),
        'level_knowledge': fields.many2one('level.knowledge',"Nivel de conocimiento"),
        'note': fields.text("Notas"),
        'crm': fields.one2many('crm.ihce', 'company_id',"Historial"),
        'parent_id': fields.many2one('companies.ihce', 'Related Company', select=True),
        'parent_name': fields.related('parent_id', 'name', type='char', readonly=True, string='Parent name'),
        'child_ids': fields.one2many('companies.ihce', 'parent_id', 'Contacts'),
        'company': fields.boolean("Empresa"),
        'contact': fields.boolean("Contacto"),
        'num_inadem': fields.char("NURAE", size=64),
        'login_id': fields.many2one('login.ihce', "Login"),
        'state': fields.selection([('draft','En espera'),('done','Aceptada'),('rechazada','Rechazada')], "Estado"),
        'diagnostico': fields.boolean("Diagnóstico"),
        'regimen': fields.boolean("Regimen"),
        'street_company_contact': fields.boolean("Dirección de la compañia"),
        'innovacion_emp': fields.boolean("Innovaión"),
        'innovacion_emp_text': fields.text("Notas"),
        'emprendimiento': fields.boolean("Emprendimiento"), 
        'emprendimiento_text': fields.text("Notas"),
        'emprendimiento_vinc': fields.text("Motivo de Vinculación"),
        'formacion_capital_humano': fields.boolean("Formación de Capital Humano"),
        'formacion_capital_humano_text': fields.text("Notas"),
        'formacion_capital_humano_vinc': fields.text("Motivo de Vinculación"),
        'desarrollo_empresarial': fields.boolean("Desarrollo Empresarial"),
        'desarrollo_empresarial_text': fields.text("Notas"),
        'desarrollo_empresarial_vinc': fields.text("Motivo de vinculación"),
        'laboratorio': fields.boolean("Laboratorio de Diseño"),
        'laboratorio_text': fields.text("Notas"),
        'laboratorio_vinc': fields.text("Motivo de Vinculación"),
        'acompanamiento_empresarial': fields.boolean("Acompañamiento Empresarial"),
        'financiamiento': fields.boolean("Financiamiento"),
        'aceleracion_empresarial': fields.boolean("Aceleración Empresarial"),
        'aceleracion_empresarial_text': fields.text("Notas"),
        'aceleracion_empresarial_vinc': fields.text("Motivo de Vinculación"),
        'idea_commerce': fields.char('Idea de Negocio', size=250),
        'name_comercial': fields.char('Nombre Comercial', size=250),
        'date': fields.date("Fecha de registro"),
        'area_related': fields.many2many('related.areas','area_company_rel', 'company_id', 'area_related', "Otras Áreas Vinculadas"),
        'contact_principal': fields.boolean("Contacto Principal"),
        'name_contact': fields.char('Contacto Principal', size=200),
        'phone_contact': fields.char('Teléfono', size=20),
        'mail_contact': fields.char('Correo Electrónico', size=50),
        'services_de': fields.many2one('services.development.bussines', "Servicio"),
        'services_lab': fields.many2one('services.laboratory', "Servicio"),
        'asesorias_ids': fields.one2many('asesorias.ihce', 'company_id', 'Asesorías'),
        'servicios_ids': fields.one2many('servicios.ihce', 'company_id', 'Servicios'),
        'code': fields.char("Codigo", size=250),
        'confirm_email': fields.boolean("Correo confirmado"),
        'user_login': fields.char('User Login', size=50),
        'password_login': fields.char('Password login', size=50),
        'atention_area': fields.many2one('atention.area', "Areas de atención"),
        'visit_area': fields.char("Áreas a Visitar"),
        'tramit': fields.char("Tramite"),
        #~ Datos solicitados por IHCE
        #~ Datos de Directorio
        'Camara_Asociacion': fields.char('Cámara o Asociación', size=50),
        'Origen': fields.char('Origen', size=50),
        'Inicio_Operaciones': fields.char('Año de Inicio de Operaciones', size=50),
        'Productos_Servicios': fields.char('Principales Productos o Servicios', size=50),
        'Tecnologia_Innovacion': fields.char('Actividades de Ciencia,Tecnología e Innovación', size=50),
        'Exporta': fields.char('Exporta', size=50),
        'Pagina_Web': fields.char('Página Web', size=50),
        'Asistente_Nombre': fields.char('Nombre Asistente', size=50),
        'Asistente_Paterno': fields.char('Apellido Paterno Asistente', size=50),
        'Asistente_Materno': fields.char('Apellido Materno Asistente', size=50),
        'Asistente_Cargo': fields.char('Cargo Asistente', size=50),
        'Asistente_Telefono1': fields.char('Teléfono 1 con Clave Lada Asistente', size=50),
        'Asistente_Telefono2': fields.char('Teléfono 2 con Clave Lada Asistente', size=50),
        'Asistente_Email': fields.char('Correo Electrónico', size=50),
        'Asistente_Financiamiento': fields.boolean('Financiamiento'),
        'Asistente_Subsidio': fields.boolean('Subsidio'),
        'Asistente_Incentivo_Fiscal': fields.boolean('Incentivo Fiscal'),
        'Asistente_Asesoria': fields.boolean('Asesoría'),
        'Asistente_Capacitacion': fields.boolean('Capacitación'),
        'Asistente_Primer_Empleo': fields.boolean('Becarios de Primer Empleo'),
        'Asistente_Gestion': fields.boolean('Gestión'),
        'Asistente_Acompanamiento': fields.boolean('Acompañamiento'),
    }
    
    _defaults = {
        'state': 'draft',
        'country': 'México',
        'company': True,
        'contact': False,
        'street_company_contact': True,
        'emprendimiento': False,
        'formacion_capital_humano': False,
        'desarrollo_empresarial': False,
        'laboratorio': False,
        'acompanamiento_empresarial': False,
        'financiamiento': False,
        'aceleracion_empresarial': False,
        'contact_principal': False,
        'diagnostico': True,
        'registro_inadem': False,
    }
    
    _order = "date desc"
    
    def _validated_inadem(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        existe = self.search(cr, uid, [('num_inadem','=',str(row.num_inadem))])
        
        if len(existe) > 1:
            return False
        else:
            return True
    
    _constraints = [(_validated_inadem, "Error: El Número INADEM ingresado ya existe en otro registro.", ['num_inadem'])]
    
    def create(self, cr, uid, vals, context=None):
        nombre = vals.get('name_people')
        nombreComercial = vals.get('name_commercial')
        apellidop = vals.get('apaterno')
        apellidoM = vals.get('amaterno')

        if nombre:

            if nombreComercial:

                vals.update({'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now(),'name': nombreComercial,'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now()})
            else:

                nombreR = nombre+" "+ apellidop +" "+ apellidoM
                vals.update({'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now(),'name': nombreR,'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now()})


        #if parent != False or parent != None:
         #   row = self.browse(cr, uid, parent, context=context)
            
          #  if vals.get('contact_principal') == True:
           #     contact_ids = self.search(cr, uid, [('parent_id', '=', row.id)])
            #    for ro in contact_ids:
             #       self.write(cr, uid, ro, {'contact_principal': False})
                
              #  self.write(cr, uid, row.id, {'name_contact': vals.get('name'), 'phone_contact': vals.get('cel_phone'), 'mail_contact': vals.get('email')})
     #           vals.update({'contact_principal': True, 'company': False,'contact':True, 'state':row.state})
      #      else:
       #         vals.update({'company': False,'contact':True, 'state':row.state})
       
       #Actulización de Julio Cesar Lazcano, No se ve el contacto por que no se guardaba el nombreComercial y 
       #por lo tanto en el inicio de beneficiarios no se podia ver
#        existe = self.search(cr, uid, [('rfc','=',rfc)])
    
        rfc = vals.get('rfc')
        typeP = vals.get('type')

        if typeP:
            
            if typeP != "emprendedor":
                existe = self.search(cr, uid, [('rfc','=',rfc)])
                #pdb.set_trace()
            else:
                existe = False

            if existe:
                #pdb.set_trace()
                raise osv.except_osv(('Error'), ('No se puede guardar el mismo RFC'))
                #return False
            else:
                return super(companies_ihce, self).create(cr, uid, vals, context)


    def create2(self, cr, uid, vals, context=None):
        #pdb.set_trace()
        return super(companies_ihce, self).create(cr, uid, vals)

    def verifica_rfc(self, cr, uid, ids, rfc, name_pe, paterno, materno, fecha, context=None):
        vocales = ['A','E','I','O','U']
        existe = self.search(cr, uid, [('rfc','=',rfc.upper())],context=context)

        if len(existe) <= 1:
            if paterno[0].upper() == rfc[0].upper() and rfc[1].upper() in vocales and rfc[2].upper() == materno[0].upper() and rfc[3].upper() == name_pe[0].upper(): 
                if rfc[4:6] == fecha[2:4] and rfc[6:8] == fecha[5:7] and rfc[8:10] == fecha[8:]:
                    if len(rfc) >= 10 and len(rfc) <= 14:
                        return True
                    else:
                        raise osv.except_osv(_('Advertencia!'), _('El RFC no es correcto. Excede los caracteres permitidos!'))
                        return False
                else:
                    raise osv.except_osv(_('Advertencia!'), _('El RFC no es correcto. La fecha de nacimiento no coincide.!'))
                    return False
            else:
                if rfc.upper() == 'XAXX010101000':
                    return True
                else:
                    raise osv.except_osv(_('Advertencia!'), _('El RFC no es correcto. El nombre y apellidos no coinciden!'))
                    return False
        else:
            raise osv.except_osv(_('Advertencia!'), _('No puede guardar los datos, el RFC ya existe.!'))
            return False
            

    #~ Se agrega una linea al historial de la empresa dependiendo de si el campo validado es seleccionado.
    def write(self, cr, uid, ids, values, context=None):
        fecha_actual = datetime.now()
        
        if values.get('idea_commerce'):
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'name':'La idea del negocio cambio a ' + values.get('idea_commerce'), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            
        if values.get('name_people') or values.get('apaterno') or values.get('amaterno') or values.get('date_birth') or values.get('rfc') or values.get('company_name') or values.get('name_commercial') or values.get('name_commercial') == False:
            row = self.browse(cr, uid, ids[0], context=context)
            rfc = values.get('rfc') or row.rfc
            tipo = values.get('type') or row.type
            name_pe = values.get('name_people') or row.name_people
            paterno = values.get('apaterno') or row.apaterno
            materno = values.get('amaterno') or row.amaterno
            fecha = values.get('date_birth') or row.date_birth
            name = row.name

            if values.get('name_commercial') != False and values.get('name_commercial') != None:
                comercial = values.get('name_commercial')
            else:
                if values.get('name_commercial') == False:
                    comercial = ''
                else:
                    if values.get('name_commercial') == None:
                        comercial = row.name_commercial

            if tipo == 'moral':
                if comercial:
                    name = comercial
                else:
                    if values.get('company_name'):
                        name = values.get('company_name')
                    else:
                        name = row.company_name
            else:
                if comercial:
                    name = comercial
                else:
                    name = name_pe + " " + paterno + " " + materno
            
            if tipo == 'fisica':
                self.verifica_rfc(cr, uid, ids, rfc, name_pe, paterno, materno, fecha, context=context)
                values.update({'name': name, 'rfc': rfc.upper()})
            else:
                values.update({'name': name})
        
        #Modificación relizada por Julio Cesar Lazcano ya que solo admitia transacciones de Personas Fisicas
        #if values.get('emprendimiento') == True or values.get('emprendimiento') == False or values.get('formacion_capital_humano') == True or values.get('formacion_capital_humano') == False or values.get('desarrollo_empresarial') == True or values.get('desarrollo_empresarial') == False or values.get('aceleracion_empresarial') == True or values.get('aceleracion_empresarial') == False:

        if values.get('emprendimiento') == True or values.get('emprendimiento') == False or values.get('formacion_capital_humano') == True or values.get('formacion_capital_humano') == False or values.get('desarrollo_empresarial') == False or values.get('aceleracion_empresarial') == True or values.get('aceleracion_empresarial') == False:
            self.sinc_vinculation(cr, uid, ids, values, context=context)
            
        values.update({'emprendimiento_vinc': values.get('emprendimiento_text'), 'formacion_capital_humano_vinc': values.get('formacion_capital_humano_text'),'desarrollo_empresarial_vinc': values.get('desarrollo_empresarial_text'),'laboratorio_vinc': values.get('laboratorio_text'),'aceleracion_empresarial_vinc': values.get('aceleracion_empresarial_text')})
        
            
        return super(companies_ihce,self).write(cr, uid, ids, values, context=context)
    
    #~ Función para mostrar las colonias correspondientes al municipio seleccionado
    def onchange_town(self, cr, uid, ids, town_id, context=None):
        res = {'domain': {'colony': []}}
        if town_id:
            res['domain'] = {'colony': [('town_id','=',town_id)]}
        return res
    
    #~ Valida empresa
    def confirm(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        anio_indi = fecha_actual.year
        row = self.browse(cr, uid, ids[0], context=context)
        data_ids = self.search(cr, uid, [('parent_id','=',row.id)])
        
        #~ Agregamos region de acuerdo al municipio
        if row.type == 'moral':
            data = self.pool.get('town.hidalgo').browse(cr, uid, row.town_company.id, context=context)
            dat = self.pool.get('town.hidalgo').browse(cr, uid, row.town.id, context=context)
            if dat:
                self.write(cr, uid, [ids[0]], {'region_company': data.region_id.id, 'region': dat.region_id.id})
        else:
            dat = self.pool.get('town.hidalgo').browse(cr, uid, row.town.id, context=context)
            if dat:
                self.write(cr, uid, [ids[0]], {'region': dat.region_id.id})
        
        if row.diagnostico:

            #~ Clasificamos a la empresa en su nivel de conocimiento de acuerdo al tiempo de operaciones
            if row.type == 'emprendedor':
                self.write(cr, uid, [row.id], {'level_knowledge': '1'})
            else:
                if row.operations:
                    anio = int(row.operations[0:4])
                    anio_act = fecha_actual.year
                    anios = anio_act - anio
                    if anios <= 1:
                        self.write(cr, uid, [row.id], {'level_knowledge': '2'})
                    elif anios > 1 and anios <= 3:
                        self.write(cr, uid, [row.id], {'level_knowledge': '3'})
                    elif anios > 3:
                        self.write(cr, uid, [row.id], {'level_knowledge': '4'})
                else:
                    self.write(cr, uid, [row.id], {'level_knowledge': '1'})
                        
            #~ Verificamos si la empresa tiene diagnostico, de no ser asi, no la podemos validar
            if row.level_knowledge:
                self.write(cr, uid, [ids[0]], {'state':'done'})
                
                name_contact = row.name_people + " " + row.apaterno + " " + row.amaterno
                #~ Creamos un primer contacto, con el representante de la empresa o con la persona fisica o emprendedor
                datos_con = {
                    'name': name_contact,
                    'street': row.street,
                    'external_number': row.external_number,
                    'city': row.city.id,
                    'town': row.town.id,
                    'colony': row.colony.id,
                    'cp': row.cp,
                    'cel_phone': row.cel_phone,
                    'civil_status': row.civil_status,
                    'population_characteristics': row.population_characteristics.id,
                    'phone': row.phone,
                    'sexo': row.sexo,
                    'email': row.email,
                    'school': row.school.id,
                    'date_birth': row.date_birth,
                    'parent_id': row.id,
                    'contact': True,
                    'company': False,
                    'contact_principal': True,
                }
                self.create(cr, uid, datos_con, context=context)
                
                #~ Asiganamos a los contactos el estado de su empresa padre.
                for data in self.browse(cr, uid, data_ids, context=context):
                    self.write(cr, uid, [data.id], {'state':'done'})
                
                self.pool.get('crm.ihce').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'name':'Empresa validada', 'user':uid, 'date_compromise':fecha_actual, 'state':'done'}, context=context)
                
                if row.type != 'emprendedor':
                    #~ Craemos la linea de historial de empleados.
                    self.pool.get('staff.history').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'staff': row.staff}, context=context)
            else:
                raise osv.except_osv(_('Advertencia!'), _('Ingrese nivel de conocimiento.!'))
        else:
            raise osv.except_osv(_('Advertencia!'), _('No puedes validar la empresa sin diagnóstico!'))
        
        return True
    
    def no_confirm(self, cr, uid, ids, context=None):
        fecha_actual = datetime.now()
        anio = fecha_actual.year
        row = self.browse(cr, uid, ids[0], context=context)
        data_ids = self.search(cr, uid, [('parent_id','=',ids[0])])
        
        self.write(cr, uid, [ids[0]], {'state':'draft'})
        for data in self.browse(cr, uid, data_ids, context=context):
            self.write(cr, uid, [data.id], {'state':'draft'})
            
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'name':'Empresa por validar', 'user':uid, 'date_compromise':fecha_actual, 'state':'done'}, context=context)
        
        return True
    
    def onchange_street(self, cr, uid, ids, valor, conte, context=None):
        result = {}
        result['value'] = {}
        
        parent_id = conte.get('default_parent_id')
        data = self.browse(cr, uid, parent_id, context=context)
        
        if valor == False:
            result['value'].update({'street': '', 'external_number': '', 'internal_number': '', 'country': '', 'city': '', 'town': '', 'region': '' , 'colony': '', 'cp': '' })
        else:
            if valor == True:
                if data.type == 'moral':
                    result['value'].update({'street': data.street_company, 'external_number': data.external_number_company, 'internal_number': data.internal_number_company, 'country': data.country_company, 'city': data.city_company, 'town': data.town_company, 'region': data.region_company , 'colony': data.colony_company, 'cp': data.cp_company })
                else:
                    result['value'].update({'street': data.street, 'external_number': data.external_number, 'internal_number': data.internal_number, 'country': data.country, 'city': data.city, 'town': data.town, 'region': data.region , 'colony': data.colony, 'cp': data.cp })
        
        return result
    
    def rechazar(self, cr, uid, ids, context=None):
        fecha_actual = date.today()

        row = self.browse(cr, uid, ids[0], context=context)
        data_ids = self.search(cr, uid, [('parent_id','=',row.id)])
        
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'name':'Empresa rechazada', 'user':uid, 'date_compromise':fecha_actual, 'state':'done'}, context=context)
        
        for data in self.browse(cr, uid, data_ids, context=context):
            self.write(cr, uid, [data.id], {'state':'rechazada'})
        
        self.write(cr, uid, [row.id], {'state': 'rechazada'}, context=context)
        
    def unlink(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for row in data:
            line = self.browse(cr, uid, row['id'], context=context)
            if line.contact == True:
                unlink_ids.append(row['id'])
            else:
                if row['state'] in ['rechazada']:
                    unlink_ids.append(row['id'])
                    rows_ids = self.search(cr, uid, [('parent_id','=',row['id'])])
                    for ro in rows_ids:
                        unlink_ids.append(ro)
                else:
                    raise osv.except_osv(_('Acción Invalida!'), _('No puede eliminar el registro de una empresa.!'))

        return super(companies_ihce, self).unlink(cr, uid, unlink_ids, context=context)

    def sinc_vinculation(self, cr, uid, ids, values, context=None):

        #~ Obtenemos los valores de la empresa con las áreas que ya está vinculada a partir del diagnóstico
        data = self.browse(cr, uid, ids[0], context=context)
        fecha_actual = datetime.now()
        
        if values.get('emprendimiento') == True:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se vinculo a Emprendimiento', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            #~ Se envía correo
            self.send_mail_vinc(cr, uid, ids, 5, context=context)
        elif values.get('emprendimiento') == False:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se desvinculo de Emprendimiento', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        elif values.get('formacion_capital_humano') == True:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se vinculo a Formación de Capital Humano', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            #~ Se envía correo
            self.send_mail_vinc(cr, uid, ids, 2, context=context)
        elif values.get('formacion_capital_humano') == False:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se desvinculo de Formación de Capital Humano', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        elif values.get('desarrollo_empresarial') == True:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se vinculo a Desarrollo Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            #~ Se envía correo
            self.send_mail_vinc(cr, uid, ids, 4, context=context)
        elif values.get('desarrollo_empresarial') == False:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se desvinculo de Desarrollo Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        elif values.get('aceleracion_empresarial') == True:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se vinculo a Aceleración Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            #~ Se envía correo
            self.send_mail_vinc(cr, uid, ids, 8, context=context)
        elif values.get('aceleracion_empresarial') == False:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se desvinculo de Aceleración Empresarial', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        elif values.get('laboratorio') == True:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se vinculo a Laboratorio de Diseño', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
            #~ Se envía correo
            self.send_mail_vinc(cr, uid, ids, 10, context=context)
        elif values.get('laboratorio') == False:
            self.pool.get('crm.ihce').create(cr, uid, {'company_id': data.id, 'date':fecha_actual, 'name':'Se desvinculo de Laboratorio de Diseño', 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        return True

    def send_mail_vinc(self, cr, uid, ids, area_id, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        titulo = "Vinculación Emprendedores"
        texto = "<p>Se te ha vinculado al beneficiario "+str(row.name.encode('utf-8'))+". Favor de revisar en el sistema que requiere.\nGracias</p> "
        
        #~ Buscamos a todos los usuarios del área correspondiente y se le envía correo
        user_ids = self.pool.get('res.users').search(cr, uid, [('area','=',area_id)])
        for line in self.pool.get('res.users').browse(cr, uid, user_ids):
            self.pool.get('mail.ihce').send_mail_user(cr, uid, ids, titulo, texto, line.id, context=context)
        
        return True
        
    def staff_button(self, cr, uid, ids, context=None):
        data = self.pool.get('staff.history').search(cr, uid, [('company_id','=',ids[0])], context=context)
        domain = [('company_id', '=', ids[0])]

        return {
            'name': "Historial de empleados",
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'staff.history',
            'type': 'ir.actions.act_window',
            'res_id': data,
            'nodestroy': True,
            'target': 'new',
            'domain': domain,
        }
    
    
    def onchange_staff(self, cr, uid, ids, men, woman, indians, disableds, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()
        
        staff = men + woman + indians + disableds
        result['value'].update({'staff': staff})
        
        return result
    
    def onchange_staff_his(self, cr, uid, ids, staff, men, woman, indias, disable, context=None):
        result = {}
        result['value'] = {}
        fecha_actual = datetime.now()

        if ids:
            #~ Craemos la linea de historial de empleados.
            self.pool.get('staff.history').create(cr, uid, {'company_id': ids[0], 'date':fecha_actual, 'staff': staff,'man': men, 'woman': woman, 'indians': indias, 'disabled': disable}, context=context)
        
        return result
        
    def add_de_lines(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        
        emp = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        #companies_.login
        #companies_.name
        #companies_.option
        #pdb.set_trace()
        self.pool.get('services.de.lines').create(cr, uid, {'name': row.services_de.id, 'service': True, 'company_id': row.id})
        if emp.emprered.id:
            self.pool.get('register.trademark').create(cr, uid, { 'emprered':emp.emprered.id, 'company_id': row.id, 'receiving_record': True, 'phonetic_search': True, 'vobo_format': True, 'servicio': True, 'impi': True, 'send_format': True, 'change_user': True, 'application_format': True})
        else:
            self.pool.get('register.trademark').create(cr, uid, {'company_id': row.id, 'receiving_record': True, 'phonetic_search': True, 'vobo_format': True, 'servicio': True, 'impi': True, 'send_format': True, 'change_user': True, 'application_format': True})
        return True
    
    def add_lab_lines(self, cr, uid, ids, context=None):
        row = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('services.lab.lines').create(cr, uid, {'name': row.services_lab.id, 'service': True, 'company_id': row.id})
        return True
        
        
class services_de_lines(osv.Model):
    _name = 'services.de.lines'
    
    _columns = {

        'name': fields.many2one('services.development.bussines',"Servicio"),
        'service': fields.boolean("Requiere"),
        'company_id': fields.many2one('companies.ihce',"Beneficiario"),
    }


class services_lab_lines(osv.Model):
    _name = 'services.lab.lines'

    _columns = {
        'name': fields.many2one('services.laboratory',"Servicio"),
        'service': fields.boolean("Requiere"),
        'company_id': fields.many2one('companies.ihce',"Beneficiario"),
    }

    
class staff_history(osv.osv_memory):
    _name = 'staff.history'

    _columns = {
        'company_id':fields.many2one('companies.ihce', "Beneficiario"),
        'staff':fields.integer("No. de empleados"),
        'man':fields.integer("No. de hombres"),
        'woman':fields.integer("No. de mujeres"),
        'indians':fields.integer("No. de indigenas"),
        'disabled':fields.integer("No. de discapacitados"),
        'date':fields.datetime("Fecha"),
    }
            
    _rec_name = 'company_id'
