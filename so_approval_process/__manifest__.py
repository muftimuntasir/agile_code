{
    'name': 'Approval Process of Sale Order',
    'version': '1.0',
    'category': '',
    'author': 'Rocky',
    'summary': 'Approval process with range declaration and sale order approval layer',
    'description': 'Approval process with range declaration and sale order approval layer',
    'depends': ['base', 'sale'],
    'data': [
        'security/so_approval_security.xml',
        'security/ir.model.access.csv',
        'views/so_approval_range_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
