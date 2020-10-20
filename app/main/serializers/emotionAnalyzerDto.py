from ..serializers.tweetDto import tweet
from flask_restx import Namespace, fields

emotion = {
    'anger': fields.Integer(description=""),
    'anticipation': fields.Integer(description=""),
    'disgust': fields.Integer(description=""),
    'fear': fields.Integer(description=""),
    'joy': fields.Integer(description=""),
    'sadness': fields.Integer(description=""),
    'surprise': fields.Integer(description=""),
    'trust': fields.Integer(description=""),
}


class EmotionAnalyzerDto:
    api = Namespace('emotionAnalyzer',
                    description='Operations related to emotion analysis')
    tweetAndEmotion = api.model('EmotionAnalyzerResult', {
        'tweet': fields.Nested(api.model('Tweet', tweet)),
        'emotion': fields.Nested(api.model('Emotion', emotion))
    })
    emotionAnalyzer = api.model('EmotionAnalyzer', {
        'topicTitle': fields.String(required=True, description="Topic title"),
        'reportId': fields.Integer(required=True, description="Report id"),
        'algorithm': fields.String(required=True, description="Algorithm to execute"),
        'threshold': fields.Float(required=True, description="Threshold to comply"),
    })
    paginatedEmotionAnalyzer = api.model('PaginatedEmotionAnalyzer', {
        'page': fields.String(description="Current page"),
        'per_page': fields.String(description="Tweets per page"),
        'pages': fields.String(description="Amount of pages"),
        'total': fields.String(description="Amount of tweets"),
        'items': fields.List(fields.Nested(tweetAndEmotion), description="Tweets with scores of current page")
    })
