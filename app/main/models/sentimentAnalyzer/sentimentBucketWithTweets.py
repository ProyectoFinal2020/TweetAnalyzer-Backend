class SentimentBucketWithTweets:
    def __init__(self, min_value: float, max_value: float, tweets: list):
        self.min_value = min_value
        self.max_value = max_value
        self.tweets = tweets