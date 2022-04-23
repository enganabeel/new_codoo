from odoo import models, fields, api
from odoo.exceptions import Warning, UserError, ValidationError

class employee_contract(models.Model):
    _inherit = 'crm.team'
    
    leads_target = fields.Float('Leads Target')
 