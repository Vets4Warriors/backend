"""
    Initializes the app
    Some people use another file for this. Call it app.py they say. Nah.
"""
from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_mongoengine import MongoEngine
from flask_stathat import StatHat

app = Flask(__name__)

app.debug = True
app.config['MONGODB_SETTINGS'] = {
    'host': 'localhost',
    'port': 27017,
    'db': 'vets'
}
app.config['STATHAT_EZ_KEY'] = 'o3OaE05mySW3g9RH'

db = MongoEngine(app)
stathat = StatHat(app)
api = swagger.docs(Api(app), apiVersion='0.1')

# Loads our routes
from app import routes

if __name__ == '__main__':
    app.run(port=5000)
