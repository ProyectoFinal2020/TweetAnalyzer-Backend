import os
import tweepy

auth = tweepy.OAuthHandler(os.getenv('TWITTER_APP_KEY'),
                           os.getenv('TWITTER_APP_SECRET'))
auth.set_access_token(os.getenv('TWITTER_KEY'), os.getenv('TWITTER_SECRET'))
tweepyApi = tweepy.API(auth, wait_on_rate_limit=True)
