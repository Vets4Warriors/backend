__author__ = 'austin'

import json
from datetime import datetime
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

    required = ['name', 'address', 'website', 'phone', 'email', 'locationType', 'coverages', 'services', 'tags',
                'comments', 'addedBy']


class Location(db.Document):
    """
        Represents a Veteran Aid Location
    """

    # meta = {
    #     'queryset_class': LocQuery
    # }

    name = db.StringField(max_length=255, unique=True)
    address = db.EmbeddedDocumentField(Address)
    hqAddress = db.EmbeddedDocumentField(Address)
    website = db.URLField()
    phone = db.StringField(max_length=15)
    email = db.EmailField()
    ratings = db.EmbeddedDocumentListField(Rating, default=[])
    locationType = db.StringField(max_length=255)
    coverages = db.ListField(db.StringField(choices=['International', 'National', 'Regional', 'State', 'Local', '']))
    # Will probably also want to limit the choices here eventually?
    services = db.ListField(db.StringField(max_length=255))

    tags = db.ListField(db.StringField(max_length=255))
    # Eventually we can make this a threaded list like a forum
    comments = db.StringField()

    addedBy = db.StringField()
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
        :param jsonData: dict
        :return: app.documents.Location
        """
        # Could get more intense about validation/formatting data
        # Will see if the users mess it up enough / harder on the front end
        address = Address.from_data(data['address'], validate=validate)

        # Not required
        hqAddress = None
        if 'hqAddress' in data and data['hqAddress'] is not None:
            hqAddress = Address.from_data(data['hqAddress'], validate=validate)

        # Process all the tags to be lowercase but services to be capitalized
        for i in range(0, len(data['tags'])):
            data['tags'][i] = data['tags'][i].lower()

        for i in range(0, len(data['services'])):
            data['services'][i] = data['services'][i].capitalize()

        location = Location(
            name=data['name'],
            address=address,
            hqAddress=hqAddress,
            website=data['website'],
            phone=data['phone'],
            email=data['email'],
            locationType=data['locationType'],
            coverages=data['coverages'],
            services=data['services'],
            tags=data['tags'],
            comments=data['comments'],
            addedBy=data['addedBy']
        )
        if validate:
            location.validate()

        return location