from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops

import APP.documents as docs

class AddressResource(Resource):
    document = docs.Address

class LocationResource(Resource):
    """

    """
    document = docs.Location

    related_resources = {
        'address': AddressResource
    }

    filters = {
        'name': [ops.Startswith, ops.Exact]
    }

