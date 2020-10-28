from ...entities.tweetsTopic import TweetsTopic
from ...repositories.unitOfWork import unitOfWork
from flask_login import current_user

def getLanguage(topicTitle):
    tweetsTopicRepository = unitOfWork.getTweetsTopicRepository()
    tweetsTopic = tweetsTopicRepository.getByTweetTopic(topic_title=topicTitle)
    return tweetsTopic.language if tweetsTopic != None else None