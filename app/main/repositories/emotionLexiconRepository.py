from ..entities.emotionLexicon import EmotionLexicon
from ..models.language import Language
from .baseRepository import BaseRepository


class EmotionLexiconRepository(BaseRepository[EmotionLexicon]):
    def __init__(self):
        super().__init__(EmotionLexicon)
        self.getEmotionsByLanguage = {
            Language.ENGLISH: self._getEmotionsEnglish,
            Language.SPANISH: self._getEmotionsSpanish,
        }
        self.getEmotionsByLanguageAndTopic = {
            Language.ENGLISH: self._getEmotionsOfATopicInEnglish,
            Language.SPANISH: self._getEmotionsOfATopicInSpanish,
        }

    def getEmotions(self, word: str, language: Language):
        return self.getEmotionsByLanguage[language](word)

    def _getEmotionsEnglish(self, word: str):
        return EmotionLexicon.query.filter(EmotionLexicon.english == word).one_or_none()

    def _getEmotionsSpanish(self, word: str):
        return EmotionLexicon.query.filter(EmotionLexicon.spanish == word).first()

    def getEmotionsOfATopic(self, topic: [str], language: Language):
        return self.getEmotionsByLanguageAndTopic[language](topic)

    def _getEmotionsOfATopicInEnglish(self, topic:[str]):
        return EmotionLexicon.query.filter(EmotionLexicon.english.in_(topic)).all()

    def _getEmotionsOfATopicInSpanish(self, topic:[str]):
        return EmotionLexicon.query.filter(EmotionLexicon.spanish.in_(topic)).all()