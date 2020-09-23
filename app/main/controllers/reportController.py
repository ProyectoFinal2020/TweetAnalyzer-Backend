from flask import request
from ..serializers.reportDto import ReportDto
from ..services.reportManager.reportManager import ReportUploader
from flask_login import login_required
from flask_restx import Resource

api = ReportDto.api
report = ReportDto.report


@api.route('')
class ReportController(Resource):
    @login_required
    @api.marshal_list_with(report)
    def get(self):
        """
        Returns a list of all reports belonging to the current user
        """
        reportUploader = ReportUploader()
        return reportUploader.getAllReportsFromUser()

    @login_required
    @api.response(201, 'Report successfully uploaded.')
    # to do: ver como arreglarlo p q acepte el serializer
    # @api.expect([report])
    def post(self):
        """
        Saves reports in the current user account
        """
        reports = request.json['reports']
        reportUploader = ReportUploader()
        return reportUploader.uploadReport(reports)

    @login_required
    @api.expect(report)
    @api.response(204, 'File successfully updated.')
    def put(self):
        """
        Updates a report associated with the current user
        """
        reportUploader = ReportUploader()
        if reportUploader.updateReport(request.json):
            return None, 200
        return None, 400

    @login_required
    @api.response(200, 'Reports successfully deleted.')
    @api.expect([int])
    def delete(self):
        """
        Deletes a list of reports belonging to the current user
        """
        reports = request.json['reports']
        reportUploader = ReportUploader()
        return reportUploader.deleteReports(reports)
