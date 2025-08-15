# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


class Agent(models.Model):
    _name = 'nila.agent'
    _description = 'nila.agent'

    @api.depends('name', 'location')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" % (self.location, self.name)

    def _check_is_operational(self):
        for rec in self:
            dur = datetime.now() - rec.last_seen
            if dur.total_seconds() > rec.pull_interval:
                state = False
            else:
                state = True
            rec.write({'is_operational': state})

    name = fields.Char()
    ip = fields.Char()
    last_seen = fields.Datetime()
    pull_interval = fields.Integer(default=60)
    is_operational = fields.Boolean()
    location = fields.Char()
    notes = fields.Text()

