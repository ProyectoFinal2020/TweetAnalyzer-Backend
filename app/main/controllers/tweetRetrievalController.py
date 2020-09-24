import json
import os
from datetime import datetime

from flask import request
from ..serializers.tweetRetrievalDto import TweetRetrievalDto
from ..services.tweetManager.tweetManager import getTweetsFromAPI, getUserMemorySpaceInformation
from flask_login import login_required, current_user
from flask_restplus import Resource

api = TweetRetrievalDto.api
userMemorySpace = TweetRetrievalDto.userMemorySpace
twitterQuery = TweetRetrievalDto.twitterQuery

def _getDate(date: str):
    if date:
        return datetime.strptime(date, '%Y-%m-%d')
    else:
        return datetime.today()


@api.route("")
class TweetRetrievalController(Resource):
    @login_required
    @api.marshal_with(userMemorySpace)
    def get(self):
        """
        Gets the available space and the space used by the current user
        """
        return getUserMemorySpaceInformation()

    @login_required
    @api.expect(twitterQuery)
    def post(self):
        """
        Retrieves tweets from Twitter API.
        """
        topic_title = request.json['topic_title']
        tags = request.json['tags']
        maxAmount = request.json['maxAmount']
        since = _getDate(request.json['since'])
        until = _getDate(request.json['until'])
        language = request.json['language'] if request.json['language'] else "en"

        tweets_dict = getTweetsFromAPI(topic_title=topic_title, search_tags=tags, maxAmount=maxAmount,
                                       since=since, until=until, language=language) 
        return tweets_dict
