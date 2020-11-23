from ..entities.tweetWithScores import TweetWithScores
from ..entities.userStreamingTweets import UserStreamingTweets
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetWithScoresRepository(BaseRepository[TweetWithScores]):
    def __init__(self):
        super().__init__(TweetWithScores)

    def getAllTweetsWithScoresFilteredByThreshold(self, topicTitle, reportId, algorithm, threshold, all=False):
        tweets = self.model.query. \
            filter(TweetWithScores.topic_title == topicTitle, TweetWithScores.report_id == reportId,
                   TweetWithScores.user_id == current_user.id, getattr(TweetWithScores, algorithm) >= threshold)
        if all:
            return tweets.all()
        return tweets

    def _getTweetsWithScores(self, topicTitle, reportId):
        return self.model.query.filter_by(user_id=current_user.id, topic_title=topicTitle, report_id=reportId)

    def getTweetsWithScoresOrderedByText(self, topicTitle, reportId, sortDesc, per_page, page):
        return self._getTweetsWithScores(topicTitle, reportId) \
            .join(UserStreamingTweets) \
            .order_by(UserStreamingTweets.text.desc() if sortDesc else UserStreamingTweets.text)\
            .paginate(per_page=per_page, page=page)

    def getTweetsWithScoresOrderedByProp(self, topicTitle, reportId, prop, sortDesc, per_page, page):
        return self._getTweetsWithScores(topicTitle, reportId)\
            .order_by(getattr(TweetWithScores, prop).desc() if sortDesc else getattr(TweetWithScores, prop))\
            .paginate(per_page=per_page, page=page)

    def getAllTweetsWithScores(self, topicTitle, reportId):
        return self._getTweetsWithScores(topicTitle, reportId).all()
