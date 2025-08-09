# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api


class Job(models.Model):
    _name = 'nila.job'
    _description = 'nila.job'

    NEW = "N"
    RUN = "R"
    DONE = "D"
    ERROR = "E"

    STATE = [
        (NEW, "New"),
        (RUN, "Run"),
        (DONE, "Done"),
        (ERROR, "Error"),
    ]


    def _default_name(self):
        return str(uuid.uuid4())

    def run(self):
        pass

    name = fields.Char(default=_default_name)
    shell = fields.Text(required=True)
    output = fields.Text()
    error = fields.Text()
    state = fields.Selection(STATE, default=NEW)
    agent_id = fields.Many2one("nila.agent", related="hoster_id.agent_id")
    hoster_id = fields.Many2one("nila.hoster", required=True)

