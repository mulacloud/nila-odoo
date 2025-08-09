# -*- coding: utf-8 -*-
import uuid

from odoo import models, fields, api
from odoo.exceptions import UserError


class Zones(models.Model):
    _name = 'nila.zones'
    _description = 'nila.zones'
    _sql_constraints = [
        ('ip_uniq', 'unique(ip, hoster_id)', 'IP Address must be unique per hoster!'),
    ]

    ILLUMOS = "I"
    FREEBSD = "F"
    LINUX = "L"

    TYPE = [
        (ILLUMOS, 'Illumos'),
        (FREEBSD, "FreeBSD"),
        (LINUX, "GNU/Linux"),
    ]

    DRAFT = "D"
    NEW = "N"
    RUN = "R"
    SUSPEND = "S"

    ORDER_STATE = [
        (DRAFT, "Draft"),
        (NEW, "New"),
        (RUN, "Ready"),
        (SUSPEND, "Suspend"),
    ]

    @api.onchange("image_id")
    def _onchange_image_id(self):
        if self.image_id:
            if self.ip != "":
                self.ip = self.image_id.hoster_id.default_network
            if self.netmask != "":
                self.netmask = self.image_id.hoster_id.default_netmask
            if self.gateway != "":
                self.gateway = self.image_id.hoster_id.default_gateway

    def default_zones_id(self):
        return uuid.uuid4()
    
    def submit(self):
        for rec in self:
            ch_dom = [
                ("ip","=",rec.ip),
                ("hoster_id","=",rec.hoster_id.id),
                ("netmask","=",rec.netmask),
            ]
            zon = self.env['nila.zones'].search(ch_dom, limit=2)
            if len(zon) > 1:
                raise UserError(f"Duplicate IP detected, Name = {zon[0].name}, IP = {zon[0].ip}")
            sshkey = []
            for key in rec.sshkey_ids:
                sshkey.append(key.key)
            sshkey = "\n".join(sshkey)
            create_step = rec.image_id.create_step.format(
                zones_id = rec.zones_id,
                memory = rec.memory,
                disk = rec.disk,
                ip = rec.ip,
                netmask = rec.netmask,
                gateway = rec.gateway,
                sshkey = sshkey
            )
            start_step = rec.image_id.start_step.format(
                zones_id = rec.zones_id)
            stop_step = rec.image_id.stop_step.format(
                zones_id = rec.zones_id)
            destroy_step = rec.image_id.destroy_step.format(
                zones_id = rec.zones_id)
            rec.write({
                "order_state": self.NEW,
                "create_step": create_step,
                "start_step": start_step,
                "stop_step": stop_step,
                "destroy_step": destroy_step,
            })

    
    def run(self):
        for rec in self:
            self.env['nila.job'].create({
                "hoster_id": rec.hoster_id.id,
                "shell": rec.create_step
            })
            rec.write({"order_state": self.RUN})
                
    def suspend(self):
        for rec in self:
            self.env['nila.job'].create({
                "hoster_id": rec.hoster_id.id,
                "shell": rec.stop_step
            })
            rec.write({"order_state": self.SUSPEND})
    
    def start(self):
        for rec in self:
            self.env['nila.job'].create({
                "hoster_id": rec.hoster_id.id,
                "shell": rec.start_step
            })
            rec.write({"order_state": self.RUN})

    def unlink(self):
        for rec in self:
            if rec.order_state not in [self.DRAFT, self.NEW]:
                self.env['nila.job'].create({
                    "hoster_id": rec.hoster_id.id,
                    "shell": rec.destroy_step
                })
        return super(Zones,self).unlink()

    name = fields.Char(required=True)
    ip = fields.Char(required=True)
    power_on = fields.Boolean(default=False)
    netmask = fields.Char(required=True)
    gateway = fields.Char(required=True)
    memory = fields.Integer(required=True, default=512)
    disk = fields.Integer(required=True, default=1)
    zones_id = fields.Char(default=default_zones_id)
    zones_type = fields.Selection(TYPE, default=ILLUMOS, related="image_id.zones_type")
    order_state = fields.Selection(ORDER_STATE, default=DRAFT)
    sshkey_ids = fields.Many2many("nila.sshkey")
    hoster_id = fields.Many2one('nila.hoster',related="image_id.hoster_id", required=True)
    image_id = fields.Many2one('nila.image', required=True)
    create_step = fields.Text()
    start_step = fields.Text()
    stop_step = fields.Text()
    destroy_step = fields.Text()

