# -*- coding: utf-8 -*-
{
    'name': "Salary Calculations Real",
 
    'summary': """
        Short (1 phrase/line) summary of the module's sss purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PerfectTeck/hatem",
    'website': "https://www.linkedin.com/in/hatem-mostafa-a6267b1a9",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','hr_payroll'],

    # always loaded
    'data': [
        'views/hr_contract_changes.xml',
        'views/crm_teams_changes.xml',
        'views/crm_employees_amounts.xml',
        'views/crm_employee_evaluation.xml',
        'security/ir.model.access.csv',
    ],
}
