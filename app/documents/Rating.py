

from datetime import datetime
from flask_restful_swagger import swagger as sg
from app import db


@sg.model
class RatingModel:
    """
        The swagger model
    """
    resource_fields = {
        'value': sg.fields.Integer,
        'user': sg.fields.String,
        'comment': sg.fields.String,
        'ratedOn': sg.fields.DateTime
    }

    required = ['value', 'user']


class Rating(db.EmbeddedDocument):
    """
        A rating from 1 to 5 with optional comment
    """
    value = db.IntField(min_value=1, max_value=5)
    user = db.StringField(max_length=255)
    comment = db.StringField(required=False)
    ratedOn = db.DateTimeField(default=datetime.utcnow)

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

