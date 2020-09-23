from ..serializers.tweetDto import tweet
from flask_restx import Namespace, fields

sentiment = {
    'anger': fields.Integer(description=""),
    'anticipation': fields.Integer(description=""),
    'disgust': fields.Integer(description=""),
    'fear': fields.Integer(description=""),
    'joy': fields.Integer(description=""),
    'sadness': fields.Integer(description=""),
    'surprise': fields.Integer(description=""),
    'trust': fields.Integer(description=""),
}


class SentimentAnalyzerDto:
    api = Namespace('sentimentAnalyzer',
                    description='Operations related to sentiment analysis')
    tweetAndSentiment = api.model('SentimentAnalyzerResult', {
        'tweet': fields.Nested(api.model('Tweet', tweet)),
        'sentiment': fields.Nested(api.model('Sentiment', sentiment))
    })
    sentimentAnalyzer = api.model('SentimentAnalyzer', {
        'topicTitle': fields.String(required=True, description="Topic title"),
        'reportId': fields.Integer(required=True, description="Report id"),
        'algorithm': fields.String(required=True, description="Algorithm to execute"),
        'threshold': fields.Float(required=True, description="Threshold to comply"),
    })
    paginatedSentimentAnalyzer = api.model('PaginatedSentimentAnalyzer', {
        'page': fields.String(description="Current page"),
        'per_page': fields.String(description="Tweets per page"),
        'pages': fields.String(description="Amount of pages"),
        'total': fields.String(description="Amount of tweets"),
        'items': fields.List(fields.Nested(tweetAndSentiment), description="Tweets with scores of current page")
    })
