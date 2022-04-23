# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, tools,api,_,fields
from odoo.exceptions import UserError, Warning


class IrAttachment(models.Model):
    _name = 'hallakeen_data'
    _description = 'بيانات الحلاقين'

    name = fields.Char(string="اسم الحلاق")
    time_from = fields.Char(string="المواعيد من ")
    time_to = fields.Char(string="الى ")
    day_off = fields.Char(string="يوم الاجازه")
    shop_id = fields.Many2one('mobile_shop')


class IrAttachment(models.Model):
    _name = 'mobile_shop'
    _description = 'Shop'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char(string="Name",store=True,index=True,tracking=1,)
    x_activity = fields.Many2one('mail.activity.type',string="Activity",indexed=True,tracking=1,store=True)
    x_address= fields.Char(string="Address",indexed=True,tracking=1,store=True)
    x_assigned_to = fields.Many2one('res.partner',string="Assigned",indexed=True,tracking=1,store=True)
    x_chairs_number =fields.Integer(string="chairs number",indexed=True,tracking=1,store=True)
    x_contact_name = fields.Char(string="Contact Name",indexed=True,tracking=1,store=True)
    x_district = fields.Many2one('x_res.district',string="District",indexed=True,tracking=1,store=True)
    x_kids =  fields.Boolean(string="kids",indexed=True,tracking=1,store=True)
    x_mens = fields.Boolean(string="men",indexed=True,tracking=1,store=True)
    x_women = fields.Boolean(string="women", indexed=True, tracking=1, store=True)
    x_name = fields.Char(string="Name",indexed=True,tracking=1,store=True)
    x_paid = fields.Boolean(string="Paid", indexed=True, tracking=1, store=True)
    x_phone = fields.Char(string="Phone",indexed=True,tracking=1,store=True)
    x_region = fields.Many2one('x_res.region', string="Region", indexed=True, tracking=1, store=True)
    x_signed = fields.Boolean(string="Signed", indexed=True, tracking=1, store=True)
    x_signing_problem = fields.Text(string="Remarks or notes",indexed=True,tracking=1,store=True)
    x_street = fields.Many2one('x_street', string="Street", indexed=True, tracking=1, store=True)
    sign_date =fields.Date(string="Payment Date")
    sign_contract_date = fields.Date(string="Sign Contract Date")

    has_long=fields.Boolean(string="تم ادخال الموقع",store=True,compute="_has_long_compute")

    has_branches = fields.Boolean('Has Branches ? ',tracking=1)

    branches_ids = fields.One2many('mobile_shop','branch_id',tracking=1,)

    is_a_branch = fields.Boolean('Is A Branch',tracking=1,)
    branch_id = fields.Many2one('mobile_shop',string="Main Branch",tracking=1,)
    web_site = fields.Char("الموقع الالكتروني ",tracking=1,)
    hallaky_user_name = fields.Char("اسم مستخدم حلاقي ", tracking=1, )
    hallakeen_data = fields.One2many('hallakeen_data','shop_id',tracking=1,)

    time_from=fields.Char(string="مواعيد العمل من ",indexed=True,tracking=1,store=True)
    time_to = fields.Char(string="الى ", indexed=True, tracking=1, store=True)
    day_off= fields.Char("ايام الاجازه")
    long=fields.Float(string="خط الطول ", indexed=True, tracking=1, store=True, digits=(12,10))
    lat = fields.Float(string="خط العرض ", indexed=True, tracking=1, store=True, digits=(12,10))
    house_service = fields.Boolean(string="الخدمة المنزلية")



    def _has_long_compute(self):
        for i in self:
            if i.long > 0.00:
                i.has_long=True
            else:
                i.has_long=False

    def send_msg(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_mobile': self.x_phone},
                }

    @api.onchange('x_region')
    def change_region(self):
        bb = {}
        if self.name:
            bb = {'domain': {'x_district': [('x_region', '=', self.x_region.id)]}}
        else:
            self.x_region=""
        return bb

    @api.onchange('x_district')
    def change_district(self):
        b = {}
        if self.name:
            if self.x_region:
                b = {'domain': {'x_street': [('x_city', '=', self.x_district.id)]}}
            else:
                raise UserError('من فضلك اختر المحافظة اولا')
            return b

    @api.onchange('x_street')
    def change_street(self):
        if self.name:
            if not self.x_district:
                raise UserError('من فضلك اختر المدينة اولا')

    @api.onchange('x_assigned_to')
    def change_assigned_to(self):
        if self.name:
            if not self.env.user.has_group('base.group_system'):
                if not self.env.user.has_group('base.group_erp_manager'):
                    raise UserError('لا يمكنك تغيير جهة الاسناد')
        else:
            self.x_assigned_to = self.env.user.partner_id.id

#class Street(models.Model):
#    _name = 'street.street'
#    _inherit = ['mail.thread', 'mail.activity.mixin']

#    name= fields.Char('اسم الشارع او المنطقة',required=True)
#    city = fields.Many2one('res.district',string="المدينة او الحي",required=True)


#class District(models.Model):
#    _name = 'res.ditrict'
#    _inherit = ['mail.thread', 'mail.activity.mixin']

#    name = fields.Char('المدينة او الحي', required=True)
#    region = fields.Many2one('x_res.region',string="المحافظه", required=True)
