from ...repositories.unitOfWork import unitOfWork
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user

class SentimentAnalyzer:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()

    def getSentiments(self, topic_title):
        return self.userStreamingTweetsRepository.getByTopicTitle(topic_title)

    def getTweetCountForPolarityBuckets(self, topic_title):
        tweets = self.userStreamingTweetsRepository.getByTopicTitle(topic_title)
        aux = [0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        j = 0
        max = 1
        min = 0.75
        while i < len(tweets): 
            polarity = tweets[i].polarity
            if polarity <= max and polarity >= min: 
                aux[j] = aux[j] + 1
                i= i+1
            else: 
                j= j+1
                min -= 0.25
                max -= 0.25
        return aux
          
        