from ...entities import db
from ...entities.report import Report
from ...repositories.unitOfWork import unitOfWork
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound


class ReportUploader:
    def __init__(self):
        self.reportRepository = unitOfWork.getReportRepository()

    def uploadReport(self, reports):
        errors = []
        for report in reports:
            title = report["title"]
            content = report["content"]
            language = report["language"]
            existsDuplicates = self.reportRepository.getByTitle(title) != None
            if existsDuplicates:
                errors.append(
                    'Ya existe una noticia titulada "{}"'.format(title))
            else:
                if content == "":
                    errors.append(
                        'La noticia titulada "{}" está vacía. Por favor utilice una noticia con contenido.'.format(
                            title))
                else:
                    newReport = Report(
                        user_id=current_user.id, title=title, content=content, language=language)
                    db.session.add(newReport)
        db.session.commit()
        return errors

    def updateReport(self, updatedReport):
        report = self.reportRepository.getById(updatedReport['id']) 
        if report is not None:
            report.title = updatedReport['title']
            report.content = updatedReport['content']
            db.session.merge(report)
            db.session.commit()
            return True
        return False

    def getAllReportsFromUser(self):
        try:
            return self.reportRepository.getAllOrderedByTitle()
        except NoResultFound:
            return None

    def deleteReports(self, reportsIds):
        for reportId in reportsIds:
            report = self.reportRepository.getById(id=reportId)
            db.session.delete(report) if report is not None else None
        db.session.commit()
