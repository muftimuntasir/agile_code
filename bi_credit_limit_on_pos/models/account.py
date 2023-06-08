# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _ , tools
import psycopg2
from odoo.tools import float_is_zero
import logging
_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
	_inherit = "account.journal"

	is_credit = fields.Boolean(string="Is Credit Journal")



class PosPaymentMethod(models.Model):
	_inherit = 'pos.payment.method'

	is_credit = fields.Boolean(string='Is Credit Journal', related='journal_id.is_credit', readonly=False)


class ResUsersInherit(models.Model):
	_inherit = 'res.partner'

	active_credit_limit = fields.Boolean(string="Allow Credit")
	warning_amount = fields.Integer(string="Set Amount to Raise Warning")
	blocking_amount = fields.Integer(string="Set Amount to Block Credit Order")
	pos_order_ids = fields.One2many('pos.order', 'partner_id', readonly=True)
	custom_credit = fields.Float('Credit',compute="_compute_pos_credit",store=True)
	available_credit = fields.Float('Available Credit',compute="_compute_pos_credit",store=True)


	@api.depends('pos_order_ids','pos_order_ids.state','pos_order_ids.amount_paid')
	def _compute_pos_credit(self):
		for rec in self:
			pos_credit = sum((odr.credit_amount if odr.is_credit == True else 0.00) for odr in rec.pos_order_ids)

			rec.custom_credit = pos_credit
			rec.available_credit = rec.blocking_amount - pos_credit


	def action_view_credit_detail(self):
		self.ensure_one()
		return {
			'name': 'POS Credit Orders',
			'type': 'ir.actions.act_window',
			'view_mode': 'tree,form',
			'res_model': 'pos.order',
			'domain': [('id', 'in', self.pos_order_ids.ids),('is_credit','=',True)],
		}


class PosPaymentInherit(models.Model):
	_inherit = 'pos.payment'

	session_id = fields.Many2one('pos.session', string='Session', related='', store=True, index=True)

	@api.model
	def create(self, vals):


		if vals.get('pos_order_id',False):
			pos_order = self.env['pos.order'].sudo().browse(vals.get('pos_order_id'))
			if pos_order : 
				vals['session_id'] = pos_order.session_id.id
		return super(PosPaymentInherit, self).create(vals)



class POSOrderLoad(models.Model):
	_inherit = 'pos.session'

	def _loader_params_pos_payment_method(self):
		result = super()._loader_params_pos_payment_method()
		result['search_params']['fields'].extend(['is_credit'])
		return result

	def _loader_params_res_partner(self):
		result = super()._loader_params_res_partner()
		result['search_params']['fields'].extend(['active_credit_limit','warning_amount','blocking_amount','custom_credit','available_credit'])
		return result


class POSOrder(models.Model):
	_inherit="pos.order"

	is_partial = fields.Boolean('Is Partial Payment')
	amount_due = fields.Float("Amount Due", compute="get_amount_due")
	is_picking_created = fields.Boolean('Picking Created')
	is_credit = fields.Boolean(string='Is Credit', default=False)
	credit_amount = fields.Float(string=' Credit Amount')

	@api.model
	def _process_order(self, order, draft, existing_order):
		"""Create or update an pos.order from a given dictionary.

		:param dict order: dictionary representing the order.
		:param bool draft: Indicate that the pos_order is not validated yet.
		:param existing_order: order to be updated or False.
		:type existing_order: pos.order.
		:returns: id of created/updated pos.order
		:rtype: int
		"""
		order = order['data']
		
		pos_session = self.env['pos.session'].browse(order['pos_session_id'])
		if pos_session.state == 'closing_control' or pos_session.state == 'closed':
			order['pos_session_id'] = self._get_valid_session(order).id

		pos_order = False
		
		if not existing_order:
			pos_order = self.create(self._order_fields(order))
		else:
			pos_order = existing_order
			pos_order.lines.unlink()
			order['user_id'] = pos_order.user_id.id
			pos_order.write(self._order_fields(order))

		pos_order = pos_order.with_company(pos_order.company_id)
		self = self.with_company(pos_order.company_id)
		self._process_payment_lines(order, pos_order, pos_session, draft)

		try:
			pos_order.action_pos_order_paid()
		except psycopg2.DatabaseError:
			# do not hide transactional errors, the order(s) won't be saved!
			raise
		except Exception as e:
			_logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

		if pos_order.is_partial == False :
			pos_order._create_order_picking()
		if order.get('to_invoice') and pos_order.state == 'paid':
			pos_order.action_pos_order_invoice()

		return pos_order.id


	@api.depends('amount_total', 'amount_paid')
	def get_amount_due(self):
		for order in self:
			if order.amount_paid - order.amount_total >= 0:
				order.amount_due = 0
				order.is_partial = False
			else:
				order.amount_due = order.amount_total - order.amount_paid

	def write(self, vals):
		for order in self:
			if order.name == '/' and order.is_partial:
				vals['name'] = order.config_id.sequence_id._next()
		return super(POSOrder, self).write(vals)

	def _is_pos_order_paid(self):
		return float_is_zero(self._get_rounded_amount(self.amount_total) - self.amount_paid,
							 precision_rounding=self.currency_id.rounding)

	def action_pos_order_paid(self):
		self.ensure_one()
		if not self.is_partial:
			return super(POSOrder, self).action_pos_order_paid()
		if self.is_partial:
			if self._is_pos_order_paid():
				self.write({'state': 'paid'})
				if len(self.picking_ids) > 0:
					return True
				else:
					return self._create_order_picking()
			else:
				if not self.picking_ids:
					return self._create_order_picking()
				else:
					return False

	def add_payment(self, data):
		"""Create a new payment for the order"""
		self.ensure_one()
		pymt_method = self.env['pos.payment.method'].sudo().browse(data.get('payment_method_id',False))
		if pymt_method and pymt_method.is_credit :

			self.write({
				'is_credit' : True,
				'credit_amount' :data.get('amount')
			})



		# else:

		self.env['pos.payment'].create(data)
		self.amount_paid = sum(self.payment_ids.mapped('amount'))

	def _create_order_picking(self):
		self.ensure_one()
		if self.is_partial == False or (self.is_partial and len(self.picking_ids) < 1):
			if not self.session_id.update_stock_at_closing or (self.company_id.anglo_saxon_accounting and self.to_invoice):
				picking_type = self.config_id.picking_type_id
				if self.partner_id.property_stock_customer:
					destination_id = self.partner_id.property_stock_customer.id
				elif not picking_type or not picking_type.default_location_dest_id:
					destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
				else:
					destination_id = picking_type.default_location_dest_id.id == False or self.is_partial and self.picking_ids

				pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(destination_id, self.lines, picking_type, self.partner_id)
				pickings.write({'pos_session_id': self.session_id.id, 'pos_order_id': self.id, 'origin': self.name})


	class CashFlow(models.Model):
		_inherit = 'account.account'

		@api.constrains('account_type')
		def _check_account_is_bank_journal_bank_account(self):
			self.env['account.account'].flush_model(['account_type'])
			self.env['account.journal'].flush_model(['type', 'default_account_id'])
			self._cr.execute('''
					SELECT journal.id
					  FROM account_journal journal
					  JOIN account_account account ON journal.default_account_id = account.id
					 WHERE account.account_type IN ('asset_receivable', 'liability_payable')
					   AND account.id IN %s
					 LIMIT 1;
				''', [tuple(self.ids)])

			# if self._cr.fetchone():
			# 	raise ValidationError(
			# 		_("You cannot change the type of an account set as Bank Account on a journal to Receivable or Payable."))
			#
			#

