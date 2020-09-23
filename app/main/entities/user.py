from . import db, login_manager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    photoUrl = db.Column(db.String(256))
    emailVerified = db.Column(db.Boolean)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
