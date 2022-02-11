# -*- coding: utf-8 -*-
{
    'name': "emperor",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/wizards.xml',
        'views/views.xml',
        'views/king.xml',
        'views/ship.xml',
        'views/people.xml',
        'views/power_station.xml',
        'views/attack_tower.xml',
        'views/defense_dome.xml',
        'views/nursery.xml',
        'views/battle.xml',
        'views/kingdom.xml',
        'views/world.xml',
        'views/travel.xml',
        'views/premium.xml',
        'views/cron.xml',
        'views/action.xml',
        'views/menus.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
