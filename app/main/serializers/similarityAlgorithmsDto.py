from ..serializers.tweetDto import tweet
from flask_restx import Namespace, fields

scores = {
    'bagOfWords': fields.Float(),
    'doc2vecGensim': fields.Float(),
    'doc2vecNSim': fields.Float(),
    'softCosine': fields.Float(),
    'tfIdfSim': fields.Float(),
    'word2vecGensim': fields.Float(),
    'wmd': fields.Float(),
    'jaccard': fields.Float()
}


class SimilarityAlgorithmsDto:
    api = Namespace('similarityAlgorithms',
                    description='Operations related to similarity algorithms')
    similarityAlgorithms = api.model('SimilarityAlgorithmsDto', {
        'topicTitle': fields.String(required=True, description="Topic title"),
        'reportId': fields.Integer(required=True, description="Report id"),
        'algorithms': fields.List(fields.String, required=True, description="Algorithms to execute"),
        'language': fields.String(required=True, description="Topic and report language")
    })
    tweetWithScores = api.model('TweetWithScores', {
        'tweet': fields.Nested(api.model('Tweet', tweet), description="Tweet"),
        'scores': fields.Nested(api.model('Scores', scores), description="Scores")
    })
    paginatedTweetWithScores = api.model('PaginatedTweetsWithScore', {
        'page': fields.String(description="Current page"),
        'per_page': fields.String(description="Tweets per page"),
        'pages': fields.String(description="Amount of pages"),
        'total': fields.String(description="Amount of tweets"),
        'items': fields.List(fields.Nested(tweetWithScores), description="Tweets with scores of current page")
    })
