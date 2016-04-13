"""
    Defining the Resources of the Rest
"""
from flask import abort, request
from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger

from app import stathat
from app.documents.Location import Location as LocDoc, LocationModel as LocMod
from app.documents.Rating import Rating as RateDoc, RatingModel as RateMod
from app.documents.Rating import Rating as RateDoc, RatingModel as RateMod
from app.documents.Address import Address as AddrDoc, AddressModel as AddrMod


class LocationRating(Resource):
    """
        Ratings for Locations.
        In future can be used for any type of rating.
    """
    @swagger.operation(
        notes="Rate a location",
        responseClass=LocMod.__name__,
        nickname="rate",
        parameters=[
            {
                "name": "rating",
                "description": "Rating from 1 to 5.",
                "required": True,
                "dataType": RateMod.__name__,
                "paramType": "body"
            }
        ],
        responseMesssage=[
            {
                "code": 201,
                "message": "Created and stored the rating!"
            },
            {
                "code": 400,
                "message": "Some part of the body data was malformed!"
            }
        ]
    )
    def post(self, locId):
        """
            Rate a Location
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
        # Don't really need to send it back but whatevs
        return location.to_json(), 201, {'Access-Control-Allow-Origin': '*'}

    def options(self, locId):
        print 'OPTIONS'
        pass


class Location(Resource):
    """
        The individual Location
    """
    @swagger.operation(
        responseClass=LocMod.__name__,
        nickname="get",
        responseMessages=[
            {
                "code": 201,
                "message": "Created and returned."
            },
            {
                "code": 404,
                "message": "No location with that id"
            }
        ]
    )
    def get(self, locId):
        """
            Get a Location by object id
        """
        location = LocDoc.objects.get(id=locId)
        stathat.count('location_get ' + str(location.id), 1)
        return location.to_json(), 200, {'Access-Control-Allow-Origin': '*'}

    @swagger.operation(
        notes="All these parameters should be in one json object in the body. If there is no data available, just leave"
              " the field blank but make sure the key is still included.",
        responseClass=LocMod.__name__,
        nickname="update",
        parameters=[
            {
                "name": "location",
                "description": "Nested json in body. Be sure to read the model about what is required. HqAddr is not!",
                "required": True,
                "dataType": LocMod.__name__,
                "paramType": "body"
            }
        ],
        responseMesssage=[
            {
                "code": 201,
                "message": "Updated the location!"
            },
            {
                "code": 400,
                "message": "Some part of the body data was malformed!"
            },
            {
                "code": 404,
                "message": "No location with that id."
            }
        ]
    )
    def put(self, locId):
        """
            Update a Location
        """
        # First find the Location
        location = LocDoc.objects.get(id=locId)

        data = request.get_json()

        if 'name' in data and isinstance(data['name'], unicode):
            location.update(name=data['name'])
        if 'address' in data:
            newAddr = AddrDoc.from_data(data=data['address'])
            location.update(address=newAddr)
        if 'hqAddress' in data:
            newHqAddr = AddrDoc.from_data(data=data['hqAddress'])
            location.update(address=newHqAddr)
        if 'website' in data and isinstance(data['website'], unicode):
            location.update(website=data['website'])
        if 'phone' in data and isinstance(data['phone'], unicode):
            location.update(phone=data['phone'])
        if 'locationType' in data and isinstance(data['locationType'], unicode):
            location.update(locationType=data['locationType'])
        if 'coverages' in data and isinstance(data['coverages'], list):
            location.update(coverages=data['coverages'])
        if 'services' in data and isinstance(data['services'], list):
            location.update(services=data['services'])
        if 'tags' in data and isinstance(data['tags'], list):
            location.update(tags=data['tags'])
        if 'comments' in data and isinstance(data['comments'], unicode):
            location.update(comments=data['comments'])

        # Will eventually do update logs/diffs

        stathat.count('location_put: ' + str(location.id), 1)
        return location.to_json(), 201, {'Access-Control-Allow-Origin': '*'}

    @swagger.operation(
        notes="Delete a location",
        nickname="delete",
        responseMesssage=[
            {
                "code": 204,
                "message": "Location deleted!"
            },
            {
                "code": 400,
                "message": "Some part of the body data was malformed!"
            },
            {
                "code": 404,
                "message": "No location with that id."
            }
        ]
    )
    def delete(self, locId):
        """
            Delete a Location
        """
        location = LocDoc.objects.get(id=locId)
        location.delete()
        stathat.count('location_delete ' + str(location.id), 1)
        return '', 204  # No Content Return

    def options(self, locId):
        pass


class LocationList(Resource):
    """
        Represents all of the Locations as a set
        Can either get all or add a new Location to the set
    """

    def __init__(self):
        super(LocationList, self).__init__()
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

    @swagger.operation(
        responseClass=LocMod.__name__,
        nickname="query all locations",
        parameters=[
            {
                "name": "name",
                "description": "",
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "lat",
                "description": " Co-req: lng, rangeMeters",
                "required": False,
                "dataType": "float",
                "paramType": "query"
            },
            {
                "name": "lng",
                "description": " Co-req: lat, rangeMeters",
                "required": False,
                "dataType": "float",
                "paramType": "query"
            },
            {
                "name": "rangeMeters",
                "description": " Co-req: lat, lng",
                "required": False,
                "dataType": "float",
                "paramType": "query"
            },
            {
                "name": "website",
                "description": "",
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "phone",
                "description": "",
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "email",
                "description": " Valid email format.",
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "locationType",
                "description": "",
                "required": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "coverage",
                "description": " Choices=['International', 'National', 'Regional', 'State', 'Local']",
                "required": False,
                "allowMultiple": True,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "services",
                "description": "",
                "required": False,
                "allowMultiple": True,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "tags",
                "description": "",
                "required": False,
                "allowMultiple": True,
                "dataType": "string",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Successful request, check the response"
            },
            {
                "code": 400,
                "message": "One of your parameters was probably of an incorrect type."
            }
        ]
    )
    def get(self):
        """
            Query all the locations
        """
        # Defaults: Get all
        args = self.parser.parse_args()

        #  Grabs keys out of the args that we want to query by
        # Will do dynamic later
        # I think it will entail a custom QuerySet

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
                elif key == 'coverages':
                    for coverage in args[key]:
                        locations = locations.filter(coverage__in=coverage.capitalize())
                elif key == 'services':
                    for service in args[key]:
                        locations = locations.filter(services__in=service.capitalize()())
                elif key == 'tags':
                    for tag in args[key]:
                        locations = locations.filter(tags__in=tag.lower())

        # Do a range search if there
        if args['rangeMeters'] != 0:
            # In lng / lat coordinates
            locations = locations.filter(address__latLng__near=[args['lng'], args['lat']],
                                         address__latLng__max_distance=args['rangeMeters'])

        stathat.count('location_get_all', 1)
        return locations.to_json(), 200, {'Access-Control-Allow-Origin': '*'}

    @swagger.operation(
        notes="All these parameters should be in one json object in the body. If there is no data available, just leave"
              " the field blank but make sure the key is still included.",
        responseClass=LocMod.__name__,
        nickname="create",
        parameters=[
            {
                "name": "location",
                "description": "Nested json in body. Be sure to read the model about what is required. HqAddr is not!",
                "required": True,
                "dataType": LocMod.__name__,
                "paramType": "body"
            }
        ],
        responseMesssage=[
            {
                "code": 201,
                "message": "Created the location! Should be sent back in the response."
            },
            {
                "code": 400,
                "message": "Some part of the body data was malformed!"
            }
        ]
    )
    def post(self):
        """
            Add a Location
        """
        try:
            location = LocDoc.from_data(request.get_json(), validate=True)
        except (TypeError, KeyError) as ex:
            abort(400)

        location.save()

        stathat.count('location_post', 1)
        return location.to_json(), 201, {'Access-Control-Allow-Origin': '*'}

    def options(self, locId):
        pass
