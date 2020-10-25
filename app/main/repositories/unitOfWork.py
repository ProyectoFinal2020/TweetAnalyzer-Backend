from .emotionLexiconRepository import EmotionLexiconRepository
from .userStreamingTweetsRepository import UserStreamingTweetsRepository
from .tweetsTopicRepository import TweetsTopicRepository
from .tweetWithScoresRepository import TweetWithScoresRepository
from .tweetWithEmotionsRepository import TweetWithEmotionsRepository
from .reportRepository import ReportRepository
from ..utils.singleton import Singleton


class UnitOfWork(metaclass=Singleton):
    def __init__(self):
        self.emotionLexiconRepository = EmotionLexiconRepository()
        self.userStreamingTweetsRepository = UserStreamingTweetsRepository()
        self.tweetsTopicRepository = TweetsTopicRepository()
        self.reportRepository = ReportRepository()
        self.tweetWithScoresRepository = TweetWithScoresRepository()
        self.tweetWithEmotionsRepository = TweetWithEmotionsRepository()

    def getEmotionLexiconRepository(self):
        return self.emotionLexiconRepository

    def getUserStreamingTweetsRepository(self):
        return self.userStreamingTweetsRepository

    def getTweetsTopicRepository(self):
        return self.tweetsTopicRepository

    def getReportRepository(self):
        return self.reportRepository

    def getTweetWithScoresRepository(self):
        return self.tweetWithScoresRepository

    def getTweetWithEmotionsRepository(self):
        return self.tweetWithEmotionsRepository


unitOfWork = UnitOfWork()
