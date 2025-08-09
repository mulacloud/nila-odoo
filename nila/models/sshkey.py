# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SshKey(models.Model):
    _name = 'nila.sshkey'
    _description = 'nila.sshkey'

    name = fields.Char()
    key = fields.Text()

