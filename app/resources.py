"""
    Defining the Resources of the Rest
"""
from flask import abort, request
from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger

from app import stathat
from app.documents import Location as LocDoc
from app.documents import Rating as RateDoc


class LocationRating(Resource):
    """
        Ratings for Locations.
        In future can be used for any type of rating.
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
        location.reload()
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

    def __init__(self):
        super(LocationList, self).__init__()
        self.queryArgsKeys = [
            'name', 'website', 'phone', 'email',
            'locationType', 'coverage', 'services', 'tags'
        ]
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('lat', type=float)
        self.parser.add_argument('lng', type=float)
        self.parser.add_argument('rangeMeters', type=float, default=0)
        # May support these later
        # self.parser.add_argument('hqLat', type=float)
        # self.parser.add_argument('hqLng', type=float)
        self.parser.add_argument('website', type=str)
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('locationType', type=str)
        self.parser.add_argument('coverage', type=str, action='append')
        self.parser.add_argument('services', type=str, action='append')
        self.parser.add_argument('tags', type=str, action='append')

    @swagger.operation()
    def get(self):
        """
            Just get the list of all the Locations
        """
        # Defaults: Get all
        args = self.parser.parse_args()

        #  Grabs keys out of the args that we want to query by
        # Will do dynamic later
        # I think it will entail a custome Query
        # queryArgs = {}
        # for key in args:
        #     if key is not None and key in self.queryArgsKeys:
        #         queryArgs[key] = args[key]
        # allLocations = LocDoc.objects
        # for arg in queryArgs:
        #     allLocations = allLocations.filter(**{arg: queryArgs[arg]})

        # Brute and lame approach
        locations = LocDoc.objects
        for key in args:
            if args[key] is not None:
                if key == 'name':
                    locations = locations.filter(name__icontains=args[key])
                elif key == 'website':
                    locations = locations.filter(website__icontains=args[key])
                elif key == 'phone':
                    locations = locations.filter(phone__icontains=args[key])
                elif key == 'email':
                    locations = locations.filter(email__icontains=args[key])
                elif key == 'locationType':
                    locations = locations.filter(locationType__icontains=args[key])
                elif key == 'coverage':
                    locations = locations.filter(coverage__in=args[key])
                elif key == 'services':
                    locations = locations.filter(services__in=args[key])
                elif key == 'tags':
                    locations = locations.filter(tags__in=args[key])

        # Do a range search if there
        if 'rangeMeters' in args:
            locations = locations.filter(address__latLng__near=[args['lat'], args['lng']],
                                         address__latLng__max_distance=args['rangeMeters'])

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