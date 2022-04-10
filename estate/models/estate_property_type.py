# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Үл хөдлөх хөрөнгийн төрлийн хүснэгт"
    _order = "name asc"

    name = fields.Char("Нэр", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(
        "Саналын тоо:", compute="_compute_offer_count")

    @api.depends("property_ids")
    def _compute_offer_count(self):
        for count in self:
            if count.property_ids.offer_ids:
                count.offer_count = len(count.property_ids.offer_ids)
            else:
                count.offer_count = 0
        return True

    def action_tree_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            'view_mode': 'tree',
            # 'domain': [("offer_ids.property_type_id", "=", self.property_ids.offer_ids.property_type_id)],
            # "res_id": self.property_ids.offer_ids.property_id,
        }
