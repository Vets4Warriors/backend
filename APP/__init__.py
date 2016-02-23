"""

"""
from flask import Flask
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

from APP import routes

if __name__ == '__main__':
    app.run(port=5000)
