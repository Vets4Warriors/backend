"""

"""
from flask import jsonify, make_response, request
from APP import app, db, stathat, api
from APP.resources import Location, LocationList


@app.route('/')
def index():
    stathat.count('index_hits', 1)
    return make_response(jsonify(response="This is Vets 4 Warriors!"), 200)


api.add_resource(LocationList, '/locations')
api.add_resource(Location, '/locations/<string:loc_id>')


@app.errorhandler(404)
def not_found(error):
    stathat.count('404_hits', 1)
    return make_response(jsonify(response="Resource does not exist"), 404)


@app.errorhandler(500)
def server_error(error):
    stathat.count('500_hits', 1)
    return make_response(jsonify(response="uh oh server error"), 500)

