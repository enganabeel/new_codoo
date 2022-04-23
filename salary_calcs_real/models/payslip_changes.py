from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, UserError, ValidationError
 
class PaySlip(models.Model):
    _inherit = 'hr.payslip'
        
    
    def action_payslip_done(self):
        res = super(PaySlip, self).action_payslip_done()
        employee_amounts = self.env['crm.employees.amounts'].search([('contract_id','=',self.contract_id.id)])
        employee_evaluation = self.env['hr.employee.evaluation'].search([('contract_id','=',self.contract_id.id)])
        if len(employee_amounts) > 0 :
            employee_amounts.clear_amounts()
        if len(employee_evaluation) > 0 :
            employee_evaluation.clear_marks()
            employee_evaluation._compute_perc() # work around to set contract's percentage
        return res
        