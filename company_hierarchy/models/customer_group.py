from odoo import api, exceptions, fields, models, _
import datetime

class CustomerGroup(models.Model):
    _name = "customer.group"
    _description = "Customer Group"
    _order = 'id desc'

    name = fields.Char(string="Name")