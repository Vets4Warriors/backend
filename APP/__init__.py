
#

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    'host': 'localhost',
    'port': 27017,
    'db': 'vets'
}

db = MongoEngine(app)
api = MongoRest(app)

# These are all the endpoints used by the
from APP import routes