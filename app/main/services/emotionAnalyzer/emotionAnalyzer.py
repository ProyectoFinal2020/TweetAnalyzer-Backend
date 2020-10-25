import collections

from ...entities import db
from ...entities.tweetWithEmotions import TweetWithEmotions
from ...entities.tweetWithScores import TweetWithScores
from ...entities.tweetsTopic import TweetsTopic
from ...entities.userStreamingTweets import UserStreamingTweets
from ...models.language import Language
from ...models.emotion import Emotion
from ...models.tweetAndEmotion import TweetAndEmotion
from ...repositories.unitOfWork import unitOfWork
from ..common.data_preprocessing import tokenize_and_preprocess, lemmatize
from flask_login import current_user


def getLanguage(topicTitle):
    tweetsTopic = TweetsTopic.query.filter_by(
        topic_title=topicTitle, user_id=current_user.id).one_or_none()
    if tweetsTopic is not None:
        return tweetsTopic.language
    return None


class EmotionAnalyzer:
    def __init__(self):
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()
        self.tweetWithEmotionsRepository = unitOfWork.getTweetWithEmotionsRepository()
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.emotionLexiconRepository = unitOfWork.getEmotionLexiconRepository()
        self.emotions = ["anger", "anticipation", "disgust",
                         "fear", "joy", "sadness", "surprise", "trust"]
        self.languageDict = {"en": Language.ENGLISH, "es": Language.SPANISH}

    def _getEmotion(self, token, language):
        emotionLexicon = self.emotionLexiconRepository.getEmotions(
            token, language=self.languageDict[language])
        emotions = []
        if emotionLexicon:
            for attr, value in emotionLexicon.__dict__.items():
                if (attr in self.emotions) and (value == 1):
                    emotions.append(attr)
        return emotions

    def _getSentenceEmotion(self, sentence_tokenized_and_lemmatized, language):
        tokens_emotions = []
        for token in sentence_tokenized_and_lemmatized:
            tokens_emotions += self._getEmotion(token, language)
        return collections.Counter(tokens_emotions)

    def _clearData(self, topicTitle):
        self.tweetWithEmotionsRepository.getTweetsByTopicTitle(topicTitle=topicTitle).delete()

    def analyzeEmotions(self, topicTitle, reportId, algorithm, threshold=0):
        self._clearData(topicTitle)
        language = getLanguage(topicTitle)
        tweetsWithScores = self.tweetWithScoresRepository.getTweetsWithScores(
            topicTitle, reportId, algorithm, threshold)
        for tweetWithScores in tweetsWithScores:
            tweet = tweetWithScores.userStreamingTweets
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lematized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            emotions = self._getSentenceEmotion(tweet_lematized, language)
            tweetWithEmotions = TweetWithEmotions(
                id=tweet.id, user_id=current_user.id, topic_title=topicTitle)
            for emotion in emotions:
                setattr(tweetWithEmotions, emotion, emotions[emotion])
            db.session.merge(tweetWithEmotions)
        db.session.commit()

    def analyzeEmotionsUnfiltered(self, topicTitle):
        self._clearData(topicTitle)
        language = getLanguage(topicTitle)
        userStreamingTweets = self.userStreamingTweetsRepository.getByTopicTitle(topicTitle)
        for tweet in userStreamingTweets:
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lematized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            emotions = self._getSentenceEmotion(tweet_lematized, language)
            tweetWithEmotions = TweetWithEmotions(
                id=tweet.id, user_id=current_user.id, topic_title=topicTitle)
            for emotion in emotions:
                setattr(tweetWithEmotions, emotion, emotions[emotion])
            db.session.merge(tweetWithEmotions)
        db.session.commit()

    def _createEmotionObject(self, tweetsWithEmotionsEntity):
        tweetsWithEmotions = []
        for item in tweetsWithEmotionsEntity:
            emotions = dict()
            for emotion in self.emotions:
                emotions[emotion] = getattr(item, emotion)
            tweetWithEmotions = TweetAndEmotion(
                tweet=item.userStreamingTweets, emotion=Emotion(emotions))
            tweetsWithEmotions.append(tweetWithEmotions)
        return tweetsWithEmotions

    def getEmotions(self, per_page, page, topicTitle):
        tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getPaginatedTweetsByTopicTitle(topicTitle=topicTitle, page=page, per_page=per_page)
        tweetsWithEmotionsEntity.items = self._createEmotionObject(tweetsWithEmotionsEntity.items)
        return tweetsWithEmotionsEntity

    def getEmotionsToDownload(self, topicTitle):
        tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getTweetsByTopicTitle(topicTitle)
        return self._createEmotionObject(tweetsWithEmotionsEntity)
