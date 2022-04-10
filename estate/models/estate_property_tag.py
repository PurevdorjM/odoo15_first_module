# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Үл хөдлөх хөрөнгийн шошго"
    _order = "name asc"

    name = fields.Char("Нэр", required=True)
    color = fields.Integer("Өнгө")
