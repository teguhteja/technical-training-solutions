# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': 'Module for real estate advertisements',

    'description': """
Long description of module's purpose
    """,

    'author': "IB Teguh Teja M",
    'website': "https://teguhteja.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Real Estate',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/estate_report_views.xml',
        'report/estate_reports.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users.xml'
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

