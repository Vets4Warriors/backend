"""
    Basic routes for our app, including status, index, resources, and error handlers
"""
from flask import jsonify, make_response, redirect
from app import app, stathat, api, apiVersion, apiSpecUrl, apiServerName
from app.resources import Location, LocationList, LocationRating
from mongoengine.errors import NotUniqueError, DoesNotExist, ValidationError, OperationError


@app.route('/')
def index():
    stathat.count('index', 1)
    return redirect('http://' + apiServerName + apiSpecUrl + '.html')

api.add_resource(LocationList, '/' + apiVersion + '/locations')
api.add_resource(Location, '/' + apiVersion + '/locations/<string:locId>')
api.add_resource(LocationRating, '/' + apiVersion + '/locations/<string:locId>/rate')


@app.errorhandler(OperationError)
@app.errorhandler(NotUniqueError)
@app.errorhandler(ValidationError)
def mongo_error(error):
    app.logger.error(error.message)
    if app.debug:
        resp = make_response(jsonify(error=error.message), 400)
    else:
        resp = bad_req(error)

    # Should put on all outgoing
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


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

