from flask import request
from ..repositories.unitOfWork import unitOfWork
from ..serializers.userInfoDto import UserInfoDto
from ..services.tweetService.tweetService import TweetsService
from flask_login import login_required
from flask_restplus import Resource

api = UserInfoDto.api
paginatedTweets = UserInfoDto.paginatedTweets
tweetTitle = UserInfoDto.tweetTitle
tweet = UserInfoDto.tweet
userMemorySpace = UserInfoDto.userMemorySpace

tweetsService = TweetsService()

@api.route("/info")
class TweetRetrievalController(Resource):
    @login_required
    @api.marshal_with(userMemorySpace)
    def get(self):
        """
        Gets the available space and the space used by the current user
        """
        return tweetsService.getUserMemorySpaceInformation()


@api.route("/availableSpace")
class TweetRetrievalController(Resource):
    @login_required
    def get(self):
        """
        Gets the available space of the current user
        """
        return tweetsService.getAvailableSpace()


@api.route("/tweets")
class TweetRetrievalController(Resource):
    @login_required
    @api.marshal_list_with(tweet)
    @api.doc(params={'topic_title': 'Title of the topic'})
    def get(self):
        """
        Gets all tweets belonging to a topic and the current user
        """
        topic_title = request.args.get('topic_title', "", type=str)
        return unitOfWork.userStreamingTweetsRepository.getAllByTopicTitle(topic_title)

    @login_required
    @api.response(200, 'Tweets successfully deleted.')
    @api.expect([str])
    def delete(self):
        """
        Deletes a set of tweets by id associated with the current user
        """
        tweets = request.json['tweets']
        tweetsService.deleteTweetsById(tweets)


@api.route("/tweets/topics")
class TweetTopicController(Resource):
    @login_required
    @api.marshal_list_with(tweetTitle)
    def get(self):
        """
        Gets all the topic titles belonging to the current user
        """
        return unitOfWork.getTweetsTopicRepository().getAllOrderedByTitle()

    @login_required
    @api.response(200, 'Tweets from topics successfully deleted.')
    @api.expect([str])
    @api.marshal_with(userMemorySpace)
    def delete(self):
        """
        Deletes the tweet topics belonging to the current user
        """
        topics = request.json['topics']
        tweetsService.deleteTweetsByTopicTitle(topics=topics)
        return tweetsService.getUserMemorySpaceInformation()


@api.route("/tweets/paginated")
class TweetsController(Resource):
    @login_required
    @api.marshal_with(paginatedTweets)
    @api.doc(params={'page': 'Page number', 'per_page': 'Tweets per page', 'topic_title': 'Title of the topic'})
    def get(self):
        """
        Get paginated tweets of a topic belonging to the current user
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        topic_title = request.args.get('topic_title', "", type=str)
        return unitOfWork.userStreamingTweetsRepository.getPaginatedByTopicTitle(per_page=per_page, page=page,
                                                                                 topic_title=topic_title)
