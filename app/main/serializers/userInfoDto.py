from .tweetDto import tweet as tweet_dict
from .tweetRetrievalDto import TweetRetrievalDto
from flask_restx import Namespace, fields


class UserInfoDto:
    api = Namespace(
        'user', description='Operations related to aditional info regarding the user')
    tweet = api.model('Tweet', tweet_dict)
    userMemorySpace = TweetRetrievalDto.userMemorySpace
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
