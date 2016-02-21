"""

"""
from flask import jsonify, make_response
import logging
from APP import app, db, stathat


@app.route('/')
def index():
    stathat.count('index_hits', 1)
    return make_response(jsonify("This is Vets 4 Warriors!"), 200)


@app.errorhandler(404)
def not_found(error):
    stathat.count('404_hits', 1)
    return make_response(jsonify("Resource does not exist"), 404)


@app.errorhandler(500)
def server_error(error):
    stathat.count('500)hits', 1)
    return make_response(jsonify("uh oh server error"), 500)

