from datetime import date

import pandas as pd
import tweepy
from ...entities import db
from ...entities.tweetsTopic import TweetsTopic
from ...entities.userStreamingTweets import UserStreamingTweets
from ...models.userMemorySpace import UserMemorySpace, TopicAndSpaceUsed
from ...services.common.getLanguage import getLanguage
from ...repositories.unitOfWork import unitOfWork
from . import tweepyApi
from .tweetBuilder import TweetBuilder
from .tweetConverter import TweetConverter
from flask_login import current_user
from ...utils.tweetAnalyzerException import TweetAnalyzerException

MAX_TWEETS_PER_USER = 10000

class TweetsService:
    def __init__(self):
        self.userStreamingTweetsRepository = unitOfWork.getUserStreamingTweetsRepository()
        self.tweetsTopicRepository = unitOfWork.getTweetsTopicRepository()

    def _createTweetsTopic(self, topic_title, language):
        tweetsTopic = self.tweetsTopicRepository.getByTweetTopic(topic_title)
        if tweetsTopic is None:
            tweetsTopic = TweetsTopic(
                topic_title=topic_title, language=language, user_id=current_user.id)
            db.session.add(tweetsTopic)
            db.session.commit()
        elif tweetsTopic.language != language: 
            raise TweetAnalyzerException('El tema ya existe para otro idioma.')

    def getTweetsFromAPI(self, topic_title: str, search_tags: list, language: str, since: date, until: date, maxAmount: int):
        self._createTweetsTopic(topic_title, language)
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

    def getUserMemorySpaceInformation(self):
        allTweets = self.userStreamingTweetsRepository.getAllByCurrentUser()
        df = pd.DataFrame([(d.topic_title, d.id, d.text) for d in allTweets],
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

    def getAvailableSpace(self):
        return MAX_TWEETS_PER_USER - self.userStreamingTweetsRepository.getByCurrentUser().count()

    def deleteTweetsByTopicTitle(self, topics):
        for topic in topics:
            self.userStreamingTweetsRepository.getByTopicTitle(topic).delete()
            tweetTopic = self.tweetsTopicRepository.getByTweetTopic(topic)
            db.session.delete(tweetTopic) if tweetTopic else None
        db.session.commit()

    def deleteTweetsById(self, tweets):
        for tweetId in tweets:
            self.userStreamingTweetsRepository.getByCurrentUserAndId(id=tweetId).delete()
        db.session.commit()
