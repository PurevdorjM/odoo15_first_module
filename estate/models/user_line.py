from odoo import fields, models


class UserLine(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id")
