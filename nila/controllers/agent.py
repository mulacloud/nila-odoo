#-*- coding: utf-8 -*-
import json
import base64
from datetime import datetime

from odoo import http
from odoo.http import request


class Agent(http.Controller):
    @http.route('/nila/agent/register', csrf=False, methods=['POST'], auth='nila_api_key', type='json')
    def register(self, name, **kw):
        agent_obj = request.env['nila.agent'].sudo()
        hoster_obj = request.env['nila.hoster'].sudo()
        agent = agent_obj.search([('name', '=', name)])
        if agent:
            hoster = []
            for hs in hoster_obj.search([("agent_id", "=", agent.id)]):
                hoster.append({
                    "address": hs.address,
                    "username": hs.username,
                    "password": hs.password,
                    "stat_command": base64.b64encode(hs.stat_command.encode("utf-8"))
                })
            return {'msg': 'already exists', 'code': 400,'hoster': hoster, 'pull_interval': agent.pull_interval}
        agent = agent_obj.create({
            'name': name,
            'ip': kw['ip'],
            'last_seen': datetime.now(),
            'is_operational': True
        })
        return {'msg': 'ok', 'pull_interval': agent.pull_interval, 'code': 201}

#     @http.route('/nila/nila/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nila.listing', {
#             'root': '/nila/nila',
#             'objects': http.request.env['nila.nila'].search([]),
#         })

#     @http.route('/nila/nila/objects/<model("nila.nila"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nila.object', {
#             'object': obj
#         })

