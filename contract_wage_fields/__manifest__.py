# -*- coding: utf-8 -*-
{
    'name': "Contract Wage Fields",

    'summary': """module to automatically create overtime and allowancees""",

    'description': """""",

    'author': "Hatem mostafa",
    'website': "https://www.linkedin.com/in/hatem-mostafa-a6267b1a9",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract'],

    # always loaded
    'data': [
        'views/contract.xml',
    ],
}
