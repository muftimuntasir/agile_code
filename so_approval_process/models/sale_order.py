from odoo import api, exceptions, fields, models, _
import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_type = fields.Selection(selection=[
        ('cash', 'Cash'),
        ('credit', 'Credit')
    ], string="Payment Type")

    state = fields.Selection(selection_add=[('cfo', 'CFO'), ('ceo', 'CEO')])

    def confirm_action_with_approval(self):

        range_value = self.env['so.approval.range'].search([])
        so_amount = self.amount_total
        if self.payment_type == 'cash':
            range_cfo_cash = range_value.cfo_cash_limit_from <= so_amount <= range_value.cfo_cash_limit_to
            range_ceo_cash = range_value.ceo_cash_limit_from <= so_amount <= range_value.ceo_cash_limit_to
            if range_cfo_cash == True and self.state == 'draft':
                self.write({
                    'state': 'cfo',
                })
            elif range_ceo_cash == True and self.state == 'cfo':
                self.write({
                    'state': 'ceo',
                })

            else:
                self.action_confirm()

        else:
            range_cfo_credit = range_value.cfo_credit_limit_from <= so_amount <= range_value.cfo_credit_limit_to
            range_ceo_credit = range_value.ceo_credit_limit_from <= so_amount <= range_value.ceo_credit_limit_to

            if range_cfo_credit == True and self.state == 'draft':
                self.write({
                    'state': 'cfo',
                })
            elif range_ceo_credit == True and self.state == 'cfo':
                self.write({
                    'state': 'ceo',
                })

            else:
                self.action_confirm()

        # rv = range_cfo_cash or range_cfo_credit or range_ceo_cash or range_ceo_credit

        # import pdb;pdb.set_trace()











        # if self.state == 'cfo':
        #
        #     if self.payment_type == 'cash' and range_cfo_cash:
        #         self.action_confirm()
        #     else:
        #         if range_value.ceo:
        #             self.write({
        #                 'state': 'ceo',
        #             })
        #
        #     if self.payment_type == 'credit' and range_cfo_credit:
        #         self.action_confirm()
        #     else:
        #         if range_value.ceo:
        #             self.write({
        #                 'state': 'ceo',
        #             })
        #
        # if self.state == 'ceo':
        #
        #     if self.payment_type == 'cash' and range_ceo_cash:
        #         self.action_confirm()
        #     else:
        #         self.action_confirm()

            if self.payment_type == 'credit' and range_ceo_credit:
                self.action_confirm()
            else:
                self.action_confirm()






