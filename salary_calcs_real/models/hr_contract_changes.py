from odoo import models, fields, api,_
from odoo.exceptions import Warning, UserError, ValidationError
 
class employee_contract(models.Model):
    _inherit = 'hr.contract'
    changebale_salary = fields.Monetary('Changeable Salary', tracking=True, help="Employee's monthly changeable Salary.",default=0)
    actual_changebale_salary = fields.Monetary('Actual Changeable Salary',tracking=True,readonly=True,compute='_set_actual_changebale_salary')
    sales_changebale_salary = fields.Monetary('Changeable Salary', tracking=True, help="Employee's monthly changeable Salary.",default=0)
    sales_actual_changebale_salary = fields.Monetary('Actual Changeable Salary',tracking=True,readonly=True,compute='_compute_wage')
    actual_wage = fields.Monetary('Actual Wage', tracking=True,default=0,readonly=True,compute='_compute_wage')
    leads_amount = fields.Float(related='amounts_id.leads_amount')
    invoicing_amount = fields.Float(related='amounts_id.invoicing_amount')
    leads_target = fields.Float('Leads Target')
    invoicing_target = fields.Float('Invoicing Target')
    employee_type = fields.Selection([('sales','Sales'),('other','Other')],required=True)
    total_salary = fields.Float(compute='_compute_total_salary')
    
    amounts_id = fields.Many2one('crm.employees.amounts')
    survey_percentage = fields.Float()
    
                
    @api.depends('actual_changebale_salary','wage')
    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = self.actual_changebale_salary + self.wage
    
    def set_actual_changebale_salary(self,perc):
        self.actual_changebale_salary = self.changebale_salary * perc
        
    @api.depends('changebale_salary','survey_percentage')
    def _set_actual_changebale_salary(self):
        for contract in self:
            perc = contract.survey_percentage / 100
            contract.set_actual_changebale_salary(perc)
        
            
            
    def get_actual_wage_from_target(self,target,amount,dependant_wage):
        if target == 0:
            return dependant_wage 
        else:
            percent_from_target = amount / target
            return percent_from_target * dependant_wage
        
    
    def set_sales_actual_changebale_salary(self):
        self.sales_actual_changebale_salary = self.get_actual_wage_from_target(self.invoicing_target,self.invoicing_amount,self.sales_changebale_salary)
        
    def set_actual_wage(self):
        self.actual_wage = self.get_actual_wage_from_target(self.leads_target,self.leads_amount,self.wage)
    
    @api.depends('invoicing_amount','leads_amount','leads_target','invoicing_target','wage','sales_changebale_salary')
    def _compute_wage(self):
        for contract in self:
            contract.set_sales_actual_changebale_salary()
            contract.set_actual_wage()
        
            

    