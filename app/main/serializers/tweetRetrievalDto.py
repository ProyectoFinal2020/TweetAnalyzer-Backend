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
    topicAndSpaceUsed = api.model('TopicAndSpaceUsed', {
        'topic': fields.String(description="Tweet's topic"),
        'spaceUsed': fields.String(description="Number of tweets about the current topic saved in the database"),
        'language': fields.String(description="Language of the topic")
    })
    userMemorySpace = api.model('UserMemorySpace', {
        'availableSpace': fields.Integer(description="Number of new tweets the user can save in the database"),
        'spaceUsed': fields.Integer(description="Number of tweets the user saved in the database"),
        'additionalInformation': fields.List(fields.Nested(topicAndSpaceUsed),
                                             description="Additional information about the storage usage")
    })
