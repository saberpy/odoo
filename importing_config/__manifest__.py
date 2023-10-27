# -*- coding: utf-8 -*-
{
    'name': "Max Importing Configuration",

    'summary': """
       Max Importing Configuration in Odoo V14 Community""",

    'description': """
        By This module we can customize max importing in setting.
        Features:
        1-add dynamic max importing setting .
        
        ** compatible with odoo version 14.0-20220131 community **

    """,

    'author': "Saber Zakariaee",

    'website': "mailto:saberzakariaee@gmail.com",

    'category': 'web',

    'odoo_version': '14.0-20220131',

    'version': '0.1',

    'depends': ['base','base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
    ],
    'qweb': [
    ],
    'sequence': 0,
    'application': True,
    'installable': True,
    'auto_install': False,
}
