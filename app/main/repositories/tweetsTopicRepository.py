from ..entities.tweetsTopic import TweetsTopic
from .baseRepository import BaseRepository
from flask_login import current_user


class TweetsTopicRepository(BaseRepository[TweetsTopic]):
    def __init__(self):
        super().__init__(TweetsTopic)

    