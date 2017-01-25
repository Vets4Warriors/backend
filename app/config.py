import os

class Config:
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': 'vets'
    }
    STATHAT_EZ_KEY = 'o3OaE05mySW3g9RH'
    SECRET_KEY = 'v4w2016stevens'
    SERVER = 'http://localhost:8000'


class ProductionConfig(Config):
    SERVER = 'https://vets.cawleyedwards.com/api'
    # SERVER_NAME = 'vets.cawleyedwards.com/api'


class LocalConfig(Config):
    DEBUG = True
    SERVER = 'http://localhost:' + os.getenv('VETS_PORT', '5000')


class DevelopmentConfig(Config):
    DEBUG = True
    SERVER = 'http://localhost'
