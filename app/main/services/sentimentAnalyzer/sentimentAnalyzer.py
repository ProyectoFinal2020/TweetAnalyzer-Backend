from ...repositories.unitOfWork import unitOfWork
from flask_login import current_user
from ... import settings
from ...models.sentimentAnalyzer.sentimentBucket import SentimentBucket
from ...models.sentimentAnalyzer.sentimentBucketWithTweets import SentimentBucketWithTweets


class SentimentAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()

    def getSentimentsFilteredByPolarityValueAndThreshold(self, topic_title, min_polarity, max_polarity, page, per_page, report_id, algorithm, threshold):
        return self.userStreamingTweetsRepository.\
            getPaginatedByPolarity(topic_title=topic_title, max_polarity=max_polarity, min_polarity=min_polarity,
                                   reportId=report_id, algorithm=algorithm, threshold=threshold, per_page=per_page, page=page)

    def getSentimentsFilteredByPolarityValue(self, topic_title, min_polarity, max_polarity, page, per_page):
        return self.userStreamingTweetsRepository.getPaginatedByTopicTitleInRange(per_page=per_page, page=page,
                                                                                  topic_title=topic_title, max_polarity=max_polarity, min_polarity=min_polarity)

    def _isPolarityLessThanMaxValue(self, tweet, currentMaxValue):
        return tweet.polarity <= currentMaxValue if currentMaxValue == settings.MAX_POLARITY_VALUE else tweet.polarity < currentMaxValue

    def _generateBucket(self, min_value, max_value, tweets, includeTweets):
        if includeTweets:
            return SentimentBucketWithTweets(min_value=min_value, max_value=max_value, tweets=tweets)
        else:
            return SentimentBucket(min_value=min_value, max_value=max_value, tweets_amount=len(tweets))

    def _generateBuckets(self, tweets, step_size: float, includeTweets):
        currentMinValue = float(settings.MIN_POLARITY_VALUE)
        currentMaxValue = currentMinValue + step_size
        polarityBuckets = []
        while currentMaxValue <= float(settings.MAX_POLARITY_VALUE):
            tweetsInBucket = list(filter(lambda tweet: tweet.polarity >=
                                         currentMinValue and self._isPolarityLessThanMaxValue(tweet, currentMaxValue), tweets))
            polarityBuckets.append(self._generateBucket(
                min_value=currentMinValue, max_value=currentMaxValue, tweets=tweetsInBucket, includeTweets=includeTweets))
            currentMaxValue += step_size
            currentMinValue += step_size
        return polarityBuckets

    def getTweetCountForPolarityBucketsFilteredBySimAlgorithm(self, report_id, topic_title, algorithm, threshold, step_size=0.25, includeTweets=False):
        tweetsWithScores = self.tweetWithScoresRepository.\
            getAllTweetsWithScoresFilteredByThreshold(
                topicTitle=topic_title, reportId=report_id, algorithm=algorithm, threshold=threshold)
        tweets = [
            tweetWithScores.userStreamingTweets for tweetWithScores in tweetsWithScores]
        return self._generateBuckets(tweets, step_size, includeTweets)

    def getTweetCountForPolarityBuckets(self, topic_title, step_size=0.25, includeTweets=False):
        tweets = self.userStreamingTweetsRepository.getAllByTopicTitle(
            topic_title=topic_title)
        return self._generateBuckets(tweets, step_size, includeTweets)
