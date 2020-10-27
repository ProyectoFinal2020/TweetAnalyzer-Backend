from ..entities.tweetWithEmotions import TweetWithEmotions
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetWithEmotionsRepository(BaseRepository[TweetWithEmotions]):
    def __init__(self):
        super().__init__(TweetWithEmotions)

    def getAllTweetsByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).all()
    
    def getTweetsByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id)

    def getPaginatedTweetsByTopicTitle(self, topicTitle, page, per_page):
        return self.model.query.filter_by(topic_title=topicTitle, user_id=current_user.id).paginate(per_page=per_page, page=page)
