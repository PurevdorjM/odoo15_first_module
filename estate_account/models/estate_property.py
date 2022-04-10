# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, Command


class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("Би 's%' удамшсан модуль дотроос хэвлэж байна.")
        self.env["account.move"].with_context(default_move_type='entry').create(
            {
                # "move_type": "out_invoice",
                "partner_id": self.partner_id,
                "journal_id": self.env["account.move"]._get_default_journal().id,
                "invoice_line_ids": [
                    Command.create({
                        "name": "Estate Invoice Line",
                        "quantity": 1,
                        "price_unit": self.selling_price,
                    })
                ],
            }
        )
        return super().action_sold()
