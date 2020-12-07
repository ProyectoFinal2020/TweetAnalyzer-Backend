from flask_restx import Namespace, fields


class TweetRetrievalDto:
    api = Namespace(
        'tweetRetrieval', description='Operations related to tweets retrieval from Twitter API')
    twitterQuery = api.model('TwitterQuery', {
        'topic_title': fields.String(required=True, description="Tweet's topic"),
        'tags': fields.List(fields.String, required=True, description="Queries to look up on twitter"),
        'maxAmount': fields.Integer(required=True, description="Maximum amount of tweets to be saved on the json file"),
        'since': fields.Date(description=""),
        'until': fields.Date(description=""),
        'language': fields.String(description="")
    })
