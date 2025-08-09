#-*- coding: utf-8 -*-
import json
import base64

from odoo import http
from odoo.http import request


class Job(http.Controller):
    @http.route('/nila/job/pull', auth='nila_api_key', csrf=True, methods=['POST'], type='json')
    def pull(self, name, stat, result):
        agent_obj = request.env['nila.agent'].sudo()
        job_obj = request.env['nila.job'].sudo()
        zones_obj = request.env['nila.zones'].sudo()
        agent = agent_obj.search([('name', '=', name)], limit=1)
        job = job_obj.search([
            "&", 
            ('agent_id', "=", agent.id),
            ("state", "=", job_obj.NEW)])
        result_out = []
        for res in job:
            result_out.append({
                "name": res.name,
                "shell": res.shell,
                "hoster": {
                    "address": res.hoster_id.address,
                    "username": res.hoster_id.username,
                    "password": res.hoster_id.password,
                }
            })
            res.write({'state': job_obj.RUN})
        if len(result) > 0:
            for jb in result:
                output = base64.b64decode(jb['output'])
                error = base64.b64decode(jb['error'])
                job = job_obj.search([
                    "&",
                    ("name", '=', jb['job_id']),
                    ("state", "=", job_obj.RUN)
                ], limit=1)
                job.write({
                    "output": output,
                    "error": error,
                    "state": jb['state']
                })
        if len(stat) > 0:
            for st in stat:
                zdom = [
                    ("zones_id", "=", st['zones_id']),
                ]
                zones = zones_obj.search(zdom)
                for zn in zones:
                    zn.write({'power_on': st['power_on']})

        return {'job': result_out}

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

