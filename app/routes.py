"""
    Basic routes for our app, including status, index, resources, and error handlers
"""
from flask import jsonify, make_response
from app import app, stathat, api
from app.resources import Location, LocationList, LocationRating
from mongoengine.errors import NotUniqueError, DoesNotExist, ValidationError


@app.route('/')
def index():
    stathat.count('index', 1)
    return make_response(jsonify(response="This is Vets 4 Warriors!"), 200)

api.add_resource(LocationList, '/locations')
api.add_resource(Location, '/locations/<string:locId>')
api.add_resource(LocationRating, '/locations/rate/<string:locId>')


@app.errorhandler(NotUniqueError)
@app.errorhandler(ValidationError)
def mongo_error(error):
    app.logger.error(error.message)
    if app.debug:
        return make_response(jsonify(error=error.message), 400)
    return bad_req(error)


@app.errorhandler(400)
def bad_req(error):
    stathat.count('400', 1)
    return make_response(jsonify(error="Bad Request"), 400)


@app.errorhandler(DoesNotExist)
@app.errorhandler(404)
def not_found(error):
    stathat.count('404', 1)
    return make_response(jsonify(error="Resource does not exist"), 404)


@app.errorhandler(500)
def server_error(error):
    stathat.count('500', 1)
    return make_response(jsonify(error="uh oh server error"), 500)
