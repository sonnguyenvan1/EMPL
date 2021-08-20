{
    'name': "DCL-2",
    'version': '1.0',
    'depends': ['mail'],
    'author': "Author Name",
    'sequence': -10,
    'category': 'DCL',
    'description': """
    Description text
    """,

    'data': [
    'sercurity/ir.model.access.csv',
    'sercurity/sercurity.xml',

    'views/menu.xml',
    'views/nv_view.xml',
    'views/contracts_view.xml',

    'wizard/creat_form_reject.xml'
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
