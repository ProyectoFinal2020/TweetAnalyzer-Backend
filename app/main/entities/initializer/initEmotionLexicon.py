import pandas
import os

from .. import db
from ..emotionLexicon import EmotionLexicon


def initializeEmotionLexiconTable():
    if(not os.getenv('ENV') and EmotionLexicon.query.count() == 0):
        excel_data_df = pandas.read_excel(
            'app/main/utils/nrc_emotion_lexicon.xlsx', sheet_name='NRC-Lex-v0.92-word-translations')

        lexicon = []
        for index, row in excel_data_df.iterrows():
            emotionLexicon = EmotionLexicon(
                english=str(row['English (en)']),
                spanish=str(row['Spanish (es)']),
                positive=bool(row['Positive']),
                negative=bool(row['Negative']),
                anger=bool(row['Anger']),
                anticipation=bool(row['Anticipation']),
                disgust=bool(row['Disgust']),
                fear=bool(row['Fear']),
                joy=bool(row['Joy']),
                sadness=bool(row['Sadness']),
                surprise=bool(row['Surprise']),
                trust=bool(row['Trust']),
            )
            lexicon.append(emotionLexicon)

            if(lexicon.count == 1000):
                db.session.add_all(lexicon)
                db.session.commit()
                lexicon = []

        db.session.add_all(lexicon)
        db.session.commit()
