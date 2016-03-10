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

from config import ProductionConfig, DevelopmentConfig

app = Flask(__name__)

# Default to production mode
if os.environ.get('VETS_ENV', 'prod') == 'dev':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)



db = MongoEngine(app)
stathat = StatHat(app)

apiVersion = '1.0'
apiServerName = app.config['SERVER']
apiSpecUrl = '/spec'

# Generates beautiful swagger documents.
# Available @ /api/spec.html
api = swagger.docs(Api(app),
                   description="The API for the Vets4Warriors online interface!",
                   basePath='http://' + apiServerName,
                   api_spec_url=apiSpecUrl,
                   apiVersion=apiVersion)

api.decorators = [cors.crossdomain(origin='*', headers=['Content-Type'])]

# Loads our routes
from app import routes


if __name__ == '__main__':
    app.run(port=5000)
