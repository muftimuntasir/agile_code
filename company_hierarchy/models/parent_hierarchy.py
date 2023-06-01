from odoo import api, exceptions, fields, models, _
import datetime


class ParentHierarchy(models.Model):
    _name = "parent.hierarchy"
    _description = "Parent Hierarchy"
    _order = 'id desc'

    name = fields.Char(string="Name")
    report_date = fields.Date(string="Report Date")


