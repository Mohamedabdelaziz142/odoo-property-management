from odoo.tests.common import TransactionCase
from odoo import fields



class TestProperty(TransactionCase):
  

  def setUp(self, *args, **kwargs):
    super(TestProperty, self).setUp()

    self.property_01_record = self.env['app_one.property'].create({
      'ref': 'PRT1000',
      'name': 'property 1000',
      'description': 'property 1000 description',
      'postcode': '4893563',
      'date_available': fields.Date.today(),
      'bedrooms': 5,
      'selling_price': 500000,
      'expected_price': 500000,
    })
  def test_1_property_values(self):
     property_id = self.property_01_record
     self.assertRecordValues(property_id, [{
       'ref': 'PRT1000',
       'name': 'property 1000',
       'description': 'property 1000 description',
       'postcode': '4893563',
       'date_available': fields.Date.today(),
       'bedrooms': 5,
       'selling_price': 500000,
       'expected_price': 500000,
    }])

