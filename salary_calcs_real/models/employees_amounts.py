# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning,ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    employee_id = fields.Many2one('hr.employee')
    visit_date = fields.Date()

class CrmEmployeesAmounts(models.Model):
    _name = 'crm.employees.amounts'
    name = fields.Char(compute='_set_name')
    contract_id = fields.Many2one('hr.contract',string='Employee Contract',required=True,domain=[('state','=','open')])
    leads_amount = fields.Float()
    invoicing_amount = fields.Float()
    notes = fields.Text()

    date_from = fields.Date()
    date_to = fields.Date()
    @api.onchange('date_from','date_to')
    def _check_only_month(self):
        print(self.date_from)
        print(self.date_to)
        if self.date_from and self.date_to:
            if self.date_from.month != self.date_to.month or self.date_from.year != self.date_to.year:
                raise ValidationError(_("Please choose the same month"))

    @api.onchange('contract_id','date_from','date_to')
    def calc_leads_amount(self):
        if self.contract_id and self.date_from and self.date_to:
            leads = self.env['crm.lead'].search_count([('employee_id','=',self.contract_id.employee_id.id),('visit_date','>=',self.date_from),('visit_date','<=',self.date_to)])
            self.leads_amount = leads
    @api.constrains('contract_id')
    def survey_id_constrains(self):
        if self.contract_id:
            same_contract_count = self.env['crm.employees.amounts'].search_count([('contract_id','=',self.contract_id.id)])
            if same_contract_count > 1:
                raise ValidationError(_('Contract must be unique'))


    @api.depends('contract_id')
    def _set_name(self):
        for rec in self:
            if rec.contract_id:
                rec.name = rec.contract_id.employee_id.name + "'s amounts"
            else:
                rec.name = ''


    @api.model
    def create(self,vals):
        res = super(CrmEmployeesAmounts,self).create(vals)
        res.contract_id.write({
                'amounts_id':res.id
        })
        return res

    def write(self,vals):
        res = super(CrmEmployeesAmounts,self).write(vals)
        contract_id = vals.get('contract_id',False)
        if contract_id:
            contract = self.env['hr.contract'].search([('id','=',contract_id)])
            contract.amounts_id = self.id
    def clear_amounts(self):
        for rec in self:
            rec.leads_amount = 0
            rec.invoicing_amount = 0
