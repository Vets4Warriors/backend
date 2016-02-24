"""
    Defining the Resources of the Rest
"""
from flask import abort, request
from flask_restful import Resource
from flask_restful_swagger import swagger

from APP import stathat
from APP.documents import Location as LocDoc
from APP.documents import Address as AddrDoc
from APP.documents import Rating as RateDoc


class LocationRating(Resource):
    """

    """
    @swagger.operation()
    def post(self, locId):
        """

        :param locId:
        :return:
        """

        location = LocDoc.objects.get(id=locId)
        try:
            # Validation errors are caught by Flask if they are raised
            rating = RateDoc.from_data(request.get_json(), validate=True)
        except (TypeError, KeyError) as ex:
            abort(400)

        location.update(push__ratings=rating)
        location.save()
        return location.to_json(), 201


class Location(Resource):
    """
        The individual Location
    """
    @swagger.operation()
    def get(self, locId):
        """
            Get a Location by object id
        """
        location = LocDoc.objects.get(id=locId)
        stathat.count('location_get ' + str(location.id), 1)
        return location.to_json(), 200

    @swagger.operation()
    def put(self, locId):
        """
            Update a Location
        """
        # First find the Location
        location = LocDoc.objects.get(id=locId)
        # Todo: Then update it!
        # In order to update by specific key, would have to do a lot of conditionals
        # So just don't. Or do later.
        try:
            updatedLocation = LocDoc.from_data(request.get_json(), validate=True)
        except (TypeError, KeyError) as ex:
            abort(400)

        location.update(
            name=updatedLocation.name,
            address=updatedLocation.address,
            hqAddress=updatedLocation.hqAddress,
            website=updatedLocation.website,
            phone=updatedLocation.phone,
            email=updatedLocation.email,
            locationType=updatedLocation.locationType,
            coverage=updatedLocation.coverage,
            services=updatedLocation.services,
            tags=updatedLocation.tags,
            comments=updatedLocation.comments
        )
        # Will eventually do update logs/diffs

        stathat.count('location_put: ' + str(location.id), 1)
        return location.to_json(), 201

    @swagger.operation()
    def delete(self, locId):
        """
            Delete a Location
        """
        location = LocDoc.objects.get(id=locId)
        location.delete()
        stathat.count('location_delete ' + str(location.id), 1)
        return '', 204  # No Content Return


class LocationList(Resource):
    """
        Represents all of the Locations as a set
        Can either get all or add a new Location to the set
    """

    @swagger.operation()
    def get(self):
        """
            Just get the list of all the Locations
        """
        # Todo: Parse the args and query parameters
        locations = LocDoc.objects()
        stathat.count('location_get_all', 1)
        return locations.to_json(), 200

    @swagger.operation()
    def post(self):
        """
            Add a Location
        """

        try:
            location = LocDoc.from_data(request.get_json(), validate=True)
        except (TypeError, KeyError) as ex:
            abort(400)

        location.get_rating()
        location.to_json()
        location.save()

        stathat.count('location_post', 1)
        return location.to_json(), 201
