from datetime import date

import pandas as pd
import tweepy
from ...entities import db
from ...entities.tweetsTopic import TweetsTopic
from ...entities.userStreamingTweets import UserStreamingTweets
from ...models.userMemorySpace import UserMemorySpace, TopicAndSpaceUsed
from ..sentimentAnalyzer.sentimentAnalyzer import getLanguage
from . import tweepyApi
from .tweetBuilder import TweetBuilder
from .tweetConverter import TweetConverter
from flask_login import current_user

MAX_TWEETS_PER_USER = 10000


def createTweetsTopic(topic_title, language):
    exists = TweetsTopic.query.filter_by(
        topic_title=topic_title, user_id=current_user.id).count() > 0
    if not exists:
        tweetsTopic = TweetsTopic(
            topic_title=topic_title, language=language, user_id=current_user.id)
        db.session.add(tweetsTopic)
        db.session.commit()


def getTweetsFromAPI(topic_title: str, search_tags: list, language: str, since: date, until: date, maxAmount: int):
    createTweetsTopic(topic_title, language)
    tweetBuilder = TweetBuilder(TweetConverter())
    tags = " OR ".join(search_tags)
    date_since = since.strftime("%Y-%m-%d")
    date_until = until.strftime("%Y-%m-%d")
    tweets_dict = []
    space_available = MAX_TWEETS_PER_USER - UserStreamingTweets.query \
        .filter(UserStreamingTweets.user_id == current_user.id).count()

    tweetsFilteredByTag = tweepy.Cursor(tweepyApi.search, q=tags + "-filter:retweets", lang=language, since=date_since,
                                        until=date_until, tweet_mode="extended").items(maxAmount)
    for tweet in tweetsFilteredByTag:
        tweets_dict.append(tweetBuilder.generateTweetDict(
            status=tweet, topic_title=topic_title))
        if len(tweets_dict) < space_available:
            db.session.merge(tweetBuilder.generateTweet(
                status=tweet, topic_title=topic_title))
            space_available -= 1

    db.session.commit()
    return tweets_dict


def getUserMemorySpaceInformation():
    userStreamingTweetsGroupedByTopic = UserStreamingTweets.query \
        .filter(UserStreamingTweets.user_id == current_user.id).all()
    df = pd.DataFrame([(d.topic_title, d.id, d.text) for d in userStreamingTweetsGroupedByTopic],
                      columns=['topic_title', 'id', 'text'])
    countByTopicTitle = df.groupby(['topic_title'])[
        'topic_title'].agg(['count'])
    topicsAndSpaceUsed = [
        TopicAndSpaceUsed(
            topic=topic_title, spacedUsed=result[0], language=getLanguage(topic_title))
        for topic_title, result in countByTopicTitle.iterrows()
    ]
    spaceUsed = len(df.index)
    return UserMemorySpace(
        availableSpace=MAX_TWEETS_PER_USER - spaceUsed,
        spaceUsed=spaceUsed,
        topicsAndSpaceUsed=topicsAndSpaceUsed
    )


def getAvailableSpace():
    return MAX_TWEETS_PER_USER - UserStreamingTweets.query \
        .filter(UserStreamingTweets.user_id == current_user.id).count()


def getTweetsTitles():
    return TweetsTopic.query.filter(
        TweetsTopic.user_id == current_user.id).order_by(TweetsTopic.topic_title).all()


def deleteTweetsByTopicTitle(topics):
    for topic in topics:
        UserStreamingTweets.query.filter_by(
            topic_title=topic, user_id=current_user.id).delete()
        TweetsTopic.query.filter_by(
            topic_title=topic, user_id=current_user.id).delete()
    db.session.commit()


def deleteTweetsById(tweets):
    for tweet in tweets:
        UserStreamingTweets.query.filter_by(
            id=tweet, user_id=current_user.id).delete()
    db.session.commit()


def getTweetsByTopic(topic):
    return UserStreamingTweets.query.filter_by(topic_title=topic, user_id=current_user.id).all()
