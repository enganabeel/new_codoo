# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'hallaky',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'description': """
Base module for SAF-T reporting
===============================
This is meant to be used with localization specific modules.
    """,
    'license': 'OEEL-1',
    'depends':['web','base','mail'],
    'data':[
        'views/views.xml'
    ],
}
