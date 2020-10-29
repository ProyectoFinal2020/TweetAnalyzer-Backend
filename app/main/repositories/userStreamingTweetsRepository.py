from ..entities.userStreamingTweets import UserStreamingTweets
from ..entities.tweetWithScores import TweetWithScores
from .baseRepository import BaseRepository
from flask_login import current_user
from ..settings import MAX_POLARITY_VALUE

class UserStreamingTweetsRepository(BaseRepository[UserStreamingTweets]):
    def __init__(self):
        super().__init__(UserStreamingTweets)

    def getByCurrentUser(self):
        return self.model.query.filter_by(user_id=current_user.id)
    
    def getAllByCurrentUser(self):
        return self.model.query.filter_by(user_id=current_user.id).all()

    def getByCurrentUserAndId(self, id):
        return self.model.query.filter_by(id=id, user_id=current_user.id)

    def getByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id)

    def getAllByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).all()
    
    def getPaginatedByTopicTitleInRange(self, per_page, page, topic_title, min_polarity, max_polarity):
        return self.model.query.filter(UserStreamingTweets.topic_title==topic_title, \
                UserStreamingTweets.user_id==current_user.id,\
                UserStreamingTweets.polarity>=min_polarity, \
                UserStreamingTweets.polarity<=max_polarity if max_polarity==MAX_POLARITY_VALUE else UserStreamingTweets.polarity<max_polarity) \
            .order_by(UserStreamingTweets.polarity.desc())\
            .paginate(per_page=per_page, page=page)

    def getPaginatedByTopicTitle(self, per_page, page, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).paginate(per_page=per_page, page=page)

    def getPaginatedByPolarity(self, topic_title, min_polarity, max_polarity, reportId, algorithm, threshold, per_page, page):
        return self.model.query.filter(UserStreamingTweets.topic_title==topic_title, \
                UserStreamingTweets.user_id==current_user.id,\
                UserStreamingTweets.polarity>=min_polarity, \
                UserStreamingTweets.polarity<=max_polarity if max_polarity==MAX_POLARITY_VALUE else UserStreamingTweets.polarity<max_polarity) \
            .join(TweetWithScores) \
            .filter(TweetWithScores.report_id == reportId, getattr(TweetWithScores, algorithm) >= threshold) \
            .paginate(per_page=per_page, page=page) 