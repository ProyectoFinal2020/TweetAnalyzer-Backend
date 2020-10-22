from flask_restx import Namespace, fields

class SentimentAnalyzerDto:
    api = Namespace('sentimentAnalyzer', description='Operations related to sentiment analysis')
    tweet = api.model('TweetWithSentiment', {
        'id': fields.String(required=True, description="Tweet's id"),
        'username': fields.String(required=True, description="Tweet's username"),
        'text': fields.String(required=True, description="Tweet's text"),
        'to': fields.String(description="Tweet's text"),
        'permalink': fields.String(description="Tweet's permalink"),
        'date': fields.DateTime(description="Tweet's date and time"),
        'formatted_date': fields.String(description="Tweet's formatted date"),
        'img_url': fields.String(description='Tweets image url'),
        'polarity': fields.Float(),
        'subjectivity': fields.Float()
    })
    paginatedSentimentAnalyzer = api.model('PaginatedSentimentAnalyzer', {
        'page': fields.String(description="Current page"),
        'per_page': fields.String(description="Tweets per page"),
        'pages': fields.String(description="Amount of pages"),
        'total': fields.String(description="Amount of tweets"),
        'items': fields.List(fields.Nested(tweet), description="Tweets with scores of current page")
    })
