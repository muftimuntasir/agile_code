# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Point of Sale Credit Limit/Credit Limit on POS",
    "version": "16.0.1.1",
    "category": "Point of Sale",
    'summary': 'POS customer credit limit on point of sale customer credit limit on pos credit limit pos credit amount customer credit on pos customer credit payment pos partial credit pos payment with credit pos partial payment allow customer credit on pos payment limit',
    "description": """

        POS Credit Limit in odoo,
        Allow Credit Li mit in odoo,
        Set Amount to Raise Warning in odoo,
        Set Amount to Block Credit Order in odoo,
        Warning if Credit Exceeding Warning Limit in odoo,
        Warning if Credit Exceeding Blocking Limit in odoo,
        Credit for the Customers in odoo,
        Warning or Validation Message in odoo,

    """,
    "author": "BrowseInfo",
    "price": 20,
    "currency": 'EUR',
    "website": "https://www.browseinfo.in",
    "depends": ['base', 'point_of_sale'],
    "data": [
        'views/account_journal.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'bi_credit_limit_on_pos/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
            'bi_credit_limit_on_pos/static/src/js/Screens/ClientScreen/ClientListScreen.js',
            'bi_credit_limit_on_pos/static/src/js/Popups/BiWarningPopup.js',
            'bi_credit_limit_on_pos/static/src/js/Popups/BiWarningBlockingPopup.js',
            'bi_credit_limit_on_pos/static/src/xml/pos.xml',
        ],
    },
    'license': 'OPL-1',
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/XV-32Byyffs',
    "images":["static/description/Banner.gif"],
}
