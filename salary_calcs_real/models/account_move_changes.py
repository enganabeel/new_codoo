from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, UserError, ValidationError

class AccountMove(models.Model): 
    _inherit = 'account.move'
         
    def get_tax_amount(self):
        all_taxes = self.amount_by_group
        return sum([tax[1] for tax in all_taxes])
    def send_invoicing_amount_to_contract(self,user_id,date_from,date_to,contract):
        self.ensure_one()
        for rec in self:
            all_invoices = self.env['account.move'].search(['&',('invoice_user_id','=',user_id),('create_date','>',date_from),'&',('create_date','<',date_to),('type_name','=','Invoice')])
            invoices_amount = 0
            for invoice in all_invoices:
                if invoice.type_name == 'Invoice':
                    amount_due_without_taxes = abs(invoice.amount_residual - invoice.get_tax_amount())
                    payed_amount_with_tax  = invoice.amount_total - invoice.amount_residual - invoice.get_tax_amount()
                    payed_amount_without_tax = invoice.amount_total - invoice.amount_residual 
                    payed_amount = payed_amount_without_tax if payed_amount_without_tax < invoice.get_tax_amount() else payed_amount_with_tax
                    invoices_amount += payed_amount
            contract.invoicing_amount = invoices_amount
            return invoices_amount
