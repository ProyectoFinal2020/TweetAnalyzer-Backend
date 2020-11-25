from flask import request
from ..serializers.similarityAlgorithmsDto import SimilarityAlgorithmsDto
from ..services.similarityAlgorithms.similarityAlgorithms import SimilarityAlgorithms
from flask_login import login_required
from werkzeug.exceptions import BadRequest
from flask_restx import Resource

api = SimilarityAlgorithmsDto.api
similarityAlgorithms = SimilarityAlgorithmsDto.similarityAlgorithms
paginatedTweetWithScores = SimilarityAlgorithmsDto.paginatedTweetWithScores
tweetWithScores = SimilarityAlgorithmsDto.tweetWithScores


@api.route("")
class SimilarityAlgorithmsController(Resource):
    @login_required
    @api.marshal_with(paginatedTweetWithScores)
    @api.doc(params={'page': 'Page number', 'per_page': 'Tweets per page',
                     'orderBy': 'Prop to order by', 'desc': 'Descending order',
                     'topicTitle': 'Topic Title', 'reportId': 'Report id',
                     'algorithms': 'Algorithms'})
    def get(self):
        """
        Returns a page of tweets with scores
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        orderBy = request.args.get('orderBy', "", type=str)
        desc = request.args.get('desc', "False", type=str)
        topicTitle = request.args.get('topicTitle', "", type=str)
        reportId = request.args.get('reportId', "", type=int)
        algorithms = request.args.get('algorithms', "", type=str)
        algorithms = algorithms.split(',')
        if orderBy != "Tweet" and not orderBy in algorithms:
            raise BadRequest("La propiedad para ordenar no es correcta.")
        similarityAlgorithms = SimilarityAlgorithms()
        return similarityAlgorithms \
            .get_tweets_with_scores(per_page=per_page, page=page, orderBy=orderBy,
                                    desc=True if desc == "true" or desc == "True" else False, topicTitle=topicTitle,
                                    reportId=reportId, algorithms=algorithms)

    @login_required
    @api.expect(similarityAlgorithms)
    def post(self):
        """
        Calculates the similarity between tweets of a topic and a report using various algorithms
        """
        reportId = request.json['reportId']
        topicTitle = request.json['topicTitle']
        algorithms = request.json['algorithms']
        language = request.json['language']
        similarityAlgorithms = SimilarityAlgorithms()
        similarityAlgorithms.execute_algorithms(reportId=reportId, topicTitle=topicTitle, algorithms=algorithms,
                                                language=language)


@api.route("/download")
class SimilarityAlgorithmsDownloadController(Resource):
    @login_required
    @api.marshal_with(tweetWithScores)
    @api.doc(params={'topicTitle': 'Topic Title', 'reportId': 'Report Id',
                     'algorithms': 'Algorithms'})
    def get(self):
        """
        Returns all tweets with scores calculated from a report, algorithms and tweets
        """
        topicTitle = request.args.get('topicTitle', "", type=str)
        reportId = request.args.get('reportId', "", type=int)
        algorithms = request.args.get('algorithms', "", type=str)
        algorithms = algorithms.split(',')
        similarityAlgorithms = SimilarityAlgorithms()
        return similarityAlgorithms \
            .get_tweets_to_download(topicTitle=topicTitle, reportId=reportId, algorithms=algorithms)
