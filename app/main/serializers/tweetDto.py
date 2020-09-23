from flask_restx import Namespace, fields

tweet = {
    'id': fields.String(required=True, description="Tweet's id"),
    'username': fields.String(required=True, description="Tweet's username"),
    'text': fields.String(required=True, description="Tweet's text"),
    'to': fields.String(description="Tweet's text"),
    'retweets': fields.Integer(description="Tweet's number of retweets"),
    'favorites': fields.Integer(description="Tweet's number of favorites"),
    'replies': fields.Integer(description="Tweet's number of replies"),
    'permalink': fields.String(description="Tweet's permalink"),
    'author_id': fields.Integer(description="Tweet's text"),
    'date': fields.DateTime(description="Tweet's date and time"),
    'formatted_date': fields.String(description="Tweet's formatted date"),
    'hashtags': fields.String(description="Tweet's hashtags"),
    'mentions': fields.String(description="Tweet's mentions"),
    'geo': fields.String(description="Tweet's geo info"),
    'urls': fields.String(description="Tweet's urls"),
    'img_url': fields.String(description='Tweets image url')
}


class TweetDto:
    api = Namespace('tweets', description='Operations related to tweets')
    tweet = api.model('Tweet', tweet)
