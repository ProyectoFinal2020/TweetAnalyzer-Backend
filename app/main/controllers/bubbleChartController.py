from flask import request
from ..serializers.bubbleChartDto import BubbleChartDto
from ..services.bubbleChart.bubbleChart import BubbleChart
from flask_login import login_required
from flask_restx import Resource

api = BubbleChartDto.api
    

@api.route('')
class BubbleChartController(Resource):
    @login_required
    @api.doc(params={'topicTitle': 'Topic Title'})
    def get(self):
        """
        Returns an array of words with its frequency
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        bubbleChart = BubbleChart()
        return bubbleChart.getWordsCount(topicTitle)
