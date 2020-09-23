from . import db


class EmotionLexicon(db.Model):
    __tablename__ = "emotion_lexicon"
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(50))
    spanish = db.Column(db.String(30))
    positive = db.Column(db.Boolean)
    negative = db.Column(db.Boolean)
    anger = db.Column(db.Boolean)
    anticipation = db.Column(db.Boolean)
    disgust = db.Column(db.Boolean)
    fear = db.Column(db.Boolean)
    joy = db.Column(db.Boolean)
    sadness = db.Column(db.Boolean)
    surprise = db.Column(db.Boolean)
    trust = db.Column(db.Boolean)
