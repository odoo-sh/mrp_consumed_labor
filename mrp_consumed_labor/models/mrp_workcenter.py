# Copyright 2020-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import fields, models

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    labor_expense_account_id = fields.Many2one('account.account', string="Labor Expense Account")
