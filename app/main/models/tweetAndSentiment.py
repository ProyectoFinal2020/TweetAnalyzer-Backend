from ..entities.tweet import Tweet
from .sentiment import Sentiment


class TweetAndSentiment:
    def __init__(self, sentiment: Sentiment, tweet: Tweet):
        self.tweet = tweet
        self.sentiment = sentiment
