"""
    Initializes the app
    Some people use another file for this. Call it app.py they say. Nah.
"""
import os
from flask import Flask
from flask_restful import Api
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

basePath = os.environ['VETS_BASE']
apiVersion = '1'

print basePath
print apiVersion

# Generates beautiful swagger documents.
# Available @ /api/spec.html
api = swagger.docs(Api(app),
                   description="The API for the Vets4Warriors online interface!",
                   basePath='http://localhost:8000',
                   apiVersion=apiVersion)

# Loads our routes
from app import routes

if __name__ == '__main__':
    app.run(port=5000)
