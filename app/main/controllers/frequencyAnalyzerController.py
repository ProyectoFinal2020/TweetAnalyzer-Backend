from flask import request
from ..serializers.frequencyAnalyzerDto import FrequencyAnalyzerDto
from ..services.frequencyAnalyzer.frequencyAnalyzer import FrequencyAnalyzer
from flask_login import login_required
from flask_restx import Resource

api = FrequencyAnalyzerDto.api
chartValues = FrequencyAnalyzerDto.chartValues

    

@api.route('')
class FrequencyAnalyzerController(Resource):
    @login_required
    @api.doc(params={'topicTitle': 'Topic Title'})
    @api.marshal_list_with(chartValues) 
    def get(self):
        """
        Returns an array of words with its frequency
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        frequencyAnalyzer = FrequencyAnalyzer()
        return frequencyAnalyzer.getWordsCount(topicTitle)

@api.route('/hashtags')
class FrequencyAnalyzerController(Resource):
    @login_required
    @api.doc(params={'topicTitle': 'Topic Title'})
    @api.marshal_list_with(chartValues) 
    def get(self):
        """
        Returns an array of hashtags with its ammount of repetitions
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        frequencyAnalyzer = FrequencyAnalyzer()
        return frequencyAnalyzer.getHashtagsCount(topicTitle)
