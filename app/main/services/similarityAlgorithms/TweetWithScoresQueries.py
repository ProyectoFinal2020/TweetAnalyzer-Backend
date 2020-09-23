from ...entities import db
from ...entities.tweetWithScores import TweetWithScores
from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user


def getTweetsWithScoresEntityOrderedByText(per_page, page, topicTitle, reportId):
    return db.session.query(TweetWithScores) \
        .join(UserStreamingTweets) \
        .order_by(UserStreamingTweets.text) \
        .filter(TweetWithScores.user_id == current_user.id, TweetWithScores.topic_title == topicTitle,
                TweetWithScores.report_id == reportId) \
        .paginate(per_page=per_page, page=page)


def getTweetsWithScoresEntityOrderedByTextDesc(per_page, page, topicTitle, reportId):
    return db.session.query(TweetWithScores) \
        .join(UserStreamingTweets) \
        .order_by(UserStreamingTweets.text.desc()) \
        .filter(TweetWithScores.user_id == current_user.id, TweetWithScores.topic_title == topicTitle,
                TweetWithScores.report_id == reportId) \
        .paginate(per_page=per_page, page=page)


def getTweetsWithScoresEntityOrderedByProp(per_page, page, prop, topicTitle, reportId):
    return TweetWithScores.query \
        .filter_by(user_id=current_user.id, topic_title=topicTitle, report_id=reportId) \
        .order_by(getattr(TweetWithScores, prop)) \
        .paginate(per_page=per_page, page=page)


def getTweetsWithScoresEntityOrderedByPropDesc(per_page, page, prop, topicTitle, reportId):
    return TweetWithScores.query \
        .filter_by(user_id=current_user.id, topic_title=topicTitle, report_id=reportId) \
        .order_by(getattr(TweetWithScores, prop).desc()) \
        .paginate(per_page=per_page, page=page)
