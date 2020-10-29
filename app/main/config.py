import os
from . import settings

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    ERROR_404_HELP =  settings.RESTPLUS_ERROR_404_HELP
    RESTPLUS_MASK_SWAGGER =  settings.RESTPLUS_MASK_SWAGGER
    RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE
    SWAGGER_UI_DOC_EXPANSION =  settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    RESTX_INCLUDE_ALL_MODELS = True
    RESTX_MASK_HEADER = 'X-Fields'
    SQLALCHEMY_ECHO =  settings.SQLALCHEMY_ECHO
    SQLALCHEMY_TRACK_MODIFICATIONS = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_LOCAL_DATABASE_URI')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
