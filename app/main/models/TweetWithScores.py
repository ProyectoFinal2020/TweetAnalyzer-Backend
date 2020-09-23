from ..entities.tweet import Tweet


class TweetWithScores:
    def __init__(self, tweet: Tweet, scores: dict):
        self.tweet = tweet
        self.scores = scores
