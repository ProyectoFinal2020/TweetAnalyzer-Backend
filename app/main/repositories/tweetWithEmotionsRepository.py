from ..entities.tweetWithEmotions import TweetWithEmotions
from ..entities.tweetWithScores import TweetWithScores
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetWithEmotionsRepository(BaseRepository[TweetWithEmotions]):
    def __init__(self):
        super().__init__(TweetWithEmotions)

    def getTweetsByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id)

    def getAllTweetsByTopicTitle(self, topic_title):
        return self.model.query.filter_by(topic_title=topic_title, user_id=current_user.id).all()

    def getPaginatedTweetsByTopicTitle(self, topicTitle, page, per_page):
        return self.model.query.filter_by(topic_title=topicTitle, user_id=current_user.id)\
            .paginate(per_page=per_page, page=page)

    def getTweetsWithScoresAndEmotions(self, topicTitle, reportId, algorithm, threshold, per_page=0, page=0):
        tweets = self.model.query.join(TweetWithScores, TweetWithScores.id == TweetWithEmotions.id)\
            .filter(TweetWithScores.topic_title == topicTitle, TweetWithScores.report_id == reportId,
                    TweetWithScores.user_id == current_user.id, getattr(TweetWithScores, algorithm) >= threshold)
        if per_page and page:
            return tweets.paginate(per_page=per_page, page=page)
        return tweets
