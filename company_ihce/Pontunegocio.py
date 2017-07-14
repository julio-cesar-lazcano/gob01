#!/usr/bin/env python
#-*- coding:utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta

import time 
import smtplib
import pdb 
# Import the email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

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



    def onchange_age(self, cr, uid, ids, fecha_operaciones2, context=None):
        #pdb.set_trace()
        if fecha_operaciones2 != False:
            return {
                'value':{
                    'amaterno': amaterno.title()
                    }
            }

    def create2(self, cr, uid, vals, context=None):
        uid = 1
        responseL = vals

        dia_1 = str(responseL['dia_1'])
        mes_1 = str(responseL['mes_1'])
        anio_1 = str(responseL['anio_1'])

        

        dia_2 = str(responseL['dia_2'])
        mes_2 = str(responseL['mes_2'])
        anio_2 = str(responseL['anio_2'])

        

        dia_3 = str(responseL['dia_3'])
        mes_3 = str(responseL['mes_3'])
        anio_3 = str(responseL['anio_3'])



        if mes_1 == 'Enero':
            mes_1 = '01'
        if mes_1 == 'Febrero':
            mes_1 = '02'
        if mes_1 == 'Marzo':
            mes_1 = '03'
        if mes_1 == 'Abril':
            mes_1 = '04'
        if mes_1 == 'Mayo':
            mes_1 = '05'
        if mes_1 == 'Junio':
            mes_1 = '06'
        if mes_1 == 'Julio':
            mes_1 = '07'
        if mes_1 == 'Agosto':
            mes_1 = '08'
        if mes_1 == 'Septiembre':
            mes_1 = '09'
        if mes_1 == 'Octubre':
            mes_1 = '10'
        if mes_1 == 'Noviembre':
            mes_1 = '11'
        if mes_1 == 'Diciembre':
            mes_1 = '12'

        if mes_2 == 'Enero':
            mes_2 = '01'
        if mes_2 == 'Febrero':
            mes_2 = '02'
        if mes_2 == 'Marzo':
            mes_2 = '03'
        if mes_2 == 'Abril':
            mes_2 = '04'
        if mes_2 == 'Mayo':
            mes_2 = '05'
        if mes_2 == 'Junio':
            mes_2 = '06'
        if mes_2 == 'Julio':
            mes_2 = '07'
        if mes_2 == 'Agosto':
            mes_2 = '08'
        if mes_2 == 'Septiembre':
            mes_2 = '09'
        if mes_2 == 'Octubre':
            mes_2 = '10'
        if mes_2 == 'Noviembre':
            mes_2 = '11'
        if mes_2 == 'Diciembre':
            mes_2 = '12'

        if mes_3 == 'Enero':
            mes_3 = '01'
        if mes_3 == 'Febrero':
            mes_3 = '02'
        if mes_3 == 'Marzo':
            mes_3 = '03'
        if mes_3 == 'Abril':
            mes_3 = '04'
        if mes_3 == 'Mayo':
            mes_3 = '05'
        if mes_3 == 'Junio':
            mes_3 = '06'
        if mes_3 == 'Julio':
            mes_3 = '07'
        if mes_3 == 'Agosto':
            mes_3 = '08'
        if mes_3 == 'Septiembre':
            mes_3 = '09'
        if mes_3 == 'Octubre':
            mes_3 = '10'
        if mes_3 == 'Noviembre':
            mes_3 = '11'
        if mes_3 == 'Diciembre':
            mes_3 = '12'


        fecha_1 = str(dia_1)  +'-'+ str(mes_1) +'-'+ str(anio_1)
        fecha_2 = str(dia_2)  +'-'+ str(mes_2) +'-'+ str(anio_2)
        fecha_3 = str(dia_3)  +'-'+ str(mes_3) +'-'+ str(anio_3)

        vals.update({'fecha_operaciones1': fecha_1,'fecha_operaciones2': fecha_2,'fecha_operaciones3': fecha_3})

        mail = str(responseL['email1'])

        addr_to   =  mail

        #pdb.set_trace()

        addr_from = 'pontunegociohidalgo@gmail.com'
         
        # Define SMTP email server details
        smtp_server = 'smtp.gmail.com:587'
        smtp_user   = 'pontunegociohidalgo@gmail.com'
        smtp_pass   = '@Orlando1234'
         
        # Construct email
        msg = MIMEMultipart('alternative')
        msg['To'] = addr_to
        msg['From'] = addr_from
        msg['Subject'] = 'yoteapoyo'
         
        # Create the body of the message (a plain-text and an HTML version).
        text = "En este email podras encontrar toda la información del financiamiento solicitado"

        #pdb.set_trace()

        finan = str(responseL['finan'])

        types = str(responseL['types'])


        if types == 'Emprendedor':
            if finan == 'SIEFI':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requi%20IMPULSO.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20emprendedores.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Credito Joven':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/RequisitosJoven.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20emprendedores.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Impulso':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requi%20IMPULSO.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20emprendedores.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Mujer Pyme':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requisitos%20MujerPYME.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20emprendedores.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """

        if types != 'Emprendedor':
            if finan == 'SIEFI':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requi%20IMPULSO.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20Fisicas%20o%20morales.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Credito Joven':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/RequisitosJoven.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20Fisicas%20o%20morales.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Impulso':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requi%20IMPULSO.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20Fisicas%20o%20morales.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
            if finan == 'Mujer Pyme':

                html = """\
                <html>
                  <head></head>
                  <body>
                    <h>Hola """+str(responseL['razon_social1'])+"""</h>
                    <p>En este email podras encontrar la informacion del financiamiento solicitado</p>
                    <img src="http://img.crm-ihce.net/Requisitos%20MujerPYME.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                    </br>
                    <img src="http://img.crm-ihce.net/2%20Fisicas%20o%20morales.jpg" alt="HTML5 Icon" style="width:728px;height:auto;">
                  </body>
                </html>
                """
         
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
         
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
         
        # Send the message via an SMTP server

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(addr_from, addr_to, msg.as_string())
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"






        #return super(web02, self).create(cr, uid, vals)
        return True

