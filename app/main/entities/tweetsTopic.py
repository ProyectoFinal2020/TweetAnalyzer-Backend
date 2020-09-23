from . import db
from .user import User


class TweetsTopic(db.Model):
    __tablename__ = "tweets_topics"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    topic_title = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    language = db.Column(db.String(2))
