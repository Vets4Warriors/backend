__author__ = 'austin'

import json
from datetime import datetime
from flask import abort
from flask_restful_swagger import swagger as sg

from app import db
from app.documents.Address import Address, AddressModel
from app.documents.Rating import Rating, RatingModel
from app.querySets import Location as LocQuery


@sg.model
@sg.nested(address=AddressModel.__name__, hqAddress=AddressModel.__name__, ratings=RatingModel.__name__)
class LocationModel:
    resource_fields = {
        'name': sg.fields.String,
        'address': sg.fields.Nested(AddressModel.resource_fields),
        'hqAddress': sg.fields.Nested(AddressModel.resource_fields, default=None, attribute="Not required."),
        'website': sg.fields.Url,
        'phone': sg.fields.String,
        'email': sg.fields.String,
        'ratings': sg.fields.Nested(RatingModel.resource_fields),
        'rating': sg.fields.Float(attribute="Only in response."),
        'locationType': sg.fields.String,
        'coverages': sg.fields.List(sg.fields.String, attribute=['International', 'National', 'Regional',
                                                                'State', 'Local', '']),
        'services': sg.fields.List(sg.fields.String),
        'tags': sg.fields.List(sg.fields.String),
        'comments': sg.fields.String,
        'addedBy': sg.fields.String,
        'addedOn': sg.fields.DateTime
    }

    required = ['name', 'website', 'locationType', 'coverages', 'services', 'addedBy']


class Location(db.Document):
    """
        Represents a Veteran Aid Location
    """

    # meta = {
    #     'queryset_class': LocQuery
    # }

    name = db.StringField(max_length=255, unique=True, required=True)
    address = db.EmbeddedDocumentField(Address)
    hqAddress = db.EmbeddedDocumentField(Address)
    website = db.URLField(default=None)
    phone = db.StringField(max_length=15)
    email = db.EmailField(default=None)
    ratings = db.EmbeddedDocumentListField(Rating, default=[])
    locationType = db.StringField(max_length=255, required=True)
    coverages = db.ListField(db.StringField(choices=['International', 'National', 'Regional', 'State', 'Local', ''],
                                            default=[]))
    # Will probably also want to limit the choices here eventually?
    services = db.ListField(db.StringField(max_length=255), default=[])

    tags = db.ListField(db.StringField(max_length=255), default=[])
    # Eventually we can make this a threaded list like a forum
    comments = db.StringField()

    addedBy = db.StringField(required=True)
    addedOn = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        locJson = json.loads(super(Location, self).to_json())
        locJson['rating'] = self.get_rating()
        # Should we return a formatted address here on our end so clients don't have to deal?
        return json.dumps(locJson)

    def get_rating(self):
        """
            Gets the average rating from all ratings
        :return: float
        """
        sum = 0
        for r in self.ratings:
            sum += r.value

        numRatings = len(self.ratings)

        return sum / numRatings if numRatings != 0 else 0

    @staticmethod
    def from_data(data, validate=False):
        """
            Builds a LocDoc from a json dictionary
        :param data: dict
        :param validate: bool
        :return: app.documents.Location
        """
        # Could get more intense about validation/formatting data
        # Will see if the users mess it up enough / harder on the front end

        phone = None
        if 'phone' in data and isinstance(data['phone'], unicode) and data['phone'] != '':
            phone = data['phone']

        email = None
        if 'email' in data and isinstance(data['email'], unicode) and data['email'] != '':
            email = data['email']

        website = None
        if 'website' in data and isinstance(data['website'], unicode) and data['website'] != '':
            website = data['website']

        comments = None
        if 'comments' in data and isinstance(data['comments'], unicode):
            comments = data['comments']

        locationType = None
        if 'locationType' in data and isinstance(data['locationType'], unicode):
            locationType = data['locationType']

        address = None
        if 'address' in data and data['address'] is not None:
            address = Address.from_data(data['address'], validate=validate)

        hqAddress = None
        if 'hqAddress' in data and data['hqAddress'] is not None:
            hqAddress = Address.from_data(data['hqAddress'], validate=validate)

        # Process all the tags to be lowercase but services to be capitalized
        tags = []
        if 'tags' in data and isinstance(data['tags'], list):
            for i in range(0, len(data['tags'])):
                if isinstance(data['tags'][i], unicode):
                    tags.append(data['tags'][i].strip().lower())

        services = []
        if 'services' in data and isinstance(data['services'], list):
            for i in range(0, len(data['services'])):
                if isinstance(data['services'][i], unicode):
                    services.append(data['services'][i].strip().capitalize())

        # Required
        if 'name' not in data or not isinstance(data['name'], unicode):
            abort(400)

        if 'addedBy' not in data or not isinstance(data['addedBy'], unicode):
            abort(400)

        location = Location(
            name=data['name'],
            address=address,
            hqAddress=hqAddress,
            website=website,
            phone=phone,
            email=email,
            locationType=locationType,
            coverages=data['coverages'],
            services=services,
            tags=tags,
            comments=comments,
            addedBy=data['addedBy']
        )
        if validate:
            location.validate()

        return location
