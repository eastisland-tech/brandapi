from flask import make_response
from pymongo import MongoClient
from bson import json_util


def mongodb(database='brandapi'):
    """
    Returns a MongoDB database object.
    """
    client = MongoClient('localhost', 27017)
    return client[database]


def json_response(body, code=200):
    """
    A custom json response that also handles MongoDB
    results.
    """
    resp = make_response(json_util.dumps(body), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def json_error_response(errors, code):
    """
    A custom json error response to help clean
    up all the dictionaries being passed around
    in views.
    """
    resp = make_response(json_util.dumps({'error': errors}), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp
