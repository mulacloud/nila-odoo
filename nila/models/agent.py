# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Agent(models.Model):
    _name = 'nila.agent'
    _description = 'nila.agent'

    @api.depends('name', 'location')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" % (self.location, self.name)

    name = fields.Char()
    ip = fields.Char()
    last_seen = fields.Datetime()
    pull_interval = fields.Integer(default=60)
    is_operational = fields.Boolean()
    location = fields.Char()
    notes = fields.Text()

