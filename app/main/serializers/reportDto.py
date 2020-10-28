from flask_restx import Namespace, fields


class ReportDto:
    api = Namespace('reports', description='Operations related to reports')
    report = api.model('Report', {
        'id': fields.Integer(description="Id of the report"),
        'title': fields.String(required=True, description="Title of the report"),
        'content': fields.String(required=True, description="Content of the report"),
        'language': fields.String(required=True, description="Language of the report")
    })
    reportsDelete = api.model('ReportsDelete', {
        'reports': fields.List(fields.Integer())
    })
