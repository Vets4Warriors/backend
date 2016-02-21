"""

"""
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_stathat import StatHat

from flask_mongorest.views import ResourceView
from flask_mongorest import methods

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017,
    'db': 'vets'
}

app.config['STATHAT_EZ_KEY'] = 'o3OaE05mySW3g9RH'

db = MongoEngine(app)
api = MongoRest(app)
stathat = StatHat(app)

from APP import resources as res

@api.register(name="locations", url='/locations/')
class LocationView(ResourceView):
    resource = res.LocationResource
    methods = [methods.Create, methods.Update, methods.Delete, methods.Fetch, methods.List]


if __name__ == '__main__':
    app.run(port=5000)
