from flask import request
from ..serializers.sentimentAnalyzerDto import SentimentAnalyzerDto
from ..services.sentimentAnalyzer.sentimentAnalyzer import SentimentAnalyzer
from flask_login import login_required
from flask_restx import Resource
import logging
from .. import settings

api = SentimentAnalyzerDto.api
paginatedTweets = SentimentAnalyzerDto.paginatedSentimentAnalyzer
log = logging.getLogger(__name__)


@api.route('')
class SentimentAnalyzerController(Resource):
    @login_required
    @api.doc(params={
        'page': 'Page number', 
        'per_page': 'Tweets per page', 
        'topicTitle': 'Topic Title',
        'min_polarity': "Minimum value for polarity",
        'max_polarity': "Maximum value for polarity"
    })
    @api.marshal_with(paginatedTweets)
    def get(self):
        """
        Returns a list of all tweets with sentiments belonging to a topic
        """
        # To-Do: falta que dependa del reportId y del algoritmo
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        topicTitle = request.args.get('topicTitle', "", type=str)
        min_polarity = request.args.get('min_polarity', settings.MIN_POLARITY_VALUE, type=float)
        max_polarity = request.args.get('max_polarity', settings.MAX_POLARITY_VALUE, type=float)
        sentimentAnalyzer = SentimentAnalyzer()
        return sentimentAnalyzer.getSentimentsFilteredByPolarityValue(topicTitle, min_polarity, max_polarity, page, per_page)

@api.route('/graph')
class SentimentAnalyzerGraphController(Resource):
    @login_required
    @api.doc(params={
        'topicTitle': 'Topic Title', 
        'step_size': 'Size of each bucket',
        'reportId': 'Report id',
        'algorithm': 'Executed algorithm',
        'threshold': 'Threshold to comply',
    })
    def get(self):
        """
        Returns an array of tweet numbers according to polarity buckets
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        step_size = request.args.get('step_size', settings.STEP_SIZE, type=float)
        reportId = request.args.get('reportId', 0, type=int)
        algorithm = request.args.get('algorithm', "", type=str)
        threshold = request.args.get('threshold', 0, type=float)
        sentimentAnalyzer = SentimentAnalyzer()
        if(not reportId or reportId==0 or not algorithm or algorithm=="" or not threshold or threshold==0):
            return sentimentAnalyzer.getTweetCountForPolarityBuckets(topicTitle, step_size=step_size)
        else:
            return sentimentAnalyzer.getTweetCountForPolarityBucketsFilteredBySimAlgorithm(\
                report_id=reportId, topic_title=topicTitle, algorithm=algorithm, threshold=threshold, step_size=step_size)
