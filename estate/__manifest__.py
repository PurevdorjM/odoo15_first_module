# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'estate',
    'version': '1.0',
    'category': '',
    'sequence': 15,
    'license': "LGPL-3",
    'summary': 'Track leads and close opportunities',
    'description': "Ти Ти Жи Ви Си Өү ХХК-ны ХАБЭАБО-ны хэлтсийн модуль",
    'website': 'https://www.ttjvco.mn',
    'depends': [
        'base',
    ],
    'data': [
        "./views/user_line_views.xml",
        "./views/estate_property_views.xml",
        "./views/estate_property_offer.xml",
        "./views/estate_property_type_views.xml",
        "./views/estate_property_tag_views.xml",
        "./views/estate_menus.xml",
        "./security/ir.model.access.csv"
    ],
    'demo': [

    ],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
