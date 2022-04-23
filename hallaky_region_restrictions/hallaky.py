# -*- coding: utf-8 -*-

# from openerp import models, fields, api, _
# from openerp.exceptions import Warning
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    regions_list = fields.Char()

class ResUsers(models.Model):
    _inherit = 'res.users'
    warehouse_ids = fields.Many2many('x_res.region', string='Allowed Regions')
    regions_list = fields.Char()

    def vvvv(self):
        dict = []
        for region in self.warehouse_ids:
            dict.append(region.id)
        self.write({'regions_list':str(dict)})
        self.partner_id.write({'x_regions_list':str(dict)})


   # def _compute_dict_region(self):
   #     dict = []
   #
   #     for rec in self:
   #         if rec.warehouse_ids:
   #             for region in rec.warehouse_ids:
   #                 dict.append(region.id)
   #         rec.regions_list = str(dict)


    
class ResUsersPockings(models.Model):
    _inherit = 'mobile_shop'
    domain=fields.Char(compute="_compute_total_reception_one2many")

    #@api.model
    def _compute_total_reception_one2many(self):
        dict = []
        #raise UserError('انا هنا مةوجود')
        #raise UserError('انا هنا مةوجود')
        if self.env.user.warehouse_ids:
            for region in self.env.user.warehouse_ids:
                dict.append(region.id)

        for rec in self:
            rec.domain="cc"
                #return {'domain': {'x_region': [('id', 'in', dict)]}}


    @api.onchange('x_phone')
    def item_delivered_id_onchange(self):
        dict = []
      #  if self.x_region:
        if self.env.user.warehouse_ids:
            for region in self.env.user.warehouse_ids:
                dict.append(region.id)
#         if self.x_region not in dict:
#            raise UserError('عذرا غير مسموح لك باستعراض البيانات')

        return {'domain': {'x_region': [('id', 'in', dict)]}}

    @api.model
    def create(self,vals):
        dict = []
        if self.env.user.warehouse_ids:
            for region in self.env.user.warehouse_ids:
                dict.append(region.id)

        if vals["x_region"] not in dict:
            raise UserError("عفوا غير مسموح بادخال بيانات تخص تلك المحافظه")
            return False

        result = super(ResUsersPockings, self).create(vals)
        return result