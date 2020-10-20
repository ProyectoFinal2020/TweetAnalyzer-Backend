from ...repositories.unitOfWork import unitOfWork
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user

class SentimentAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()

    def getSentiments(self, topic_title):
        return self.userStreamingTweetsRepository.getByTopicTitle(topic_title)