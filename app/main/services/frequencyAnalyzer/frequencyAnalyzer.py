from ...repositories.unitOfWork import unitOfWork
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user
from ..common.getLanguage import getLanguage
from ...services.common.data_preprocessing import tokenize_and_preprocess, lemmatize

class FrequencyAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()

    def getWordsCount(self, topic_title):
        tweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topic_title)
        language = getLanguage(topic_title)
        wordsCount = {}
        for tweet in tweets:
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lemmatized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            for lemma in tweet_lemmatized:
                try:
                    wordsCount[lemma] = wordsCount[lemma] + 1                 
                except KeyError:
                    wordsCount[lemma] = 1
                    
        return wordsCount

    def getHashtagsCount(self, topic_title):
        tweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topic_title)
        hashtagsCount = {}
        for tweet in tweets:
            hashtags = tweet.hashtags.replace('#','').split()
            for hashtag in hashtags:
                try:
                    hashtagsCount[hashtag] = hashtagsCount[hashtag] +1
                except KeyError:
                    hashtagsCount[hashtag] = 1
        return hashtagsCount