#-*- coding: utf-8 -*-
import json
from datetime import datetime

from odoo import http
from odoo.http import request


class Agent(http.Controller):
    @http.route('/nila/agent/register', csrf=False, methods=['POST'], auth='nila_api_key', type='json')
    def register(self, name, **kw):
        agent_obj = request.env['nila.agent'].sudo()
        if agent_obj.search([('name', '=', name)]):
            return {'msg': 'already exists', 'code': 400}
        agent_obj.create({
            'name': name,
            'ip': kw['ip'],
            'last_seen': datetime.now(),
            'is_operational': True
        })
        return {'msg': 'ok'}

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

