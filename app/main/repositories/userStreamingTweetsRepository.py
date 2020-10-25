from ..entities.userStreamingTweets import UserStreamingTweets
from .baseRepository import BaseRepository
from flask_login import current_user


class UserStreamingTweetsRepository(BaseRepository[UserStreamingTweets]):
    def __init__(self):
        super().__init__(UserStreamingTweets)

    def getByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).all()
    
    def getPaginatedByTopicTitleInRange(self, per_page, page, topic_title, min_polarity, max_polarity):
        return self.model.query.filter(UserStreamingTweets.topic_title==topic_title, \
                UserStreamingTweets.user_id==current_user.id,\
                UserStreamingTweets.polarity>=min_polarity, \
                UserStreamingTweets.polarity<max_polarity) \
            .order_by(UserStreamingTweets.polarity.desc())\
            .paginate(per_page=per_page, page=page)

    def getPaginatedByTopicTitle(self, per_page, page, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).paginate(per_page=per_page, page=page)
