{
    'name': "DCL",
    'version': '1.0',
    'depends': ['mail','hr_contract'],
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

    'data/mail_template.xml'
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
