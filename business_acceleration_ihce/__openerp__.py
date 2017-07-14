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
    "name": "Aceleración Empresarial IHCE",
    "version": "1.0",
    "depends": ["base",'courses_ihce'],
    "author": "Grupo Altegra",
    "category": "Custom Modules",
    "description": "Área de aceleración empresarial, crea proyectos para las empresas",
    "data" :[
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/percent_ihce_view.xml',
        'views/date_course_view_inh.xml',
        'views/acceleration_company_view.xml',
        'views/acceleration_view.xml',
        'views/company_view.xml',
        'demo/percent_demo_ae.xml',
        ],
    "demo" : [
        #~ 'demo/percent_demo_ae.xml',
    ],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': False,
}
