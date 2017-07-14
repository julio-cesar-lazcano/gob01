#!/usr/bin/env python
#-*- coding:utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta
import time 
import smtplib
import pdb 

class web02(osv.Model):
    _name = 'web02'
    
    _columns = {
        #~ Datos Generales de identificación de la Empresa
        'razon_social1': fields.char("Razón social", size=200),
        'no_empleados1': fields.integer("Núm. de empleados", size=5),
        'des_actividad1': fields.char("Descripción de la Actividad Económica", size=400),
        'fecha_operaciones1': fields.date("Fecha inicio de operaciones"),
        'direccion_empresa1': fields.char("Domicilio de la Empresa Calle y Número", size=200),
        'colonia_empresa1': fields.char("Colonia", size=50),
        'localidad1': fields.char("Localidad", size=50),
        'municipio1': fields.char("Municipio", size=50),
        'estado1': fields.char("Estado", size=50),
        'cp1': fields.integer("C.P.", size=6),
        'telefono1': fields.integer("Teléfono", size=12),
        'fax1': fields.integer("Fax", size=20),
        'rfc1': fields.char("R.F.C.", size=20),
        'organismo_empresarial1': fields.char("Cámara u Organismo Empresaria", size=100),
        'email1': fields.char("Correo electrónico", size=100),
        'ref_personales1': fields.integer("Referencias telefónicas personales", size=150),


        #~ Datos del Representante Legal (Persona Moral) o Propietario (Persona Física)
        'razon_social2': fields.char("Razón social", size=200),
        'no_empleados2': fields.integer("Núm. de empleados", size=5),
        'des_actividad2': fields.char("Descripción de la Actividad Económica", size=400),
        'fecha_operaciones2': fields.date("Fecha inicio de operaciones"),
        'direccion_empresa2': fields.char("Domicilio de la Empresa Calle y Número", size=200),
        'colonia_empresa2': fields.char("Colonia", size=50),
        'localidad2': fields.char("Localidad", size=50),
        'municipio2': fields.char("Municipio", size=50),
        'estado2': fields.char("Estado", size=50),
        'cp2': fields.integer("C.P.", size=6),
        'telefono2': fields.integer("Teléfono", size=12),
        'fax2': fields.integer("Fax", size=20),
        'rfc2': fields.char("R.F.C.", size=20),
        'organismo_empresarial2': fields.char("Cámara u Organismo Empresaria", size=100),
        'email2': fields.char("Correo electrónico", size=100),
        'ref_personales2': fields.integer("Referencias telefónicas personales", size=150),
        

        #~ Datos del Aval
        'razon_social3': fields.char("Razón social", size=200),
        'no_empleados3': fields.integer("Núm. de empleados", size=5),
        'des_actividad3': fields.char("Descripción de la Actividad Económica", size=400),
        'fecha_operaciones3': fields.date("Fecha inicio de operaciones"),
        'direccion_empresa3': fields.char("Domicilio de la Empresa Calle y Número", size=200),
        'colonia_empresa3': fields.char("Colonia", size=50),
        'localidad3': fields.char("Localidad", size=50),
        'municipio3': fields.char("Municipio", size=50),
        'estado3': fields.char("Estado", size=50),
        'cp3': fields.integer("C.P.", size=6),
        'telefono3': fields.integer("Teléfono", size=12),
        'fax3': fields.integer("Fax", size=20),
        'rfc3': fields.char("R.F.C.", size=20),
        'organismo_empresarial3': fields.char("Cámara u Organismo Empresaria", size=100),
        'email3': fields.char("Correo electrónico", size=100),
        'ref_personales3': fields.integer("Referencias telefónicas personales", size=150),


        #~ Características del Financiamiento
        'monto_solicitado': fields.integer("Monto del crédito solicitado", size=20),
        'plazo': fields.char("	Plazo", size=20),
        'empleos_proyecta': fields.integer("Empleos que se proyectan generar", size=400),
        'destino_financiamiento': fields.char("Especificar destino del financiamiento", size=400),
		'garantias': fields.char("Especificar Garantías", size=200),
        'valor_comercial': fields.char("Valor comercial actualizado", size=200),

        #~  Observaciones y comentarios del Solicitante 
        'obser': fields.char("Observaciones", size=400),
        'lugar_fecha': fields.char("Lugar y fecha de captura", size=200),
    }
    
    _defaults = {

    }
    
    _order = "date desc"

    def create2(self, cr, uid, vals, context=None):
        pdb.set_trace()
    

        fromadd='pontunegociohidalgo@gmail.com'
        toadd='julio-lazcano@outlook.com'
        #agendaihce@gmail.com

        sbj='Pon tu negocio'
        msg='''Hola,

                En este e-mail se te dan a conocer los documentos necesarios para el financimiento solicitado:

                

                Estamos Atentos a tus solicitudes. 
        '''
        #msg["Subject"] = "Correo de prueba"
        #username='juliogoo0523@gmail.com'
        #passwd='celmi2013'

        username='pontunegociohidalgo@gmail.com'
        passwd='@Orlando1234'

        message = 'Subject: {}\n\n{}'.format(sbj, msg)

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username,passwd)

            server.sendmail(fromadd,toadd,msg)
            print("Mail Send Successfully")
            server.quit()

        except:
            print("Error:unable to send mail")

        return super(web02, self).create(cr, uid, vals)

