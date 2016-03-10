__author__ = 'austin'

from mongoengine import QuerySet


class LocationQuery(QuerySet):
    def from_json(self, json_data):
        return super(LocationQuery, self).from_json(json_data)