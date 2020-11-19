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
    @api.doc(params={'topicTitle': 'Topic Title', 'reportId': 'Report id', 'algorithm': 'Algorithm', 'threshold': 'Threshold'})
    @api.marshal_list_with(chartValues) 
    def get(self):
        """
        Returns an array of words with its frequency
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        reportId = request.args.get('reportId', 0, type=int)
        algorithm = request.args.get('algorithm', "", type=str)
        threshold = request.args.get('threshold', 0, type=float)
        frequencyAnalyzer = FrequencyAnalyzer()
        return frequencyAnalyzer.getWordsCount(topicTitle, reportId, algorithm, threshold)

@api.route('/hashtags')
class FrequencyAnalyzerController(Resource):
    @login_required
    @api.doc(params={'topicTitle': 'Topic Title', 'reportId': 'Report id', 'algorithm': 'Algorithm', 'threshold': 'Threshold'})
    @api.marshal_list_with(chartValues) 
    def get(self):
        """
        Returns an array of hashtags with its ammount of repetitions
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        reportId = request.args.get('reportId', 0, type=int)
        algorithm = request.args.get('algorithm', "", type=str)
        threshold = request.args.get('threshold', 0, type=float)
        frequencyAnalyzer = FrequencyAnalyzer()
        return frequencyAnalyzer.getHashtagsCount(topicTitle, reportId, algorithm, threshold)
