from flask_restx import Namespace

class BubbleChartDto:
    api = Namespace('bubbleChart', description='Operations related to the bubble chart')
