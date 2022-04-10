# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Үл хөдлөх хөрөнгийн санал"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Саналын үнийн утга нь - тоо байж болохгүй'),
    ]
    _order = "price desc"

    price = fields.Float("Үнэ")
    status = fields.Selection(string="Төлөв", selection=[
                              ("accepted", "Зөвшөөрсөн"), ("refused", "Татгалзсан")], readonly=True)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type")

    validity = fields.Integer("Хүчинтэй хоног:", default=7)
    date_deadline = fields.Date(
        "Дуусах хугацаа:", compute="_compute_date", inverse="_inverse_validity")

    create_date = fields.Date()

    @api.constrains("price", "property_id.expected_price")
    def _check_price(self):
        for price in self:
            persent = price.price / 100 * price.property_id.expected_price
            if persent < 90:
                raise ValidationError(
                    "Худалдаалагдах үнийн дүн хүлээгдэж буй үнийн дүнгийн 90 хувиас бага байж болохгүй")

    @api.depends("validity", "create_date")
    def _compute_date(self):
        for date in self:
            if date.create_date:
                date.date_deadline = date.create_date + \
                    relativedelta(days=date.validity)
            else:
                date.date_deadline = datetime.now() + relativedelta(days=date.validity)

    def _inverse_validity(self):
        for valid in self:
            valid.validity = int(
                valid.date_deadline.strftime("%d")) - int(valid.create_date.strftime("%d"))

    def action_accepted(self):
        for offer in self:
            if offer.property_id.selling_price:
                raise UserError(
                    ("Худалдагдсан үл хөдлөх хөрөнгийг дахиж худалдаж болохгүй"))
            else:
                offer.status = "accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.partner_id = offer.partner_id
                offer.property_id.state = "offer_accepted"
        return True

    def action_refused(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(
            vals['property_id']).add_offer_state()
        return super(EstatePropertyOffer, self).create(vals)
