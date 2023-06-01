{
    'name': 'Company Hierarchy',
    'version': '1.0',
    'category': '',
    'author': 'Rocky',
    'summary': 'Company hierarchy process for credit limit',
    'description': 'Company hierarchy process for credit limit',
    'depends': ['base'],
    'data': [
        'security/company_hierarchy_security.xml',
        'security/ir.model.access.csv',
        'views/customer_group_view.xml',
        'views/res_partner_view.xml',
        'views/company_hierarchy_view.xml',
        'views/parent_hierarchy_view.xml',


    ],
    'installable': True,
    'auto_install': False,
}
