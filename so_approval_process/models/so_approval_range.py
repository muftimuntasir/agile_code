from odoo import api, exceptions, fields, models, _
import datetime


class SOApprovalRange(models.Model):
    _name = "so.approval.range"
    _order = 'id desc'

    name = fields.Char(string="Approval Range for")
    active = fields.Boolean(string="Active", default=True)

    cfo = fields.Boolean(string="CFO")
    cfo_cash_limit_from = fields.Integer(string="Cash Limit From")
    cfo_cash_limit_to = fields.Integer(string="Cash Limit To")
    cfo_credit_limit_from = fields.Integer(string="Credit Limit From")
    cfo_credit_limit_to = fields.Integer(string="Credit Limit To")

    ceo = fields.Boolean(string="CEO")
    ceo_cash_limit_from = fields.Integer(string="Cash Limit From")
    ceo_cash_limit_to = fields.Integer(string="Cash Limit To")
    ceo_credit_limit_from = fields.Integer(string="Credit Limit From")
    ceo_credit_limit_to = fields.Integer(string="Credit Limit To")

    # def save(self):
    #     return True



