class SentimentBucket:
    def __init__(self, min_value: float, max_value: float, tweets_amount: int):
        self.min_value = min_value
        self.max_value = max_value
        self.tweets_amount = tweets_amount