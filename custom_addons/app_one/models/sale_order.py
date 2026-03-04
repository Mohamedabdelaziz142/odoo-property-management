from odoo import models, fields


class SaleOrder (models.Model):
   
    _inherit = 'sale.order'


# This field creates a many-to-one relationship between the sale.order model and the app_one.property model,
#  allowing each sale order to be associated with a specific property.
# this is an extention of the model inhertance to add a new field to the existing sale.order model without modifying the original code, 

    property_id =fields.Many2one('app_one.property', string='Property')


    
# example of overriding the action_confirm method of sale.order model to add a note when the order is confirmed
#  which is python type of method overriding in Odoo.
#  This allows us to add custom behavior to the existing method without modifying the original code, 
# ensuring that our changes are maintainable and compatible with future updates of Odoo.

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.note = 'This is a confirmed order.'
        return res
  