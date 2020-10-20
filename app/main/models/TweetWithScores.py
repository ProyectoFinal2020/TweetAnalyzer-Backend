from ..entities.userStreamingTweets import UserStreamingTweets


class TweetWithScores:
    def __init__(self, tweet: UserStreamingTweets, scores: dict):
        self.tweet = tweet
        self.scores = scores
