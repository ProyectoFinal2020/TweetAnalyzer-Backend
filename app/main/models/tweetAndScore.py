from ..entities.tweet import Tweet


class TweetAndScore:
    def __init__(self, tweet: Tweet, tweetWithoutStopwords: [], score):
        self.tweet = tweet
        self.tweetWithoutStopwords = tweetWithoutStopwords
        self.score = score
