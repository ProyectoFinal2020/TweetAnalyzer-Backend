import os

from . import settings


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', settings.SECRET_KEY)
    ERROR_404_HELP = settings.RESTPLUS_ERROR_404_HELP
    RESTPLUS_MASK_SWAGGER = settings.RESTPLUS_MASK_SWAGGER
    RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE
    SWAGGER_UI_DOC_EXPANSION = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    SQLALCHEMY_TRACK_MODIFICATIONS = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    SQLALCHEMY_ECHO = settings.SQLALCHEMY_ECHO
    RESTX_INCLUDE_ALL_MODELS = True
    RESTX_MASK_HEADER = 'X-Fields'


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    # ?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/DB_TWEETANALYZER"
    DEBUG = True


class ProductionConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = "postgres://fikupfxgrbamgc:eb155597fc40aedb0638ee3c7f35660f61097fc5fbed266642833be8c6f5cec1@ec2-52-207-124-89.compute-1.amazonaws.com:5432/df2otjl8jg5ja6"
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
