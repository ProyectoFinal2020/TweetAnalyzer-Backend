from . import db


class Tweet(db.Model):
    id = db.Column(db.String(25), primary_key=True, unique=True)
    username = db.Column(db.String(100))
    to = db.Column(db.String(100), nullable=True)
    text = db.Column(db.String(3000))
    retweets = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    replies = db.Column(db.Integer)
    permalink = db.Column(db.String(150))
    author_id = db.Column(db.BigInteger)
    date = db.Column(db.DateTime)
    formatted_date = db.Column(db.String(40))
    hashtags = db.Column(db.String(1000))
    mentions = db.Column(db.String(1000))
    geo = db.Column(db.String(40))
    urls = db.Column(db.String(2048))
