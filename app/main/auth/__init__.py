import os
from .. import settings
from ..entities import db
from ..entities.user import OAuth

from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user


twitter_blueprint = make_twitter_blueprint(
    api_key=os.getenv('TWITTER_APP_KEY', settings.TWITTER_APP_KEY),
    api_secret=os.getenv('TWITTER_APP_SECRET', settings.TWITTER_APP_SECRET),
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user, user_required=False))

github_blueprint = make_github_blueprint(
    client_id=os.getenv('GITHUB_CLIENT_ID', settings.GITHUB_CLIENT_ID),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET', settings.GITHUB_CLIENT_SECRET),
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user, user_required=False))

google_blueprint = make_google_blueprint(
    client_id=os.getenv('GOOGLE_CLIENT_ID', settings.GOOGLE_CLIENT_ID),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', settings.GOOGLE_CLIENT_SECRET),
    storage=SQLAlchemyStorage(
        OAuth, db.session, user=current_user, user_required=False),
    offline=True)

facebook_blueprint = make_facebook_blueprint(
    client_id=os.getenv('FACEBOOK_CLIENT_ID', settings.FACEBOOK_CLIENT_ID),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET', settings.FACEBOOK_CLIENT_SECRET),
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user, user_required=False))


def set_up_auth(flask_app):
    flask_app.register_blueprint(
        twitter_blueprint, url_prefix="/twitter_login")
    flask_app.register_blueprint(github_blueprint, url_prefix="/github_login")
    flask_app.register_blueprint(google_blueprint, url_prefix="/google_login")
    flask_app.register_blueprint(
        facebook_blueprint, url_prefix="/facebook_login")
