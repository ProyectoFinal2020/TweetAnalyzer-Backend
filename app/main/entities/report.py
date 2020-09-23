from . import db
from .user import User


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(30))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    language = db.Column(db.String(2))
