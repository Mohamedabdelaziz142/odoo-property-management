from odoo import models


# The Client model inherits from the Owner model, which means that it will have all the fields and behavior of the Owner model,
# This is an example of model inheritance in Odoo, which allows to prototupe a new model based on an existing one,
#  reusing its fields and methods, and adding new ones if needed.
#but most importantly a new table is mapped not just extending a table here 
class Client (models.Model):

     _name = 'app_one.client'
     _inherit = 'app_one.owner'    
