from ...entities import db
from ...entities.report import Report
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound


class ReportUploader:
    def _buildDict(self, titles):
        fileWithTitle = dict()
        for title in titles:
            fileWithTitle[title["filename"]] = title["title"]
        return fileWithTitle

    def uploadReport(self, reports):
        errors = []
        for report in reports:
            title = report["title"]
            content = report["content"]
            language = report["language"]
            existsDuplicates = Report.query.filter_by(
                title=report["title"], user_id=current_user.id).count() > 0
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
        report = Report.query.filter_by(id=updatedReport['id']).one_or_none()
        if report is not None:
            report.title = updatedReport['title']
            report.content = updatedReport['content']
            db.session.merge(report)
            db.session.commit()
            return True
        return False

    def getAllReportsFromUser(self):
        query = Report.query.filter_by(
            user_id=current_user.id).order_by(Report.title)
        try:
            reports = query.all()
            return reports
        except NoResultFound:
            pass

    def deleteReports(self, reports):
        couldNotDelete = []
        for report in reports:
            try:
                db.session.delete(Report.query.filter_by(
                    id=report, user_id=current_user.id).one())
            except NoResultFound:
                couldNotDelete.append(report)
        db.session.commit()
        return couldNotDelete

    def getReportByTitle(self, title):
        return Report.query.filter_by(title=title, user_id=current_user.id).one_or_none()

    def getReportById(self, reportId):
        return Report.query.filter_by(id=reportId, user_id=current_user.id).one_or_none()
