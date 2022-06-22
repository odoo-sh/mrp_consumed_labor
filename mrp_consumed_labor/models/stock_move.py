# Copyright 2018-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        self.ensure_one()
        res = super(StockMove, self)._generate_valuation_lines_data(partner_id=partner_id, qty=qty, debit_value=debit_value, credit_value=credit_value,
                                                              debit_account_id=debit_account_id, credit_account_id=credit_account_id, description=description)
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        if self._is_in() and self.location_dest_id.usage == 'internal' and self.product_id.cost_method in ('fifo', 'average'):
            self.ensure_one()
            workcenter_ids = []
            work_center_cost_dict = self.env.context.get('work_center_cost_dict', False)
            count = 1
            byproduct_ids = self.production_id.bom_id.byproduct_ids.mapped('product_id')
            if self.product_id not in byproduct_ids:
                for work_order in self.production_id.workorder_ids:
                    work_center_cost = work_center_cost_dict and work_center_cost_dict.get(work_order.workcenter_id.id, False) or False
                    if work_order.workcenter_id.labor_expense_account_id and work_center_cost and work_order.workcenter_id.id not in workcenter_ids:
                        labor_debit_line_vals = {
                            'name': description,
                            'product_id': self.product_id.id,
                            'quantity': qty,
                            'product_uom_id': self.product_id.uom_id.id,
                            'ref': description,
                            'partner_id': partner_id,
                            'credit': work_center_cost if work_center_cost > 0 else 0,
                            'debit':-work_center_cost if work_center_cost < 0 else 0,
                            'account_id': work_order.workcenter_id.labor_expense_account_id.id,
                        }
                        labor_credit_line_vals = {
                            'name': description,
                            'product_id': self.product_id.id,
                            'quantity': qty,
                            'product_uom_id': self.product_id.uom_id.id,
                            'ref': description,
                            'partner_id': partner_id,
                            'debit': work_center_cost if work_center_cost > 0 else 0,
                            'credit':-work_center_cost if work_center_cost < 0 else 0,
                            'account_id': acc_src,
                        }
                        res.update({'labor_debit_line_vals' + str(count):labor_debit_line_vals, 'labor_credit_line_vals' + str(count):labor_credit_line_vals})
                        count = count + 1
                    workcenter_ids.append(work_order.workcenter_id.id)
        return res