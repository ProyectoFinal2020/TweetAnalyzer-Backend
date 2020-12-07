from .tweetDto import tweet as tweet_dict
from .tweetRetrievalDto import TweetRetrievalDto
from flask_restx import Namespace, fields


class UserInfoDto:
    api = Namespace(
        'user', description='Operations related to aditional info regarding the user')
    tweet = api.model('Tweet', tweet_dict)
    paginatedTweets = api.model('PaginatedTweets', {
        'page': fields.String(description="Current page"),
        'per_page': fields.String(description="Tweets per page"),
        'pages': fields.String(description="Amount of pages"),
        'total': fields.String(description="Amount of tweets"),
        'items': fields.List(fields.Nested(tweet), description="Tweets of current page")
    })
    tweetTitle = api.model("TweetTitle", {
        'topic_title': fields.String(description="Topic title"),
        'language': fields.String(description="Topic language")
    })
    topicAndSpaceUsed = api.model('TopicAndSpaceUsed', {
        'topic_title': fields.String(description="Tweet's topic"),
        'spaceUsed': fields.String(description="Number of tweets about the current topic saved in the database"),
        'language': fields.String(description="Language of the topic")
    })
    userMemorySpace = api.model('UserMemorySpace', {
        'availableSpace': fields.Integer(description="Number of new tweets the user can save in the database"),
        'spaceUsed': fields.Integer(description="Number of tweets the user saved in the database"),
        'additionalInformation': fields.List(fields.Nested(topicAndSpaceUsed),
                                             description="Additional information about the storage usage")
    })
