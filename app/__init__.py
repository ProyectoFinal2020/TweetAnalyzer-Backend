from flask_restx import Api
from flask import Blueprint

from .main.controllers.accountController import api as account_ns
from .main.controllers.reportController import api as reports_ns
from .main.controllers.emotionAnalyzerController import api as sentAnalyzer_ns
from .main.controllers.similarityAlgorithmsController import api as simlgorithms_ns
from .main.controllers.tweetRetrievalController import api as tweetsRetrieval_ns
from .main.controllers.userInfoController import api as userInfo_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, version='1.0', title='Tweets API',
          description='Flask RestPlus powered API')

api.add_namespace(reports_ns)
api.add_namespace(account_ns)
api.add_namespace(userInfo_ns)
api.add_namespace(sentAnalyzer_ns)
api.add_namespace(simlgorithms_ns)
api.add_namespace(tweetsRetrieval_ns)
