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

    @property
    def address(self):
        return "%s:%s" % (self.ip,self.port)

    name = fields.Char()
    ip = fields.Char()
    port = fields.Integer()
    os_type = fields.Selection(TYPE, default=SMARTOS)
    username = fields.Char()
    password = fields.Char()
    agent_id = fields.Many2one('nila.agent')
    default_network = fields.Char()
    default_netmask = fields.Char()
    default_gateway = fields.Char()
    stat_command = fields.Text()

