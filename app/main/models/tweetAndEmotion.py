from ..entities.userStreamingTweets import UserStreamingTweets
from .emotion import Emotion


class TweetAndEmotion:
    def __init__(self, emotion: Emotion, tweet: UserStreamingTweets):
        self.tweet = tweet
        self.emotion = emotion
