from APP import db

from datetime import datetime


class Rating(db.EmbeddedDocument):
    """
        Ratings can get more complex. For now
    """
    value = db.IntField(min_value=0, max_value=5)
    user = db.StringField(max_length=255)
    comment = db.StringField(required=False)


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


class Location(db.Document):
    """
        Represents a Veteran Aid Location
    """
    name = db.StringField(max_length=255)
    address = db.EmbeddedDocumentField(Address)
    hqLocation = db.EmbeddedDocumentField(Address)
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

    def get_rating(self):
        """
            Gets the average rating from all ratings
        :return: float
        """
        sum = 0
        for r in self.ratings:
            sum += r.value

        return sum / len(self.ratings)
