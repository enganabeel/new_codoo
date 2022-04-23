from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, UserError, ValidationError
 
class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    def send_user_leads_amount(self,user_id,date_from,date_to,contract):
        leads_amount = self.env['crm.lead'].search_count([('user_id','=',user_id),('create_date','>',date_from),('create_date','<',date_to)])
        contract.leads_amount = leads_amount
    
    