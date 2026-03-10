{
    'name': 'First App',
    'version': '1.0.0',
    'summary': 'A short description of what your module does',
    'description': 'A longer description if needed.',
    'author': 'Mohamed',
    'website': 'https://example.com',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': [
              'base', 
                'sale_management',    # Adds Sales features
                'account', # Adds Invoicing/Accounting features
                'mail',    # Adds Messaging features
                'contacts', # Adds Contact Management features
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/property_style.css',
        ]
    },
    'installable': True,
    'application': True,
}
