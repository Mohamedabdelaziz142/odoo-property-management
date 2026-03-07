from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'app_one.property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=False)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', required=False)
    date_available = fields.Date(string='Date Available',tracking=True)
    expected_price = fields.Float(string='Expected Price', digits=(0, 5))
    selling_price = fields.Float(string='Selling Price')
    difference = fields.Float(compute = '_compute_difference', store=True, string='Difference',readonly= False)
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

# relation of many to one and the related fields of the data coming from the omdel 
    owner_id = fields.Many2one('app_one.owner', string='Owner')
    owner_address = fields.Char(related = 'owner_id.address', readonly=False)
    owner_phone = fields.Char(related = 'owner_id.phone', readonly=False)

# relation of many to many with the tag model and the field name is tag_ids which is a list of tags associated with the property,
    tag_ids = fields.Many2many('app_one.tag', string='Tags')

    lines_ids = fields.One2many('property.line', inverse_name= 'property_id')

    _sql_constraints = [ ('unique_name', 'unique(name)', 'The name must be unique') ]

    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ] ,default='draft', string='Status', tracking=True)

    # this is an example of a constraint that checks if the number of bedrooms is greater than zero and less than 100,
    #  which is a python type of constraint in Odoo.
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_than_zero(self):
        for record in self:
            if record.bedrooms <= 0:
                raise ValidationError("The number of bedrooms cannot be zero or negative.")
            if record.bedrooms > 99: raise ValidationError("The number of bedrooms cannot exceed 99.")

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            #rec.write({'state': 'draft'})

    def action_pending(self):
        for rec in self:
            rec.write({
                'state': 'pending'})


    def action_sold(self):
        for rec in self:
            rec.state = 'sold'
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


class PropertyLine(models.Model):
      _name = 'property.line'
      
      area = fields.Float()
      description = fields.Char()
      property_id = fields.Many2one('app_one.property')


      
    #@api.model_create_multi  
    #def create(self, vals) :
     # res = super(Property, self).create(vals)
      #for val in vals:
       # if 'selling_price' not in val or not val['selling_price']:
        #    raise ValidationError("selling_price is required and cannot be empty.")
      #return res
    
    # @api.model
    # def search(self, domain, offset=0, limit=0, order=None, access_rights_uid=None):
      #  res = super(Property, self).search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
      #  fo   rec in res:
            # if record.selling_price <= 0:
                # raise ValidationError("The selling price must be greater than zero.")
      #  return res
    
    # def write(self, vals):
      # res = super(Property, self).write(vals)
      # for val in vals:
        # if 'selling_price' not in val or not val['selling_price']:
            # raise ValidationError("selling_price is required and cannot be empty.")
      # return res
    
  #  def unlink(self):
   #    res = super(Property, self).unlink()
    #   return res