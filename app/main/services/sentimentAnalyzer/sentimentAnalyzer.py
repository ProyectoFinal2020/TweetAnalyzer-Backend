from ...repositories.unitOfWork import unitOfWork
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user
from ... import settings

class SentimentAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()

    def getSentimentsFilteredByPolarityValue(self, topic_title, min_polarity, max_polarity, page, per_page):
        return self.userStreamingTweetsRepository.getPaginatedByTopicTitleInRange(per_page=per_page, page=page,\
            topic_title=topic_title, max_polarity=max_polarity, min_polarity=min_polarity)
    
    def _generateBuckets(self, tweets, step_size, includeTweets=False):
        currentMinValue = settings.MIN_POLARITY_VALUE
        currentMaxValue = currentMinValue + step_size
        polarityBuckets = []
        while currentMaxValue <= settings.MAX_POLARITY_VALUE: 
            tweetsInBucket = list(filter(lambda tweet: tweet.polarity >= currentMinValue and tweet.polarity < currentMaxValue, tweets))
            polarityBuckets.append(tweetsInBucket if includeTweets else len(tweetsInBucket))
            currentMaxValue += step_size
            currentMinValue += step_size
        return polarityBuckets

    def getTweetCountForPolarityBucketsFilteredBySimAlgorithm(self, report_id, topic_title, algorithm, threshold, step_size=0.25):
        tweetsWithScores = self.tweetWithScoresRepository.\
            getTweetsWithScores(topicTitle=topic_title, reportId=report_id, algorithm=algorithm, threshold=threshold)
        tweets = [tweetWithScores.userStreamingTweets for tweetWithScores in tweetsWithScores]
        return self._generateBuckets(tweets, step_size)

    def getTweetCountForPolarityBuckets(self, topic_title, step_size=0.25):
        tweets = self.userStreamingTweetsRepository.getByTopicTitle(topic_title=topic_title)
        return self._generateBuckets(tweets, step_size)
          
        