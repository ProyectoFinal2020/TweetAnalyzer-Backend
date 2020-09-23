from . import db
from .report import Report
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship


class TweetWithScores(db.Model):
    __tablename__ = "tweets_with_scores"
    id = db.Column(db.String(25), primary_key=True)
    topic_title = db.Column(db.String(100), primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey(
        Report.id, ondelete="CASCADE"), primary_key=True)
    report = db.relationship(Report)
    user_id = db.Column(db.Integer, primary_key=True)
    userStreamingTweets = relationship("UserStreamingTweets", foreign_keys=[id, topic_title, user_id],
                                       back_populates='tweetWithScores')
    bagOfWords = db.Column(db.Float())
    doc2vecGensim = db.Column(db.Float())
    doc2vecNSim = db.Column(db.Float())
    softCosine = db.Column(db.Float())
    tfIdfSim = db.Column(db.Float())
    word2vecGensim = db.Column(db.Float())
    wmd = db.Column(db.Float())
    jaccard = db.Column(db.Float())

    __table_args__ = (
        ForeignKeyConstraint(
            ['id', 'user_id', 'topic_title'],
            ['tweets.id', 'tweets.user_id',
                'tweets.topic_title'],
            ondelete="CASCADE"
        ),
    )
