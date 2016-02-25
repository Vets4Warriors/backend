"""
    Defines the Schemas for each resource in MongoEngine Terms
"""

import json
from datetime import datetime

from app import db


class Rating(db.EmbeddedDocument):
    """
        Ratings can get more complex. For now
    """
    value = db.IntField(min_value=0, max_value=5)
    user = db.StringField(max_length=255)
    comment = db.StringField(required=False)

    @staticmethod
    def from_data(data, validate=False):
        """

        :param data:
        :return: Rating
        """
        comment = None
        if 'comment' in data:
            comment = data['comment']

        rating = Rating(
            value=data['value'],
            user=data['user'],
            comment=comment
        )

        if validate:
            rating.validate()

        return rating


class Address(db.EmbeddedDocument):
    """
        A basic address representation
    """
    address1 = db.StringField(max_length=255)
    address2 = db.StringField(max_length=255)
    city = db.StringField(max_length=255)
    state = db.StringField(max_length=255)
    country = db.StringField(max_length=255)
    zipcode = db.StringField(max_length=10)
    latLng = db.PointField()

    @staticmethod
    def from_data(data, validate=False):
        """
        :raises: TypeError
        :raises: KeyError
        :param data:
        :return: Address
        """
        address = Address(
                address1=data['address1'],
                address2=data['address2'],
                city=data['city'],
                state=data['state'],
                country=data['country'],
                zipcode=data['zipcode'],
                latLng=data['latLng']
        )
        if validate:
            address.validate()

        return address


class Location(db.Document):
    """
        Represents a Veteran Aid Location
    """
    name = db.StringField(max_length=255, unique=True)
    address = db.EmbeddedDocumentField(Address)
    hqAddress = db.EmbeddedDocumentField(Address)
    website = db.URLField()
    phone = db.StringField(max_length=11)
    email = db.EmailField()
    ratings = db.EmbeddedDocumentListField(Rating, default=[])
    locationType = db.StringField(max_length=255)
    coverage = db.ListField(db.StringField(choices=['International', 'National', 'Regional', 'State', 'Local']))
    # Will probably also want to limit the choices here eventually?
    services = db.ListField(db.StringField(max_length=255))

    tags = db.ListField(db.StringField(max_length=255))
    # Eventually we can make this a threaded list like a forum
    comments = db.StringField()

    addedBy = db.StringField()
    addedDate = db.DateTimeField(default=datetime.utcnow)

    def to_json(self):
        locJson = json.loads(super(Location, self).to_json())
        locJson['rating'] = self.get_rating()
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
        if 'hqAddress' in data:
            hqAddress = Address.from_data(data['hqAddress'], validate=validate)

        location = Location(
            name=data['name'],
            address=address,
            hqAddress=hqAddress,
            website=data['website'],
            phone=data['phone'],
            email=data['email'],
            locationType=data['locationType'],
            coverage=data['coverage'],
            services=data['services'],
            tags=data['tags'],
            comments=data['comments'],
            addedBy=data['user']
        )
        if validate:
            location.validate()

        return location

