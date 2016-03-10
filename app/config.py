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
    SERVER = 'localhost:8000'


class ProductionConfig(Config):
    SERVER = 'vets.cawleyedwards.com/api'
    SERVER_NAME = 'vets.cawleyedwards.com/api'


class DevelopmentConfig(Config):
    DEBUG = True