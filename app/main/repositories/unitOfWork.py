from .emotionLexiconRepository import EmotionLexiconRepository
from .userStreamingTweetsRepository import UserStreamingTweetsRepository
from ..utils.singleton import Singleton


class UnitOfWork(metaclass=Singleton):
    def __init__(self):
        self.emotionLexiconRepository = EmotionLexiconRepository()
        self.userStreamingTweetsRepository = UserStreamingTweetsRepository()

    def getEmotionLexiconRepository(self):
        return self.emotionLexiconRepository

    def getUserStreamingTweetsRepository(self):
        return self.userStreamingTweetsRepository


unitOfWork = UnitOfWork()
