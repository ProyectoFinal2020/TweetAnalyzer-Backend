from ..reportManager.reportManager import ReportUploader

def getNews(reportId):
    reportUploader = ReportUploader()
    return reportUploader.getReportById(reportId).content
