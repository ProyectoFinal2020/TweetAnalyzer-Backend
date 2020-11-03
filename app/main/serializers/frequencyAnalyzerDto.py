from flask_restx import Namespace

class FrequencyAnalyzerDto:
    api = Namespace('frequencyAnalyzer', description='Operations related to the frequency analysis')
