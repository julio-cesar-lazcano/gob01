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
############################################################################ 

{
    "name": "Informes IHCE",
    "version": "1.0",
    "depends": ["base",'business_development_ihce','entrepreneurship_ihce'],
    "author": "Grupo Altegra",
    "category": "Custom Modules",
    "description": "Informes IHCE",
    "data" :[
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/reports_view.xml',
        'views/emprendimiento_view.xml',
        'views/platicas_cursos_view.xml',
        'views/asesoria_pymes_view.xml',
        'views/servicio_pymes_view.xml',
        'views/cursos_view.xml',
        'views/consultorias_view.xml',
        'views/emprendimiento_emprered_view.xml',
        'views/asesoria_emprered_view.xml',
        'views/servicios_emprered_view.xml',
        'views/cursos_emprered_view.xml',
        'views/consultorias_emprered_view.xml',
        'views/emprered_view.xml',
        'views/ihce_view.xml',
        'views/indicadores_emprered_view.xml',
        'views/meta_anual_view.xml',
        'views/report_laboratory.xml',
        'views/report_services_laboratory.xml',
        'views/indicadores_ihce_view.xml',
        'views/reporte_ejecutivo_view.xml',
        'views/cursos_ihce_ejecutivo_view.xml',
        'views/emprered_ejecutivo_view.xml',
        'views/metas_ejecutivo_view.xml',
        'views/reporte_regiones.xml',
        'demo/apan_demo.xml',
        'demo/atotonilco_demo.xml',
        'demo/huejutla_demo.xml',
        'demo/huichapan_demo.xml',
        'demo/ixmiquilpan_demo.xml',
        'demo/otomi_demo.xml',
        'demo/mixquiahuala_demo.xml',
        'demo/pachuca_demo.xml',
        'demo/tizayuca_demo.xml',
        'demo/tula_demo.xml',
        'demo/tulancingo_demo.xml',
        'demo/zacualtipan_demo.xml',
        'demo/molango_demo.xml',
        'demo/metztitlan_demo.xml',
        'demo/jacala_demo.xml',
        'demo/total_demo.xml',
        'demo/aceleracion_demo.xml',
        'demo/emprendimiento_demo.xml',
        'demo/formacion_demo.xml',
        'demo/servicios_empresariales_demo.xml',
        ],
    'demo': [
    ],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': False,
}
