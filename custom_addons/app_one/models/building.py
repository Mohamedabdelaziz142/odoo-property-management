from odoo import models, fields

class Building(models.Model):
    _name = 'app_one.building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    #_rec_name = 'no'

    no = fields.Integer(string='Building Number', required=True)
    code = fields.Char(string='Address')
    description = fields.Text(string='Description')
  #now _rec_name is name sice its automatiaclly is the default for it sice its a reserved feild name in odoo
    name = fields.Char(string='Building Name')
  #for the active feild we can use it to archive the record instead of deleting it so we can keep the history of the records and we can also use it to filter the records in the views
    active = fields.Boolean(string='Active', default=True)

