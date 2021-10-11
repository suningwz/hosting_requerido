# -*- coding: utf-8 -*-

{
    'name': 'SE Repository Management',
    'summary': 'Manage Repositories.',
    'version': '13.0.1.0.0',
    'category': 'Extra Tools',
    'website': "https://softwareescarlata.com/",
    'author': 'David Montero Crespo',
    'installable': True,
    'external_dependencies': {
        
       
    },
    'depends': [
        'base','mail'
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/repository_repository_view.xml',
        'views/panel_tool.xml',
        'views/ir_module_module.xml'
    ],
    'application': True,
    'price': 40,
    "uninstall_hook": "uninstall_hook",
    'images': ['static/description/imagen.png'],
    'currency': 'EUR',
    'license': 'AGPL-3',

}
