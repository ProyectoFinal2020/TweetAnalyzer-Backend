from flask_restx import Namespace, fields

class FrequencyAnalyzerDto:
    api = Namespace('frequencyAnalyzer', description='Operations related to the frequency analysis')
    chartValues = api.model('ChartValues', {
        'label': fields.String(),
        'value': fields.String()
    })
