from ..entities.tweetsTopic import TweetsTopic
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetsTopicRepository(BaseRepository[TweetsTopic]):
    def __init__(self):
        super().__init__(TweetsTopic)

    def getByTweetTopic(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).one_or_none()

    def getAllOrderedByTitle(self):
        return self.model.query.filter_by(user_id=current_user.id).order_by(TweetsTopic.topic_title).all()

    