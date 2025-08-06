# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Hoster(models.Model):
    _name = 'nila.hoster'
    _description = 'nila.hoster'

    SMARTOS = "S"
    FREEBSD = "F"

    TYPE = [
        (SMARTOS, 'SmartOS'),
        (FREEBSD, "FreeBSD")
    ]

    name = fields.Char()
    ip = fields.Char()
    os_type = fields.Selection(TYPE, default=SMARTOS)
    username = fields.Char()
    password = fields.Char()
    agent_id = fields.Many2one('nila.agent')

