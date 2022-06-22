# (c) 2018-2022 Sodexis
# License OPL-1 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _cal_price(self, consumed_moves):
        """Set a price unit on the finished move according to `consumed_moves`.
        """
        work_center_cost_dict = {}
        for work_order in self.workorder_ids:
            work_center_cost = 0
            if work_order.workcenter_id.labor_expense_account_id:
                time_lines = work_order.time_ids.filtered(lambda x: x.date_end and not x.cost_already_recorded)
                duration = sum(time_lines.mapped('duration'))
                work_center_cost = work_center_cost_dict.get(work_order.workcenter_id.id, False) or 0.0
                work_center_cost += (duration / 60.0) * work_order.workcenter_id.costs_hour
                work_center_cost_dict.update({work_order.workcenter_id.id : work_center_cost})
        if work_center_cost_dict:
            self.env.context = dict(self.env.context)
            self.env.context.update({'work_center_cost_dict': work_center_cost_dict})
        return super(MrpProduction, self)._cal_price(consumed_moves)
