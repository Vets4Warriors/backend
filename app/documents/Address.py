"""
    Defines the Schemas for each resource in MongoEngine Terms
"""


from flask_restful_swagger import swagger as sg
from app import db


@sg.model
class AddressModel:
    resource_fields = {
        'address1': sg.fields.String,
        'address2': sg.fields.String,
        'city': sg.fields.String,
        'state': sg.fields.String,
        'country': sg.fields.String,
        'zipcode': sg.fields.String,
        'latLng': sg.fields.List(sg.fields.Float),
    }

    # They're all required
    required = resource_fields.keys()


class Address(db.EmbeddedDocument):
    """
        A basic address representation

        KEY POINT: latLng is stored ad [lng, lat] in mongodb
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
        Allows for None address1, address2, and zip.
        Will need to account for this in the frontend.

        :raises: TypeError
        :raises: KeyError
        :param data:
        :return: Address
        """

        # Required
        # Check for a dict of {lat: , lng: } form and convert
        latLng = data['latLng']
        if type(data['latLng']) is dict:
            latLng = [latLng['lng'], latLng['lat']]

        zipcode = None
        if 'zipcode' in data:
            zipcode = data['zipcode']

        address1 = None
        if 'address1' in data:
            address1 = data['address1']

        address2 = None
        if 'address2' in data:
            address2 = data['address2']

        address = Address(
                address1=address1,
                address2=data['address2'],
                city=data['city'],
                state=data['state'],
                country=data['country'],
                zipcode=zipcode,
                latLng=latLng
        )
        if validate:
            address.validate()

        return address


