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

    def getEmotions(self, word: str, language: Language):
        return self.getEmotionsByLanguage[language](word)

    def _getEmotionsEnglish(self, word: str):
        return EmotionLexicon.query.filter(EmotionLexicon.english == word).one_or_none()

    def _getEmotionsSpanish(self, word: str):
        return EmotionLexicon.query.filter(EmotionLexicon.spanish == word).first()
