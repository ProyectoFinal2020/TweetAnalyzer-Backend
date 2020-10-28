from ..entities.report import Report
from .baseRepository import BaseRepository
from flask_login import current_user


class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def getByTitle(self, title):
        return Report.query.filter_by(title=title, user_id=current_user.id).one_or_none()

    def getAllOrderedByTitle(self):
        return self.model.query.filter_by(user_id=current_user.id).order_by(Report.title).all()