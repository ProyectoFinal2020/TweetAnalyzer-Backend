from . import db
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship


class TweetWithEmotions(db.Model):
    __tablename__ = "tweets_with_emotions"
    id = db.Column(db.String(25), primary_key=True)
    topic_title = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    userStreamingTweets = relationship("UserStreamingTweets", foreign_keys=[id, topic_title, user_id],
                                       back_populates='tweetWithEmotions')
    positive = db.Column(db.Float)
    negative = db.Column(db.Float)
    anger = db.Column(db.Integer)
    anticipation = db.Column(db.Integer)
    disgust = db.Column(db.Integer)
    fear = db.Column(db.Integer)
    joy = db.Column(db.Integer)
    sadness = db.Column(db.Integer)
    surprise = db.Column(db.Integer)
    trust = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id', 'user_id', 'topic_title'],
            ['tweets.id', 'tweets.user_id',
                'tweets.topic_title'],
            ondelete="CASCADE"
        ),
    )
