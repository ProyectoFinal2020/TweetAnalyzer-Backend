import collections

from ...entities import db
from ...entities.tweetWithEmotions import TweetWithEmotions
from ...entities.tweetWithScores import TweetWithScores
from ...entities.tweetsTopic import TweetsTopic
from ...entities.userStreamingTweets import UserStreamingTweets
from ...models.language import Language
from ...models.sentiment import Sentiment
from ...models.tweetAndSentiment import TweetAndSentiment
from ...repositories.unitOfWork import unitOfWork
from ..common.data_preprocessing import tokenize_and_preprocess, lemmatize
from flask_login import current_user


def getLanguage(topicTitle):
    tweetsTopic = TweetsTopic.query.filter_by(
        topic_title=topicTitle, user_id=current_user.id).one_or_none()
    if tweetsTopic is not None:
        return tweetsTopic.language
    return None


class SentimentAnalyzer:
    def __init__(self):
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

    def _getTweetsWithScores(self, topicTitle, reportId, algorithm, threshold):
        return TweetWithScores.query. \
            filter(TweetWithScores.topic_title == topicTitle, TweetWithScores.report_id == reportId,
                   TweetWithScores.user_id == current_user.id, getattr(TweetWithScores, algorithm) >= threshold).all()

    def _clearData(self, topicTitle):
        TweetWithEmotions.query.filter_by(
            topic_title=topicTitle, user_id=current_user.id).delete()

    def analyzeSentiments(self, topicTitle, reportId, algorithm, threshold=0):
        self._clearData(topicTitle)
        language = getLanguage(topicTitle)
        tweetsWithScores = self._getTweetsWithScores(
            topicTitle, reportId, algorithm, threshold)
        for tweetWithScores in tweetsWithScores:
            tweet = tweetWithScores.userStreamingTweets
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lematized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            sentiments = self._getSentenceEmotion(tweet_lematized, language)
            tweetWithEmotions = TweetWithEmotions(
                id=tweet.id, user_id=current_user.id, topic_title=topicTitle)
            for sentiment in sentiments:
                setattr(tweetWithEmotions, sentiment, sentiments[sentiment])
            db.session.merge(tweetWithEmotions)
        db.session.commit()

    def analyzeSentimentsUnfiltered(self, topicTitle):
        self._clearData(topicTitle)
        language = getLanguage(topicTitle)
        userStreamingTweets = UserStreamingTweets.query. \
            filter_by(topic_title=topicTitle, user_id=current_user.id).all()
        for tweet in userStreamingTweets:
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lematized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            sentiments = self._getSentenceEmotion(tweet_lematized, language)
            tweetWithEmotions = TweetWithEmotions(
                id=tweet.id, user_id=current_user.id, topic_title=topicTitle)
            for sentiment in sentiments:
                setattr(tweetWithEmotions, sentiment, sentiments[sentiment])
            db.session.merge(tweetWithEmotions)
        db.session.commit()

    def _createSentimentObject(self, tweetsWithEmotionsEntity):
        tweetsWithEmotions = []
        for item in tweetsWithEmotionsEntity:
            sentiments = dict()
            for emotion in self.emotions:
                sentiments[emotion] = getattr(item, emotion)
            tweetWithSentiments = TweetAndSentiment(
                tweet=item.userStreamingTweets, sentiment=Sentiment(sentiments))
            tweetsWithEmotions.append(tweetWithSentiments)
        return tweetsWithEmotions

    def getSentiments(self, per_page, page, topicTitle):
        tweetsWithEmotionsEntity = TweetWithEmotions.query.filter_by(topic_title=topicTitle,
                                                                     user_id=current_user.id).paginate(
            per_page=per_page, page=page)
        tweetsWithEmotionsEntity.items = self._createSentimentObject(
            tweetsWithEmotionsEntity.items)
        return tweetsWithEmotionsEntity

    def getSentimentsToDownload(self, topicTitle):
        tweetsWithEmotionsEntity = TweetWithEmotions.query.filter_by(topic_title=topicTitle,
                                                                     user_id=current_user.id).all()
        return self._createSentimentObject(tweetsWithEmotionsEntity)
