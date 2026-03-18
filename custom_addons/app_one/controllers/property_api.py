from odoo import http
from odoo.http import request
import json
# from urllib.parse import parse_qs  # Documentation: Use this if you need to manually parse query_string

def valid_response(data, status):
    response_body = {
        'message': 'successful',
        'data': data
    }
    return request.make_json_response(response_body, status = status)

def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status = status)

    
class PropertyApi(http.Controller):

    # --- 1. POST METHOD (HTTP) ---
    @http.route('/v1/app_one.property', type='http', auth='none', methods=['POST'], csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            
            if not vals.get('name'):
                return request.make_json_response({'error': 'Name is required'}, status=400)

            res = request.env['app_one.property'].sudo().create(vals)
            return request.make_json_response({
                'message': 'property has been created successfully',
                'id': res.id,
                'name': res.name
            }, status=201)
        except Exception as error:
            return request.make_json_response({'error': str(error)}, status=400)

    # --- 2. PUT METHOD (Update) ---
    @http.route('/v1/app_one.property/<int:property_id>', type='http', auth='none', methods=['PUT'], csrf=False)
    def update_property(self, property_id):
        try:
            property_rec = request.env['app_one.property'].sudo().browse(property_id)
            if not property_rec.exists():
                return request.make_json_response({'error': 'ID does not exist'}, status=404)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_rec.write(vals)
            
            return request.make_json_response({
                'message': 'property updated successfully',
                'id': property_rec.id
            }, status=200)
        except Exception as error:
            return request.make_json_response({'error': str(error)}, status=400)

    # --- 3. GET METHOD (Read Single) ---
    @http.route('/v1/app_one.property/<int:property_id>', type='http', auth='none', methods=["GET"], csrf=False)
    def read_property(self, property_id):
        try:
            property_rec = request.env['app_one.property'].sudo().browse(property_id)
            if not property_rec.exists():
                return invalid_response('ID does not exist', status=404)
            
            return valid_response({
                'id': property_rec.id,
                'name': property_rec.name,
                'ref': property_rec.ref or "",
                'description': property_rec.description or "",
                'bedrooms': property_rec.bedrooms,
            }, status=200)
        except Exception as error:
            return request.make_json_response({'error': str(error)}, status=400)

    # --- 4. GET METHOD (List with request.params) ---
    @http.route('/v1/properties', type='http', auth='none', methods=["GET"], csrf=False)
    def get_property_list(self):
        try:
            # DOCUMENTATION: The old manual way with parse_qs:
            # query_string = request.httprequest.query_string.decode('utf-8')
            # parms = parse_qs(query_string)
            # if parms.get('state'): domain += [('state', '=', parms.get('state')[0])]
            
            # MODERN WAY: Using request.params
            state_val = request.params.get('state')
            
            property_domain = []
            if state_val:
                 property_domain = [('state', '=', state_val)]
            
            property_ids = request.env['app_one.property'].sudo().search(property_domain)
            
            if not property_ids:
                 return request.make_json_response({'error': 'There are no records'}, status=404)

            return valid_response([{
                'id': rec.id,
                'name': rec.name,
                'ref': rec.ref or "",
                'description': rec.description or "",
                'bedrooms': rec.bedrooms,
            } for rec in property_ids], status=200)
        except Exception as error:
            return request.make_json_response({'error': str(error)}, status=400)

    # --- 5. DELETE METHOD ---
    @http.route('/v1/app_one.property/<int:property_id>', type='http', auth='none', methods=["DELETE"], csrf=False)
    def delete_property(self, property_id):
        try:
            property_rec = request.env['app_one.property'].sudo().browse(property_id)
            if not property_rec.exists():
                return request.make_json_response({'error': 'ID does not exist'}, status=404)
            
            property_rec.unlink()
            return request.make_json_response({'message': 'Property deleted successfully'}, status=200)
        except Exception as error:
            return request.make_json_response({'error': str(error)}, status=400)