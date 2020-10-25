from ..entities.tweetWithScores import TweetWithScores
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetWithScoresRepository(BaseRepository[TweetWithScores]):
    def __init__(self):
        super().__init__(TweetWithScores)

    def getTweetsWithScores(self, topicTitle, reportId, algorithm, threshold):
        return self.model.query. \
            filter(TweetWithScores.topic_title == topicTitle, TweetWithScores.report_id == reportId,
                   TweetWithScores.user_id == current_user.id, getattr(TweetWithScores, algorithm) >= threshold).all()