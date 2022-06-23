# Copyright 2020-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).
{
    'name': "Mrp Consumed Labor",

    'summary': """
             This module posts the Labor cost which is calculated from work center hourly rates to credit to WIP, from a labor expense account.""",

    'version': "15.0.1.0.0",
    'category': 'Manufacturing',
    'website': "http://sodexis.com/",
    'author': "Sodexis",
    'license': 'OPL-1',
    'installable': True,
    'depends': ['base', 'mrp', 'stock_account'],
    'data': [
        'views/mrp_workcenter_views.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'price': 49.95,
    'currency': 'USD',
}
