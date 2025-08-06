#-*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request


class Nila(http.Controller):
    @http.route('/nila/version', auth='nila_api_key', type='json')
    def version(self, **kw):
        return {'version': '0.0.1'}

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

