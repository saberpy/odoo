# -*- coding: utf-8 -*-
{
    'name': "cardex_inventory",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sazcom",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_cardex_view.xml',
        'views/stock_move_views.xml',
        'views/stock_move_views_reload.xml',
        'views/stock_picking_type_view.xml',
        # 'views/templates.xml'
    ],
    'demo':[],
    'qweb':['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': True,
}
