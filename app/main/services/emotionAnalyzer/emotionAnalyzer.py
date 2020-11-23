import collections

from ...entities import db
from ...entities.tweetWithEmotions import TweetWithEmotions
from ...entities.tweetWithScores import TweetWithScores
from ...entities.userStreamingTweets import UserStreamingTweets
from ...models.language import Language
from ...models.emotion import Emotion
from ...models.tweetAndEmotion import TweetAndEmotion
from ...repositories.unitOfWork import unitOfWork
from ..common.data_preprocessing import tokenize_and_preprocess, lemmatize
from flask_login import current_user
from ..common.getLanguage import getLanguage
from bunch import Bunch
import json


class EmotionAnalyzer:
    def __init__(self):
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()
        self.tweetWithEmotionsRepository = unitOfWork.getTweetWithEmotionsRepository()
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.emotionLexiconRepository = unitOfWork.getEmotionLexiconRepository()
        self.emotions = ["anger", "anticipation", "disgust",
                         "fear", "joy", "sadness", "surprise", "trust"]
        self.languageDict = {"en": Language.ENGLISH, "es": Language.SPANISH}

    def _getLemmas(self, language, topicTitle):
        lemmas = []
        self.tweets_with_lemmas = []
        userStreamingTweets = self.userStreamingTweetsRepository.getAllByTopicTitle(
            topicTitle)
        for tweet in userStreamingTweets:
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_with_lemma = []
            for token in tweet_tokenized:
                lemma = lemmatize(token, language)
                lemmas.append(lemma)
                tweet_with_lemma.append(lemma)
            aux = Bunch(id=tweet.id, lemmas=tweet_with_lemma)
            self.tweets_with_lemmas.append(aux)
        return lemmas

    def _getEmotionsFromLexicon(self, topicTitle):
        language = getLanguage(topicTitle)
        lemmas = self._getLemmas(language, topicTitle)
        words_with_emotions = self.emotionLexiconRepository.getEmotionsOfATopic(
            lemmas, self.languageDict[language])
        self.lemma_with_emotions_dict = {}
        for word_with_emotion in words_with_emotions:
            if language == "es":
                self.lemma_with_emotions_dict[word_with_emotion.spanish] = word_with_emotion
            else:
                self.lemma_with_emotions_dict[word_with_emotion.english] = word_with_emotion

    def _getEmotion(self, token, language):
        emotions = []
        if token in self.lemma_with_emotions_dict:
            entry = self.lemma_with_emotions_dict[token]
            for attr, value in entry.__dict__.items():
                if (attr in self.emotions) and (value == 1):
                    emotions.append(attr)
        return emotions

    def _getSentenceEmotion(self, sentence_tokenized_and_lemmatized, language):
        tokens_emotions = []
        for token in sentence_tokenized_and_lemmatized:
            tokens_emotions += self._getEmotion(token, language)
        return collections.Counter(tokens_emotions)

    def analyzeEmotions(self, topicTitle):
        self._getEmotionsFromLexicon(topicTitle)
        language = getLanguage(topicTitle)
        for tweet in self.tweets_with_lemmas:
            emotions = self._getSentenceEmotion(tweet.lemmas, language)
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

    def getEmotions(self, topicTitle, reportId, algorithm, threshold, per_page, page):
        if reportId and threshold and algorithm != "":
            tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getTweetsWithScoresAndEmotions(
                topicTitle, reportId, algorithm, threshold, per_page, page)
        else:
            tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getPaginatedTweetsByTopicTitle(
                topicTitle=topicTitle, page=page, per_page=per_page)
        tweetsWithEmotionsEntity.items = self._createEmotionObject(
            tweetsWithEmotionsEntity.items)
        return tweetsWithEmotionsEntity

    def getEmotionsToDownload(self, topicTitle):
        tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getAllTweetsByTopicTitle(
            topicTitle)
        return self._createEmotionObject(tweetsWithEmotionsEntity)

    def getEmotionsOfATopic(self, topicTitle, reportId, algorithm, threshold):
        lemmas_emotions_dict = {}
        for emotion in self.emotions:
            lemmas_emotions_dict[emotion] = 0
        if reportId and threshold and algorithm != "":
            tweets = self.tweetWithEmotionsRepository.getTweetsWithScoresAndEmotions(
                topicTitle, reportId, algorithm, threshold)
        else:
            tweets = self.tweetWithEmotionsRepository.getAllTweetsByTopicTitle(
                topicTitle)
        for tweet in tweets:
            for attr, value in tweet.__dict__.items():
                if (attr in self.emotions) and (value == 1) and attr in lemmas_emotions_dict:
                    lemmas_emotions_dict[attr] = lemmas_emotions_dict[attr] + 1
        return lemmas_emotions_dict
