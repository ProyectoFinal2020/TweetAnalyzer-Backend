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

        
    def _getLemmas(self, language, topicTitle, reportId, algorithm, threshold):
        lemmas = []
        self.tweets_with_lemmas = []
        if(reportId == 0 or algorithm == "" or threshold == 0):
            userStreamingTweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topicTitle)
        else:
            userStreamingTweets = self.tweetWithScoresRepository.getAllTweetsWithScoresFilteredByThreshold(topicTitle, reportId, algorithm, threshold)
        for tweet in userStreamingTweets:
            if (reportId != 0 and algorithm != "" and threshold != 0):
                tweet = tweet.userStreamingTweets
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_with_lemma = []
            for token in tweet_tokenized:
                lemma = lemmatize(token, language)
                lemmas.append(lemma)
                tweet_with_lemma.append(lemma)
            aux = Bunch(id=tweet.id, lemmas=tweet_with_lemma)
            self.tweets_with_lemmas.append(aux)
        return lemmas

    def _getEmotionsFromLexicon(self, topicTitle, reportId, algorithm, threshold=0):
        language = getLanguage(topicTitle)
        lemmas = self._getLemmas(language, topicTitle, reportId, algorithm, threshold)
        words_with_emotions = self.emotionLexiconRepository.getEmotionsOfATopic(lemmas, self.languageDict[language])
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

    def _clearData(self, topicTitle):
        self.tweetWithEmotionsRepository.getTweetsByTopicTitle(topic_title=topicTitle).delete()
        db.session.commit()

    def analyzeEmotions(self, topicTitle, reportId, algorithm, threshold=0):
        self._clearData(topicTitle)
        self._getEmotionsFromLexicon(topicTitle,reportId, algorithm, threshold)
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
                if lemma in lemmas_dict:
                    lemmas_dict[lemma] = lemmas_dict[lemma] + 1                 
                else:
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
            frequency =  lemmas_dict[word.english if language=="en" else word.spanish]
            for attr, value in word.__dict__.items():
                if (attr in self.emotions) and (value == 1):
                    if attr in lemmas_emotions_dict:
                        lemmas_emotions_dict[attr] = lemmas_emotions_dict[attr] + frequency
        return lemmas_emotions_dict