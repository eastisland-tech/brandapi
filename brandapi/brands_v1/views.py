from flask import Blueprint, make_response, url_for, request, jsonify
from flask.views import MethodView
from pymongo import MongoClient
from bson import json_util


def mongodb(database='brandapi'):
    client = MongoClient('localhost', 27017)
    return client[database]

def bson_response(body, code=200):
    resp = make_response(json_util.dumps(body), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp

db = mongodb()
brands_v1 = Blueprint('brands_v1', __name__)


class BrandsAPI(MethodView):
    """
    Handles all API calls for Brands.
    """
    def get(self, brand_name):
        if brand_name is None:
            brands = db.brands.find()
            return bson_response(brands)
        else:
            # return a single brand
            brand = db.brands.find_one({"brand_name": brand_name})
            if not brand:
                return jsonify({"error": "brand not found"}), 404
            return bson_response(brand)

    def post(self):
        # create a new brand
        if not request.json or 'brand_name' not in request.json:
            return jsonify({'error': 'payload was invalid'}), 400
        if db.brands.find_one({'brand_name': request.json['brand_name']}):
            return jsonify({"error": "brand already exists"}), 400
        b_id = db.brands.insert({'brand_name': request.json['brand_name']})
        return bson_response(db.brands.find_one({"_id": b_id}))

    def delete(self, brand_name):
        brand = db.brands.find_one({"brand_name": brand_name})
        if not brand:
            return jsonify({'error': 'brand not found'}), 404
        db.brands.remove({'_id': brand['_id']})
        return jsonify({'result': True})

    def put(self, brand_name):
        if not request.json or 'brand_name' not in request.json:
            return jsonify({'error': 'payload was invalid'}), 400
        resp = db.brands.update({"brand_name": brand_name}, {"brand_name": request.json['brand_name']}, upsert=False)
        if not resp['updatedExisting']:
            return jsonify({'error': 'brand not found'}), 404
        return bson_response(db.brands.find_one({"brand_name": request.json['brand_name']}))


brands_views = BrandsAPI.as_view('brands_api')
brands_v1.add_url_rule('/', defaults={"brand_name": None},
                       view_func=brands_views, methods=['GET',])
brands_v1.add_url_rule('/', view_func=brands_views, methods=['POST',])
brands_v1.add_url_rule('/<string:brand_name>/', view_func=brands_views,
                       methods=['GET', 'PUT', 'DELETE'])
