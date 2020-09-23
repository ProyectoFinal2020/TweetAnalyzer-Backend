from ..reportManager.reportManager import ReportUploader
from ..tweetManager.tweetManager import getTweetsByTopic


def getTweets(topicTitle):
    return getTweetsByTopic(topicTitle)


def getNews(reportId):
    reportUploader = ReportUploader()
    return reportUploader.getReportById(reportId).content
