from flask import Blueprint, make_response, url_for, request, jsonify
from flask.views import MethodView
from ..utils import json_response, mongodb, json_error_response
from validators import UpdateBrandValidator, CreateBrandValidator


db = mongodb()
brands_v1 = Blueprint('brands_v1', __name__)


class BrandsAPI(MethodView):
    """
    Handles all API calls for Brands.
    """
    def get(self, brand_name):
        """
        Get all brands, or a specific Brand.
        """
        if brand_name is None:
            brands = db.brands.find({}, {'_id': False})
            return json_response(brands)
        else:
            # return a single brand
            brand = db.brands.find_one({"brand_name": brand_name}, {'_id': False})
            if not brand:
                return json_error_response('brand_not_found', 404)
            return json_response(brand)

    def post(self):
        """
        Create a new Brand.
        """
        v = CreateBrandValidator(request.json)
        if request.json and v.validate():
            if db.brands.find_one({'brand_name': request.json['brand_name']}):
                return json_error_response('brand already exists', 400)

            b_id = db.brands.insert({'brand_name': request.json['brand_name']})
            brand = db.brands.find_one({"_id": b_id}, {'_id': False})
            return json_response(brand)
        return json_error_response(v.errors, 400)

    def delete(self, brand_name):
        """
        Delete a Brand.
        """
        brand = db.brands.find_one({"brand_name": brand_name})
        if not brand:
            return json_error_response('brand not found', 404)
        db.brands.remove({'_id': brand['_id']})
        return jsonify({'result': True})

    def put(self, brand_name):
        """
        Update a Brand. If it doesn't exist, create it.
        """
        v = UpdateBrandValidator(request.json)
        if request.json and v.validate():
            resp = db.brands.update({"brand_name": brand_name},
                {"brand_name": request.json['brand_name']}, upsert=True)
            return json_response(db.brands.find_one({
                "brand_name": request.json['brand_name']}, {'_id': False}))
        return json_response(v.errors), 400


# Register out url rules with the blueprint
brands_views = BrandsAPI.as_view('brands_api')
brands_v1.add_url_rule('/', defaults={"brand_name": None},
                       view_func=brands_views, methods=['GET',])
brands_v1.add_url_rule('/', view_func=brands_views, methods=['POST',])
brands_v1.add_url_rule('/<string:brand_name>/', view_func=brands_views,
                       methods=['GET', 'PUT', 'DELETE'])
