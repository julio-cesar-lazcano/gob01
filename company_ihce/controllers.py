# coding=utf-8
from openerp.osv import fields, osv
from openerp import models, fields, api, exceptions, tools, SUPERUSER_ID 
from openerp.tools.translate import _
from openerp import http
from datetime import datetime
import locale
import sys
import pdb
import smtplib
reload(sys)
sys.setdefaultencoding('utf-8')
#pdb.set_trace()

class Register(http.Controller): 

    @http.route('/signup/', auth='public', website=True, methods=['GET'])
    def index(self, **kw): 
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        
        i = [] 
        for x in atentionareas:
            i.append(x.name) 
 
        emprered = http.request.env['emprereds']
        emprereD = emprered.search([('name','!=','')])

        ie = []
        for x in emprereD:
            ie.append(x.name)

        return http.request.render('company_ihce.form', {            
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'areas': i,
            'empr': ie,
        })

    @http.route('/signup/', auth='public', website=True, methods=['POST'])
    def reg(self, **kw):
        print "INSIDE" + str(http.request.params)

        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']
        Res = http.request.env['res.users']
        emprered = http.request.env['emprereds']
        #pdb.set_trace()
        #------------------------------Aqui va el listado de areas de atencion-------------#
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        i = []
        for x in atentionareas:
            i.append(x.name)
        #------------------------------Consulta si el user_login existe-------------# 
        responseL = http.request.params
        responsel = str(responseL['user_l'])
        empreredname = str(responseL['empr'])

        usuarioActivo = Companies.search([('user_login','=',responsel)])
        emprereId = emprered.search([('name','=',empreredname)])


        iemp = []
        for x in emprereId:
            iemp.append(x.id) 


        nombre = str(responseL['name_people']) + " " + str(responseL['apaterno']) + " " + str(responseL['amaterno']) 



        emprereD = emprered.search([('name','!=','')])

        ie = []
        for x in emprereD:
            ie.append(x.name)


        types = str(responseL['types'])

      
        if types == "Emprendedor":
            types = "emprendedor"
        if types == "Persona Fisica":
            types = "fisica"
        if types == "Persona Moral":
            types = "moral"

        types_areas = str(responseL['areas'])
        if types_areas == "Administrativo":
            types_areas = 1
        if types_areas == "Formación de Capital Humano":
            types_areas = 2
        if types_areas == "Agencia de Innovación Empresarial":
            types_areas = 3
        if types_areas == "Financiamiento":
            types_areas = 4
        if types_areas == "Fondo Emprendedor":
            types_areas = 5
        if types_areas == "Laboratorio de Diseño":
            types_areas = 6
        if types_areas == "Dirección General":
            types_areas = 7
        if types_areas == "Emprendimiento":
            types_areas = 8
        if types_areas == "Acompañamiento Empresarial":
            types_areas = 9

        var = len(usuarioActivo)
        if var == 0 :
            #pdb.set_trace()
            http.request.params.update({'name_commercial':nombre, 'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now(),'name': nombre,'emprered': iemp[0], 'user_login':responsel, 'atention_area':types_areas, 'type':types})
            com = Companies.create2(http.request.params)
            #com.write({})
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Gracias por registrarte.',
            'areas': i,
            'empr': ie,
            })
            
        else :
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'No Registrado',
            'areas': i,
            'empr': ie,
            })





class RegistroFinanciamiento(http.Controller): 

    @http.route('/RegistroFinanciamiento/', auth='public', website=True, methods=['GET'])
    def index(self, **kw): 
        

        return http.request.render('company_ihce.form_fina', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],            
            'finan': ['SIEFIH','Credito Joven','Impulso', 'Mujer Pyme'],
            'dia': ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
            'mes': ['Enero','Febrero', 'Marzo', 'Abril','Mayo', 'Junio','Julio', 'Agosto', 'Septiembre','Octubre','Noviembre','Diciembre'],
            'anio': ['1950','1951', '1952', '1953','1954', '1955','1956', '1957', '1958','1959','1960','1961','1962','1963', '1964', '1965','1966', '1967','1968', '1969', '1970','1971','1972','1973','1974','1975', '1976', '1977','1978', '1979','1980', '1981', '1982','1983','1984','1985','1986','1987', '1988', '1989','1990', '1991','1992', '1993', '1994','1995','1996','1997','1998','1999', '2000', '2001','2002', '2003','2004', '2005', '2006','2007','2008','2009','2010','2011', '2012', '2013','2014', '2015','2016', '2017', '2018','2019','2020'],
        })

    @http.route('/RegistroFinanciamiento/', auth='public', website=True, methods=['POST'])
    def reg(self, **kw):
        w = http.request.env['web02']
        http.request.params
        uid = 1
        #pdb.set_trace()
       # http.request.params.update({'name_commercial':nombre, 'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now(),'name': nombre,'emprered': iemp[0], 'user_login':responsel, 'atention_area':types_areas, 'type':types})
        com = w.create2(http.request.params)
        return http.request.render('company_ihce.form_fina', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'finan': ['SIEFI','Credito Joven','Impulso', 'Mujer Pyme'],
            'dia': ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
            'mes': ['Enero','Febrero', 'Marzo', 'Abril','Mayo', 'Junio','Julio', 'Agosto', 'Septiembre','Octubre','Noviembre','Diciembre'],
            'anio': ['1950','1951', '1952', '1953','1954', '1955','1956', '1957', '1958','1959','1960','1961','1962','1963', '1964', '1965','1966', '1967','1968', '1969', '1970','1971','1972','1973','1974','1975', '1976', '1977','1978', '1979','1980', '1981', '1982','1983','1984','1985','1986','1987', '1988', '1989','1990', '1991','1992', '1993', '1994','1995','1996','1997','1998','1999', '2000', '2001','2002', '2003','2004', '2005', '2006','2007','2008','2009','2010','2011', '2012', '2013','2014', '2015','2016', '2017', '2018','2019','2020'],
            'message': 'Gracias por registrarte.',
        })

    def onchange_age(self, cr, uid, ids, fecha_operaciones2, context=None):
        #pdb.set_trace()
        if fecha_operaciones2 != False:
            return {
                'value':{
                    'amaterno': amaterno.title()
                    }
            }




class seguimiento(http.Controller):

    @http.route('/seguimiento/signup/', auth='public', website=True, methods=['GET'])
    def index(self, **kw):
        return http.request.render('company_ihce.forms_user', {            
            
        })

    @http.route('/seguimiento/signup/', auth='public', website=True, methods=['POST'])
    def a_log(self, **kw):
        print "INSIDE" + str(http.request.params)
        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']

        responseL = http.request.params
        responsel = str(responseL['user_l'])
        responseP = str(responseL['password_login'])


        usuarioActivo = Companies.search([('user_login','=',responsel), ('password_login','=',responseP)])

        var = len(usuarioActivo)
        if var == 1 :
            return http.request.render('company_ihce.forms', {
            'message': 'Gracias puedes continuar para agendar una asesoria',
            'id': usuarioActivo.id,
            'name': usuarioActivo.name,
            })
            
        else :
            return http.request.render('company_ihce.forms_user', {
            'message': 'Usuario no registrado, registrate para crear una aseosria',
            })     

    @http.route('/seguimiento/asesoria/', auth='public', website=True, methods=['POST'])
    def reg_ase(self, **kw):
        Asesorias = http.request.env['asesorias.ihce']
        #http.request.params.update({'name_commercial':nombre, 'rfc':nombre})
        com = Asesorias.create2(http.request.params)


        return http.request.render('company_ihce.forms_user',{
            'message': 'Gracias, tu asesoria esta registrada',
            })



class registro_acompanamiento(http.Controller): 

    @http.route('/1/registro_acompanamiento/', auth='public', website=True, methods=['GET'])
    def index(self, **kw): 
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        Municipio = http.request.env['town.hidalgo']
        municipio = Municipio.search([('name', '!=', '')])
        emprered = http.request.env['emprereds']
        emprereD = emprered.search([('name','!=','')])

        i = [] 
        for x in atentionareas:
            i.append(x.name) 
 
        

        ie = []
        for x in emprereD:
            ie.append(x.name)

       
        mun =[]
        for x in municipio:
            mun.append(x.name)

        

        return http.request.render('company_ihce.form_acompa', {            
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'areas': i,
            'empr': ie,
            'muni': mun,
        })

    @http.route('/1/registro_acompanamiento/', auth='public', website=True, methods=['POST'])
    def a_log(self, **kw):

        print "INSIDE" + str(http.request.params)
        uid = 72
        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']       


        
        #------------------------------Aqui va el listado de areas de atencion-------------#
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        i = []
        for x in atentionareas:
            i.append(x.name)
     
        responseL = http.request.params
        responseC = str(responseL['name_people'])
        responseO = str(responseL['apaterno']) 
        responseP = str(responseL['amaterno'])  
        responseA = str(responseL['user_login'])
        responseB = str(responseL['password_login'])
        responseD = str(responseL['name_comer'])
        responseE = str(responseL['product_server'])
        responseF = str(responseL['tramit_comer']) 
        responseH = str(responseL['muni'])
        responseG = str(responseL['tel'])
        responseI = str(responseL['RFC'])
        responseJ = str(responseL['email'])
        responseK = str(responseL['sexo'])
        responseM = str(responseL['areas']) 
        responseN = str(responseL['empr'])      

        usuarioActivo = Companies.search([('user_login','=',responseA)])
       


        nombre = str(responseL['name_people']) + " " + str(responseL['apaterno']) + " " + str(responseL['amaterno']) 


        types = str(responseL['types'])
        if types == "Emprendedor":
            types = "emprendedor"
        if types == "Persona Fisica":
            types = "fisica"
        if types == "Persona Moral":
            types = "moral"
        
        typesemp = str(responseL['empr'])
        #pdb.set_trace()
        if typesemp == "Emprered Tula":
            typesemp = 1
        if typesemp == "Emprered Tizayuca":
            typesemp = 2
        if typesemp == "Emprered Mixquiahuala":
            typesemp = 4
        if typesemp == "Emprered Huichapan":
            typesemp = 5
        if typesemp == "Emprered Apan":
            typesemp = 7
        if typesemp == "Emprered Huejutla":
            typesemp = 8
        if typesemp == "Emprered Ixmiquilpan":
            typesemp = 9
        if typesemp == "Emprered Pachuca":
            typesemp = 10
        if typesemp == "Emprered Zacualtipán":
            typesemp = 11
        if typesemp == "Emprered Tulancingo":
            typesemp = 13
        if typesemp == "Emprered Atotonilco":
            typesemp = 16
        if typesemp == "Emprered Otomí-tepehua":
            typesemp = 17
        if typesemp == "Emprered Molango":
            typesemp = 18
        if typesemp == "Emprered Metztitlán":
            typesemp = 19
        if typesemp == "Emprered Jacala":
            typesemp = 20
        if typesemp == "Emprered Zimapan":
            typesemp = 21
        if typesemp == "IHCE":
            typesemp = 22
        else:
            typesemp = 17




        #pdb.set_trace()
        types_areas = str(responseL['areas'])
        if types_areas == "Administrativo":
            types_areas = 1
        if types_areas == "Formación de Capital Humano":
            types_areas = 2
        if types_areas == "Agencia de Innovación Empresarial":
            types_areas = 3
        if types_areas == "Financiamiento":
            types_areas = 4
        if types_areas == "Fondo Emprendedor":
            types_areas = 5
        if types_areas == "Laboratorio de Diseño":
            types_areas = 6
        if types_areas == "Dirección General":
            types_areas = 7
        if types_areas == "Emprendimiento":
            types_areas = 8
        if types_areas == "Acompañamiento Empresarial":
            types_areas = 9

        
        types_muni  = str(responseL['muni'])
        if types_muni == "Acatlán":
            types_muni = 1
        if types_muni == "Acaxochitlán":
            types_muni = 2
        if types_muni == "Actopan":
            types_muni = 3
        if types_muni == "Agua Blanca de Iturbe":
            types_muni = 4
        if types_muni == "Ajacuba":
            types_muni = 5
        if types_muni == "Alfajayucan":
            types_muni = 6
        if types_muni == "Almoloya":
            types_muni = 7
        if types_muni == "Apan":
            types_muni = 8
        if types_muni == "El Arenal":
            types_muni = 9
        if types_muni == "Atitalaquia":
            types_muni = 10
        if types_muni == "Atlapexco":
            types_muni = 11
        if types_muni == "Atotonilco El Grande":
            types_muni = 12
        if types_muni == "Atotonilco de Tula":
            types_muni = 13
        if types_muni == "Calnali":
            types_muni = 14
        if types_muni == "Cardonal":
            types_muni = 15
        if types_muni == "Cuautepec":
            types_muni = 16
        if types_muni == "Chapantongo":
            types_muni = 17
        if types_muni == "Chapulhuacan":
            types_muni = 18
        if types_muni == "Chilcuahutla":
            types_muni = 19
        if types_muni == "Eloxochitlan":
            types_muni = 20
        if types_muni == "Emilio Zapata":
            types_muni = 21
        if types_muni == "Epazoyucan":
            types_muni = 22
        if types_muni == "Francisco I Madero":
            types_muni = 23
        if types_muni == "Huasca de Ocampo":
            types_muni = 24
        if types_muni == "Huautla":
            types_muni = 25
        if types_muni == "Huazalingo":
            types_muni = 26
        if types_muni == "Huehuetla":
            types_muni = 27
        if types_muni == "Huejutla de Reyes":
            types_muni = 28
        if types_muni == "Huichapan":
            types_muni = 29
        if types_muni == "Ixmiquilpan":
            types_muni = 30
        if types_muni == "Jacala de Ledezma":
            types_muni = 31
        if types_muni == "Jaltocán":
            types_muni = 32
        if types_muni == "Juárez Hidalgo":
            types_muni = 33
        if types_muni == "Lolotla":
            types_muni = 34
        if types_muni == "Metepec":
            types_muni = 35
        if types_muni == "San Agustin Metzquititlán":
            types_muni = 36
        if types_muni == "Metztitlán":
            types_muni = 37
        if types_muni == "Mineral del Chico":
            types_muni = 38
        if types_muni == "Mineral del Monte":
            types_muni = 39
        if types_muni == "La Misión":
            types_muni = 40
        if types_muni == "Mixquiahuala de Juárez":
            types_muni = 41
        if types_muni == "Molango de Escamilla":
            types_muni = 42
        if types_muni == "Nicolas Flores":
            types_muni = 43
        if types_muni == "Nopala de Villagrán ":
            types_muni = 44
        if types_muni == "Omitlán de Juárez":
            types_muni = 45
        if types_muni == "San Felipe Orizatlán":
            types_muni = 46
        if types_muni == "Pacula":
            types_muni = 47
        if types_muni == "Pachuca de Soto":
            types_muni = 48
        if types_muni == "Pisaflores":
            types_muni = 49
        if types_muni == "Progreso de Obregon":
            types_muni = 50
        if types_muni == "Mineral de la Reforma":
            types_muni = 51
        if types_muni == "San Agustín Tlaxiaca":
            types_muni = 52
        if types_muni == "San Bartolo Tutotepec":
            types_muni = 53
        if types_muni == "San Salvador":
            types_muni = 54
        if types_muni == "Santiago de Anaya":
            types_muni = 55
        if types_muni == "Santiago Tulantepec":
            types_muni = 56
        if types_muni == "Singuilucan":
            types_muni = 57
        if types_muni == "Tasquillo":
            types_muni = 58
        if types_muni == "Tecozautla":
            types_muni = 59
        if types_muni == "Tenango de Doria":
            types_muni = 60
        if types_muni == "Tepeapulco":
            types_muni = 61
        if types_muni == "Tepehuacan de Guerrero":
            types_muni = 62
        if types_muni == "Tepeji del Río":
            types_muni = 63
        if types_muni == "Tepetitlán":
            types_muni = 64
        if types_muni == "Tetepango":
            types_muni = 65
        if types_muni == "Tezontepec de Aldama":
            types_muni = 66
        if types_muni == "Tianguistengo":
            types_muni = 67
        if types_muni == "Tizayuca":
            types_muni = 68
        if types_muni == "Tlahuelilpan":
            types_muni = 69
        if types_muni == "Tlahuiltepa":
            types_muni = 70
        if types_muni == "Emiliano Zapata":
            types_muni = 71
        if types_muni == "Tlanchinol":
            types_muni = 72
        if types_muni == "Tlaxcoapan":
            types_muni = 73
        if types_muni == "Tolcayuca":
            types_muni = 74
        if types_muni == "Tula de Allende":
            types_muni = 75
        if types_muni == "Tulancingo de Bravo":
            types_muni = 76
        if types_muni == "Xochiatipan":
            types_muni = 77
        if types_muni == "Xochicoatlán":
            types_muni = 78
        if types_muni == "Yahualica":
            types_muni = 79
        if types_muni == "Zacualtipán":
            types_muni = 80
        if types_muni == "Zapotlán de Juárez":
            types_muni = 81
        if types_muni == "Zempoala":
            types_muni = 82
        if types_muni == "Zimapán":
            types_muni = 83

        i = [] 
        for x in atentionareas:
            i.append(x.name) 
 
        emprered = http.request.env['emprereds']
        emprereD = emprered.search([('name','!=','')])

        ie = []
        for x in emprereD:
            ie.append(x.name)


        Municipio = http.request.env['town.hidalgo']
        municipio = Municipio.search([('name', '!=', '')])

        mun =[]
        for x in municipio:
            mun.append(x.name)



        #pdb.set_trace()
        var = len(usuarioActivo)
        if var == 0 :
            http.request.params.update({'name':nombre, 'apaterno':responseO, 'amaterno':responseP, 'user_login':responseA, 'password_login':responseB, 'name_commercial':responseD, 'date': datetime.now(), 'Productos_Servicios':responseE, 'tramit':responseF, 'town_company':types_muni, 'cel_phone':responseG, 'rfc':responseI, 'email':responseJ, 'sexo':responseK, 'atention_area':types_areas, 'emprered':typesemp, 'type':types})
            com = Companies.create2(http.request.params)
            return http.request.render('company_ihce.form_acompa', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Gracias por registrarte.',
            'areas': i,
            'empr': ie,
            'muni': mun,
            })
            
        else :
            return http.request.render('company_ihce.form_acompa', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'No Registrado',
            'areas': i,
            'empr': ie,
            'muni': mun,
            })





