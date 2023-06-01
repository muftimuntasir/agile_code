from odoo import api, exceptions, fields, models, _
import datetime


class CompanyHierarchy(models.Model):
    _name = "company.hierarchy"
    _description = "Company Hierarchy"
    _order = 'id desc'

    name = fields.Char(string="Name")
    parent_hierarchy_id = fields.Many2one('parent.hierarchy', string="Parent")
    monthly = fields.Boolean(string="Monthly")
    credit_limit = fields.Float(string="Credit Limit")
    report_date = fields.Date(string="Report Date")


    def save(self):

        partner_ids = self.env['res.partner'].search([('company_hierarchy_id', '=', self.id)])

        for partner in partner_ids:
            partner.active_credit_limit = True
            partner.warning_amount = self.credit_limit
            partner.blocking_amount = self.credit_limit



