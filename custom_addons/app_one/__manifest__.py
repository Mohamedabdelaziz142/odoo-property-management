{
    'name': 'First App',
    'version': '1.0.0',
    'summary': 'A short description of what your module does',
    'description': 'A longer description if needed.',
    'author': 'Mohamed',
    'website': 'https://example.com',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/property_style.css',
        ]
    },
    'installable': True,
    'application': True,
}
