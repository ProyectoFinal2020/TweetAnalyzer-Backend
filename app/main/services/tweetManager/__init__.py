import os
import tweepy
from ... import settings

auth = tweepy.OAuthHandler(os.getenv('TWITTER_APP_KEY', settings.TWITTER_APP_KEY),
                           os.getenv('TWITTER_APP_SECRET', settings.TWITTER_APP_SECRET))
auth.set_access_token(os.getenv('TWITTER_KEY', settings.TWITTER_KEY), os.getenv(
    'TWITTER_SECRET', settings.TWITTER_SECRET))
tweepyApi = tweepy.API(auth, wait_on_rate_limit=True)
