from odoo import models, fields


class Owner (models.Model):
    _name = 'owner'
    _description = 'Property Owner'


    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    property_ids = fields.One2many('app_one.property', 'owner_id', string='Properties')