from odoo import fields, models

class Tag(models.Model):
    _name = 'app_one.tag'
    _description = 'Property Tag'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.Many2many('app_one.property', string="Properties")