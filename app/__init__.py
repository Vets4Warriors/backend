"""
    Initializes the app
    Some people use another file for this. Call it app.py they say. Nah.
"""
import os
from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors
from flask_restful_swagger import swagger
from flask_mongoengine import MongoEngine
from flask_stathat import StatHat

app = Flask(__name__)

app.debug = os.environ['VETS_ENV'] == 'DEV'
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017,
    'db': 'vets'
}
app.config['STATHAT_EZ_KEY'] = 'o3OaE05mySW3g9RH'

db = MongoEngine(app)
stathat = StatHat(app)

apiVersion = '1.0'
apiServer = os.environ['VETS_SERVER']

apiSpecUrl = '/spec'

# Generates beautiful swagger documents.
# Available @ /api/spec.html
api = swagger.docs(Api(app),
                   description="The API for the Vets4Warriors online interface!",
                   basePath='http://' + apiServer,
                   api_spec_url=apiSpecUrl,
                   apiVersion=apiVersion)

api.decorators = [cors.crossdomain(origin='*', headers=['Content-Type'])]

# Loads our routes
from app import routes

if __name__ == '__main__':
    app.run(port=5000)
