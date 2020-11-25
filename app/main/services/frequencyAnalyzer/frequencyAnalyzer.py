from ...repositories.unitOfWork import unitOfWork
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user
from ..common.getLanguage import getLanguage
from ...services.common.data_preprocessing import tokenize_and_preprocess, lemmatize
from .frequencyAnalyzerMerger import merge

class FrequencyAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()

    def getWordsCount(self, topicTitle, reportId, algorithm, threshold):
        unfiltered = reportId == 0 or algorithm == "" or threshold == 0
        if unfiltered:
            tweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topicTitle)
        else:
            tweets = self.tweetWithScoresRepository.getAllTweetsWithScoresFilteredByThreshold(topicTitle, reportId, algorithm, threshold)
        language = getLanguage(topicTitle)
        wordsCount = {}
        for tweet in tweets:
            if not unfiltered:
                tweet = tweet.userStreamingTweets
            tweet_tokenized = tokenize_and_preprocess(tweet.text, language)
            tweet_lemmatized = [lemmatize(token, language)
                               for token in tweet_tokenized]
            for lemma in tweet_lemmatized:
                if lemma in wordsCount:
                    wordsCount[lemma] = wordsCount[lemma] + 1                 
                else:
                    wordsCount[lemma] = 1
        return merge(wordsCount)

    def getHashtagsCount(self, topicTitle, reportId, algorithm, threshold):
        unfiltered = reportId == 0 or algorithm == "" or threshold == 0
        if(unfiltered):
            tweets = self.userStreamingTweetsRepository.getAllByTopicTitle(topicTitle)
        else:
            tweets = self.tweetWithScoresRepository.getAllTweetsWithScoresFilteredByThreshold(topicTitle, reportId, algorithm, threshold)
        hashtagsCount = {}
        for tweet in tweets:
            if not unfiltered:
                tweet = tweet.userStreamingTweets
            hashtags = tweet.hashtags.split()
            for hashtag in hashtags:
                if hashtag in hashtagsCount:
                    hashtagsCount[hashtag] = hashtagsCount[hashtag] +1
                else:
                    hashtagsCount[hashtag] = 1
        return merge(hashtagsCount)