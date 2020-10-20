from flask import request
from ..serializers.sentimentAnalyzerDto import SentimentAnalyzerDto
from ..services.sentimentAnalyzer.sentimentAnalyzer import SentimentAnalyzer
from flask_login import login_required
from flask_restx import Resource
import logging

api = SentimentAnalyzerDto.api
tweet = SentimentAnalyzerDto.tweet
log = logging.getLogger(__name__)


@api.route('')
class SentimentAnalyzerController(Resource):
    @login_required
    @api.doc(params={'topicTitle': 'Topic Title'})
    @api.marshal_list_with(tweet)
    def get(self):
        """
        Returns a list of all tweets with sentiments belonging to a topic
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        sentimentAnalyzer = SentimentAnalyzer()
        return sentimentAnalyzer.getSentiments(topicTitle)
