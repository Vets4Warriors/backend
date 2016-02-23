from flask import request
from flask_restful import Resource
from flask_restful_swagger import swagger

from APP.documents import Location as LocDoc


class Location(Resource):
    """

    """
    @swagger.operation(

    )
    def get(self, loc_id):
        """

        :return:
        """

        return {"hi": "hi"}, 200

    def put(self):
        return "", 201

    def post(self):
        """
        Add a location
        :return:
        """
        return "", 201

    def delete(self):
        return "", 204


class LocationList(Resource):
    def get(self):
        locations = LocDoc.objects()
        return locations, 200