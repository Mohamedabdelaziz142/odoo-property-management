from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

# This field establishes a one-to-many relationship between the res.partner model and the app_one.property model.
# The field name is property_id, and it allows you to access the properties associated with a partner (owner) through this relationship. 
    property_id = fields.Many2one('app_one.property', string='Properties')       
    price = fields.Float(related='property_id.selling_price', string='Property Selling Price', store=True)

  


# This field will store the selling price of the associated property, and it is computed based on the related property's selling price.
  #   price = fields.Float(compute='_compute_price', store=True)   
  # @api.depends('property_id')
   # def _compute_price(self):
    #    for partner in self:
     #       partner.price = partner.property_id.selling_price if partner.property_id else 0.0 
