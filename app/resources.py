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
    @swagger.operation(
        notes="Rate a location",
        responseClass=LocDoc.__name__,
        nickname="rate",
        parameters=[
            {
                "name": "value",
                "description": "The value. From [0,5]",
                "required": True,
                "dataType": "json",
                "paramType": "body"
            },
            {
                "name": "user",
                "description": "Who is rating",
                "required": True,
                "dataType": "json",
                "paramType": "body"
            },
            {
                "name": "comment",
                "description": "Any extra comments",
                "required": False,
                "dataType": "json",
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
        return location.to_json(), 201


class Location(Resource):
    """
        The individual Location
    """
    @swagger.operation(
        responseClass=LocDoc.__name__,
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
        return location.to_json(), 200

    @swagger.operation(
        responseClass=LocDoc.__name__,
        nickname="update",
        parameters=[
            {
                "name": "name",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "website",
                "description": "In body. Must follow http:// full format",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "phone",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "email",
                "description": "In body. Must be a valid email address.",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "locationType",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "coverage",
                "description": "In body. choices=['International', 'National', 'Regional', 'State', 'Local']",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "services",
                "description": "In body.",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "tags",
                "description": "In body.",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "comments",
                "description": "In body.",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "user",
                "description": "In body. The person who adds this!",
                "required": True,
                "dataType": "string",
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
        responseClass="List of: " + LocDoc.__name__,
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
                elif key == 'coverage':
                    locations = locations.filter(coverage__in=args[key])
                elif key == 'services':
                    locations = locations.filter(services__in=args[key])
                elif key == 'tags':
                    locations = locations.filter(tags__in=args[key])

        # Do a range search if there
        if args['rangeMeters'] != 0:
            locations = locations.filter(address__latLng__near=[args['lat'], args['lng']],
                                         address__latLng__max_distance=args['rangeMeters'])

        stathat.count('location_get_all', 1)
        return locations.to_json(), 200

    @swagger.operation(
        responseClass=LocDoc.__name__,
        nickname="create",
        parameters=[
            {
                "name": "name",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "website",
                "description": "In body. Must follow http:// full format",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "phone",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "email",
                "description": "In body. Must be a valid email address.",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "locationType",
                "description": "In body",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "coverage",
                "description": "In body. choices=['International', 'National', 'Regional', 'State', 'Local']",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "services",
                "description": "In body.",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "tags",
                "description": "In body.",
                "required": True,
                "dataType": "list of strings",
                "paramType": "body"
            },
            {
                "name": "comments",
                "description": "In body.",
                "required": True,
                "dataType": "string",
                "paramType": "body"
            },
            {
                "name": "user",
                "description": "In body. The person who adds this!",
                "required": True,
                "dataType": "string",
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

        location.get_rating()
        location.to_json()
        location.save()

        stathat.count('location_post', 1)
        return location.to_json(), 201
