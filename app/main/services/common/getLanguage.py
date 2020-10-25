from ...entities.tweetsTopic import TweetsTopic
from flask_login import current_user

def getLanguage(topicTitle):
    tweetsTopic = TweetsTopic.query.filter_by(
        topic_title=topicTitle, user_id=current_user.id).one_or_none()
    if tweetsTopic is not None:
        return tweetsTopic.language
    return None