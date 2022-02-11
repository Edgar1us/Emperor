
from odoo import models, fields, api

# herència de classe

class king_premium(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'king Premium'
    # Main fields
    is_premium = fields.Boolean()





