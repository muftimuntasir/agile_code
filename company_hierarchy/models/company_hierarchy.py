from odoo import api, exceptions, fields, models, _
import datetime


class CompanyHierarchy(models.Model):
    _name = "company.hierarchy"
    _description = "Company Hierarchy"
    _order = 'id desc'

    name = fields.Char(string="Name")
    parent_hierarchy_id = fields.Many2one('parent.hierarchy', string="Parent") ## Depricated
    sub_company_id = fields.Many2one('company.hierarchy', string="Parent Company")
    monthly = fields.Boolean(string="Monthly")
    credit_limit = fields.Float(string="Credit Limit")
    report_date = fields.Date(string="Report Date")


    def save(self):

        partner_ids = self.env['res.partner'].search([('company_hierarchy_id', '=', self.id)])

        for partner in partner_ids:
            partner.active_credit_limit = True
            partner.warning_amount = self.credit_limit
            partner.blocking_amount = self.credit_limit


    def set_credit_limit(self):
        monthly_ids = self.env['company.hierarchy'].search([('monthly', '=', True)])
        fixed_date_ids = self.env['company.hierarchy'].search([('monthly', '!=', True)])
        from datetime import date,datetime
        today = date.today()
        d1 = today.strftime("%d")
        print("d1 =", d1)
        ## Monthly Code Check

        for itm in monthly_ids:
           if int(d1) == 1:
               now = datetime.now()
               dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

               if dt_string is not False:
                   self._cr.execute('update pos_order set is_credit=False where date_order<%s', (dt_string,))
                   self._cr.execute('update res_partner set custom_credit=0.00')
                   self._cr.commit()

       ## Fixed Date Code Check
        for itm in fixed_date_ids:
            dt_string = itm.report_date

            if dt_string is not False:
                self._cr.execute('update pos_order set is_credit=False where date_order<%s', (dt_string,))
                self._cr.execute('update res_partner set custom_credit=0.00')
                self._cr.commit()








        return True



