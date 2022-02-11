# -*- coding: utf-8 -*-
# from odoo import http


# class Emperor(http.Controller):
#     @http.route('/emperor/emperor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emperor/emperor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emperor.listing', {
#             'root': '/emperor/emperor',
#             'objects': http.request.env['emperor.emperor'].search([]),
#         })

#     @http.route('/emperor/emperor/objects/<model("emperor.emperor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emperor.object', {
#             'object': obj
#         })
