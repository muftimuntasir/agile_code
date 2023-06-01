from odoo import api, exceptions, fields, models, _
import datetime


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_hierarchy_id = fields.Many2one('company.hierarchy', string='Company Hierarchy')
    customer_group_id = fields.Many2one('customer.group', string='Customer Group')
    nid = fields.Char(string="Customer NID")
    birth_certificate  = fields.Char(string="Customer Birth Certificate No")

    @api.onchange('company_hierarchy_id')
    def _onchange_company_hierarchy_id(self):
        if self.company_hierarchy_id:
            self.active_credit_limit = True
            self.warning_amount = self.company_hierarchy_id.credit_limit
            self.blocking_amount = self.company_hierarchy_id.credit_limit
        else:
            self.active_credit_limit = False
            self.warning_amount = 0.0
            self.blocking_amount = 0.0


