from ..entities.userStreamingTweets import UserStreamingTweets
from .baseRepository import BaseRepository
from flask_login import current_user


class UserStreamingTweetsRepository(BaseRepository[UserStreamingTweets]):
    def __init__(self):
        super().__init__(UserStreamingTweets)

    def getPaginatedByTopicTitle(self, per_page, page, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).paginate(per_page=per_page, page=page)
