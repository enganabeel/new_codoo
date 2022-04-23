from odoo import models, fields, api
from odoo.exceptions import Warning, UserError, ValidationError

class employee_contract(models.Model):
    _inherit = 'hr.contract'
    
    insurance_wage = fields.Float('الراتب التأميني')
    employee_percent = fields.Float('نسبة الراتب الموظف',default=11)
    company_percent = fields.Float('نسبة الشركة',default=10)
    employee_insurance_amount = fields.Float('الراتب التأميني الموظف',compute='_compute_amounts')
    company_insurance_amount = fields.Float('الراتب التأميني الشركة',compute='_compute_amounts')
    profit_tax_percent = fields.Float('ضريبة كسب العمل نسبة')
    profit_tax_amount = fields.Float('ضريبة كسب العمل قيمة',compute='_compute_amounts')
    trans_allowance = fields.Float('بدل انتقال')
    
    @api.depends('wage','profit_tax_percent','insurance_wage','employee_percent','company_percent')
    def _compute_amounts(self):
        for rec in self:
            rec.profit_tax_amount = rec.wage * (rec.profit_tax_percent / 100)
            rec.employee_insurance_amount = rec.insurance_wage * (rec.employee_percent / 100)
            rec.company_insurance_amount = rec.insurance_wage * (rec.company_percent / 100)

