# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Image(models.Model):
    _name = 'nila.image'
    _description = 'nila.image'

    ILLUMOS = "I"
    FREEBSD = "F"
    LINUX = "L"

    TYPE = [
        (ILLUMOS, 'Illumos'),
        (FREEBSD, "FreeBSD"),
        (LINUX, "GNU/Linux"),
    ]


    name = fields.Char()
    hoster_id = fields.Many2one("nila.hoster")
    zones_type = fields.Selection(TYPE, default=ILLUMOS)
    create_step = fields.Text()
    start_step = fields.Text()
    stop_step = fields.Text()
    destroy_step = fields.Text()

