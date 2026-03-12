from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'app_one.property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default=' New', string='Reference', readonly=True)
    name = fields.Char(string='Name', required=False)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', required=False)
    date_available = fields.Date(string='Date Available', tracking=True)
    expected_selling_date = fields.Date(string='Expected Selling Date', tracking=True)
    is_lated = fields.Boolean(string='Is Late', store=True)
    
    expected_price = fields.Float(string='Expected Price') # digits=(0, 5))
    selling_price = fields.Float(string='Selling Price')    
    difference = fields.Float(compute='_compute_difference', store=True, string='Difference', readonly=False)
    
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sq ft)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sq ft)') 
    
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north', string='Garden Orientation')

    # relation of many to one and the related fields of the data coming from the model 
    owner_id = fields.Many2one('app_one.owner', string='Owner')
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)

    # relation of many to many with the tag model and the field name is tag_ids which is a list of tags associated with the property,
    tag_ids = fields.Many2many('app_one.tag', string='Tags')

    lines_ids = fields.One2many('property.line', inverse_name='property_id')

    _sql_constraints = [('unique_name', 'unique(name)', 'The name must be unique')]

    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft', string='Status', tracking=True)

    # this is an example of a constraint that checks if the number of bedrooms is greater than zero and less than 100,
    # which is a python type of constraint in Odoo.
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_than_zero(self):
        for record in self:
            if record.bedrooms <= 0:
                raise ValidationError("The number of bedrooms cannot be zero or negative.")
            if record.bedrooms > 99: 
                raise ValidationError("The number of bedrooms cannot exceed 99.")

    def action_draft(self):
        for rec in self:
            rec.create_property_history(old_state=rec.state, new_state='draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_property_history(old_state=rec.state, new_state='pending')
            rec.write({'state': 'pending'})

    def action_sold(self):
        for rec in self:
            rec.create_property_history(old_state=rec.state, new_state='sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_property_history(old_state=rec.state, new_state='closed')
            rec.state = 'closed'

    def check_expected_date(self):
        # because the automated action or cron action does not return self,
        # we need to search for all the records of the property model and check if the expected selling date is less than the current date,
        # if it is less than the current date,
        # we will set the is_lated field to True, otherwise we will set it to False.
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_lated = True
            else:
                rec.is_lated = False

    @api.depends('selling_price', 'expected_price')
    def _compute_difference(self):
        for record in self:
            if record.selling_price and record.expected_price:
                record.difference = record.selling_price - record.expected_price
            else:
                record.difference = 0.0

    @api.onchange('selling_price')
    def _onchange_selling_price(self):
        if self.selling_price and self.selling_price <= 0:
            return {
                "warning": {
                    "title": "Invalid Selling Price",
                    "message": "The selling price must be a positive value.",
                }
            }
    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == ' New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res
    
    def create_property_history(self, old_state, new_state, reason=False):
        for rec in self:
            # 1. We prepare the lines separately to keep the 'create' dict clean
            # 2. Added a check 'if rec.line_ids' so we don't try to loop over an empty field
            history_lines = [
                (0, 0, {
                    'description': line.description,
                    'area': line.area
                }) for line in rec.lines_ids
            ] if rec.lines_ids else []

            self.env['app_one.property_history'].create({
                'property_id': rec.id,
                'user_id': self.env.user.id, # Modern Odoo style
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': history_lines,
            })
                
    def action_open_change_state_wizard(self):
         action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
         action['context'] = {'default_property_id': self.id}
         return action
    
class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line' # Added this to avoid the "no _description" warning
      
    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('app_one.property')