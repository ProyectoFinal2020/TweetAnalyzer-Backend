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
        self.tweetWithEmotionsRepository.getTweetsByTopicTitle(topic_title=topicTitle).delete()
        db.session.commit()

    def analyzeEmotions(self, topicTitle, reportId, algorithm, threshold=0):
        self._clearData(topicTitle)
        language = getLanguage(topicTitle)
        if(not reportId or not algorithm or not threshold):
            userStreamingTweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topicTitle)
        else:
            userStreamingTweets = self.tweetWithScoresRepository.getAllTweetsWithScoresFilteredByThreshold(
                topicTitle, reportId, algorithm, threshold)
        for tweet in userStreamingTweets:
            if (reportId and algorithm and threshold):
                tweet = tweet.userStreamingTweets
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
        tweetsWithEmotionsEntity = self.tweetWithEmotionsRepository.getAllTweetsByTopicTitle(topicTitle)
        return self._createEmotionObject(tweetsWithEmotionsEntity)

    def _buildLemmasDict(self, language, topicTitle, reportId, algorithm, threshold):
        lemmas_dict = {}
        if(reportId == 0 or algorithm == "" or threshold == 0):
            userStreamingTweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topicTitle)
        else:
            userStreamingTweets = self.tweetWithScoresRepository.getAllTweetsWithScoresFilteredByThreshold(topicTitle, reportId, algorithm, threshold)
        for tweet in userStreamingTweets:
            if (reportId != 0 and algorithm != "" and threshold != 0):
                tweet = tweet.userStreamingTweets
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            for token in tweet_tokenized:
                lemma = lemmatize(token, language)
                try:
                    lemmas_dict[lemma] = lemmas_dict[lemma] + 1                 
                except KeyError:
                    lemmas_dict[lemma] = 1
        return lemmas_dict

    def getEmotionsOfATopic(self, topicTitle, reportId, algorithm, threshold):
        language = getLanguage(topicTitle)
        lemmas_dict = self._buildLemmasDict(language, topicTitle, reportId, algorithm, threshold)
        lemmas_emotions_dict = {}
        for emotion in self.emotions:
            lemmas_emotions_dict[emotion] = 0
        words_with_emotions = self.emotionLexiconRepository.getEmotionsOfATopic(lemmas_dict.keys(), self.languageDict[language])
        for word in words_with_emotions:
            frequency =  lemmas_dict[word.english]
            for attr, value in word.__dict__.items():
                if (attr in self.emotions) and (value == 1):
                    lemmas_emotions_dict[attr] = lemmas_emotions_dict[attr] + frequency
        return lemmas_emotions_dict