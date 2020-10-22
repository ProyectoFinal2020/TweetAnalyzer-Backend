from .emotionLexiconRepository import EmotionLexiconRepository
from .userStreamingTweetsRepository import UserStreamingTweetsRepository
from .tweetsTopicRepository import TweetsTopicRepository
from ..utils.singleton import Singleton


class UnitOfWork(metaclass=Singleton):
    def __init__(self):
        self.emotionLexiconRepository = EmotionLexiconRepository()
        self.userStreamingTweetsRepository = UserStreamingTweetsRepository()
        self.tweetsTopicRepository = TweetsTopicRepository()

    def getEmotionLexiconRepository(self):
        return self.emotionLexiconRepository

    def getUserStreamingTweetsRepository(self):
        return self.userStreamingTweetsRepository

    def getTweetsTopicRepository(self):
        return self.tweetsTopicRepository


unitOfWork = UnitOfWork()
