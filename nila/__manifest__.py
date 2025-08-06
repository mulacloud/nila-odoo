# -*- coding: utf-8 -*-
{
    'name': "Nila Cloud Manager",

    'summary': "Nila odoo adaptor",
    
    'description' : "Nila odoo adaptor",


    'author': "Mula Cloud Project",
    'website': "https://mula.cloud",

    'category': 'Cloud',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/agent.xml',
        'views/hoster.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

