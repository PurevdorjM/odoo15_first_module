# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Үл хөдлөх хөрөнгийн модуль"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Хүлээгдэж буй үнийн утга нь - тоо байж болохгүй'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'Худалдах үнийн утга нь - тоо байж болохгүй'),
        ('name_uniq', 'unique(name)',
         'Ерөнхий мэдээллийн нэр давхардаж болохгүй'),
    ]
    _order = "id desc"

    name = fields.Char("Нэр:", required=True)
    description = fields.Text("Тайлбар:")
    postcode = fields.Char("Шуудангийн код:")
    date_availability = fields.Date(
        "Боломжит огноо:", copy=False, default=lambda self: fields.Datetime.now())
    expected_price = fields.Float("Хүлээгдэж буй үнэ:", required=True)
    selling_price = fields.Float("Худалдах үнэ:", readonly=True, copy=False)
    bedrooms = fields.Integer("Унтлагын өрөөний тоо:", default=2)
    living_area = fields.Integer("Амьдрах талбай:")
    facades = fields.Integer("Фасадуудын тоо:")
    garage = fields.Boolean("Граж:")
    garden = fields.Boolean("Цэцэрлэг:")
    garden_area = fields.Integer("Цэцэрлэгийн талбайн хэмжээ:")
    garden_orentation = fields.Selection(string="Цэцэрлэгийн байршил", selection=[(
        "north", "Хойд"), ("south", "Өмнөд"), ("east", "Зүүн"), ("west", "Баруун")], help="Та зүг чигээ сонгоно уу")
    state = fields.Selection(string="Төлөв", selection=[("new", "Шинэ"), ("offer_recieved", "Хүлээн авсан"), (
        "offer_accepted", "Хүлээн зөвшөөрсөн"), ("sold", "Зарагдсан"), ("canceled", "Буцаагдсан")], default="new", help="Та үл хөдлөхийн төлөвийг сонгон уу?")
    active = fields.Boolean(string="Идэвхтэй", default=True)

    # ManyToOne холбоос хийж системийн үндсэн буюу кор-оос user болон partner хоёрыг дуудаж байгаа хэсэг
    partner_id = fields.Many2one("res.partner", string="Худалдан авагч")
    user_id = fields.Many2one("res.users", string="Худалдагч")
    tag_ids = fields.Many2many("estate.property.tag", string="Шошго")
    property_type_id = fields.Many2one("estate.property.type", string="Төрөл")
    # One2Many холбоос хийж estate.property.offer моделоос field-үүд оруулж ирж байна.
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id")

    # Тооцоолсон талбар буюу compute талбарын жишээ
    total_area = fields.Integer(compute='_compute_area', string="Нийт үнэ:")
    best_price = fields.Integer(
        compute="_compute_best_price", string="Хамгийн сайн үнэ:")

    # total_area тооцоолсон талбарын функц

    @api.depends('garden_area', 'living_area')
    def _compute_area(self):
        for area in self:
            area.total_area = area.garden_area + area.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        if self.offer_ids:
            calculate = max(self.offer_ids.mapped("price"))
        else:
            calculate = 0
        for best in self:
            best.best_price = calculate

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == 1:
            self.garden_area = 10
            self.garden_orentation = "north"
        else:
            self.garden_area = 0
            self.garden_orentation = ""

    def action_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError(
                    ("Нэгэнт цуцлагдсан төлөвийг өөрчлөх боломжгүй"))
            else:
                property.state = "sold"
        return True

    def action_canceled(self):
        for property in self:
            property.state = "canceled"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_check(self):
        for check in self:
            if check.state == "offer_recieved" or check.state == "offer_accepted":
                raise UserError(
                    _("Та '%s' -төлөвтэй хөрөнгийн бүртгэл устгах боломжгүй", check.state))
            elif check.offer_ids.id:
                raise UserError(
                    "Та саналуудыг устгасны дараа үл хөдлөхийн мэдээллийг устгаж болно.")

    def add_offer_state(self):
        for property in self:
            property.state = "offer_recieved"
        return True
