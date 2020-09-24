from . import db
from .user import User
from sqlalchemy.orm import relationship


class UserStreamingTweets(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.String(25), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    user = db.relationship(User)
    topic_title = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.Unicode(100, collation='utf8mb4_unicode_ci'))
    username = db.Column(db.String(100))
    to = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Unicode(3000, collation='utf8mb4_unicode_ci'))
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
    img_url = db.Column(db.String(2048))
    polarity = db.Column(db.Float)
    subjectivity = db.Column(db.Float)
    tweetWithScores = relationship(
        "TweetWithScores", back_populates='userStreamingTweets')
    tweetWithEmotions = relationship(
        "TweetWithEmotions", back_populates='userStreamingTweets')
