from ...entities import db
from ...entities.tweetWithScores import TweetWithScores as TweetWithScoresEntity
from ...models.TweetWithScores import TweetWithScores
from ..common.initializer import Initializer
from .bag_of_words import BagOfWords
from .doc2vec import Doc2VecN_Sim
from .doc2vec_gensim import Doc2VecGensim
from .jaccard import Jaccard
from .soft_cosine import SoftCosine
from .tf_idf import TfIdf
from .wmd import Wmd
from .word2vec_gensim import Word2VecGensim
from flask_login import current_user

from ...repositories.unitOfWork import unitOfWork


class SimilarityAlgorithms:
    def __init__(self):
        self.algorithm_names = self.initializeDictionary()
        self.tweetWithScoresRepository = unitOfWork.getTweetWithScoresRepository()

    def initializeDictionary(self):
        return {
            "bagOfWords": {"algorithm": self.bag_of_words, "initializer": self.bag_of_words_initializer},
            "doc2vecGensim": {"algorithm": self.doc2vec_gensim, "initializer": self.doc2vec_gensim_initializer},
            "doc2vecNSim": {"algorithm": self.doc2vec_n_sim, "initializer": self.doc2vec_n_sim_initializer},
            "softCosine": {"algorithm": self.soft_cosine, "initializer": self.soft_cosine_initializer},
            "tfIdfSim": {"algorithm": self.tf_idf_sim, "initializer": self.tf_idf_sim_initializer},
            "word2vecGensim": {"algorithm": self.word2vec_gensim, "initializer": self.word2vec_gensim_initializer},
            "wmd": {"algorithm": self.wmd, "initializer": self.wmd_initializer},
            "jaccard": {"algorithm": self.jaccard, "initializer": self.jaccard_initializer}
        }

    def execute_algorithms(self, reportId, topicTitle, algorithms, language):
        initializer = Initializer(
            reportId=reportId, topicTitle=topicTitle, language=language)
        tweets = initializer.getTweets()
        for algorithm in algorithms:
            self.algorithm_names[algorithm]["initializer"](
                initializer=initializer)
        for index in range(len(tweets)):
            tweetWithScores = TweetWithScoresEntity(id=tweets[index].id, user_id=current_user.id,
                                                    topic_title=topicTitle, report_id=reportId)
            for algorithm in algorithms:
                score = self.algorithm_names[algorithm]["algorithm"](index)
                setattr(tweetWithScores, algorithm, float(score))
            db.session.merge(tweetWithScores)
        db.session.commit()

    def _getTweetsWithScoresEntity(self, per_page, page, orderBy, desc, topicTitle, reportId):
        if orderBy == 'Tweet':
            return self.tweetWithScoresRepository.getTweetsWithScoresOrderedByText(topicTitle, reportId, desc, per_page, page)
        else:
            return self.tweetWithScoresRepository.getTweetsWithScoresOrderedByProp(topicTitle, reportId, orderBy, desc, per_page, page)

    def _createScoresObject(self, tweetsWithScoresEntity, algorithms):
        tweetsWithScores = []
        for item in tweetsWithScoresEntity:
            scores = dict()
            for algorithm in self.algorithm_names:
                if algorithm in algorithms:
                    scores[algorithm] = getattr(item, algorithm)
            tweetWithScore = TweetWithScores(
                tweet=item.userStreamingTweets, scores=scores)
            tweetsWithScores.append(tweetWithScore)
        return tweetsWithScores

    def get_tweets_with_scores(self, per_page, page, orderBy, desc, topicTitle, reportId, algorithms):
        tweetsWithScoresEntity = self._getTweetsWithScoresEntity(
            per_page, page, orderBy, desc, topicTitle, reportId)
        tweetsWithScoresEntity.items = self._createScoresObject(
            tweetsWithScoresEntity.items, algorithms)
        return tweetsWithScoresEntity

    def get_tweets_to_download(self, topicTitle, reportId, algorithms):
        tweetsWithScoresEntity = self.tweetWithScoresRepository.getAllTweetsWithScores(topicTitle, reportId)
        return self._createScoresObject(tweetsWithScoresEntity, algorithms)

    def bag_of_words_initializer(self, initializer):
        self.bagOfWords = BagOfWords(initializer)

    def bag_of_words(self, index):
        return self.bagOfWords.bagOfWordSim(index)

    def doc2vec_gensim_initializer(self, initializer):
        self.doc2vecGensim = Doc2VecGensim(initializer)

    def doc2vec_gensim(self, index):
        return self.doc2vecGensim.doc2VecSim(index)

    def doc2vec_n_sim_initializer(self, initializer):
        self.doc2VecNSim = Doc2VecN_Sim(initializer)

    def doc2vec_n_sim(self, index):
        return self.doc2VecNSim.doc2VecSim(index)

    def soft_cosine_initializer(self, initializer):
        self.softCosine = SoftCosine(initializer)

    def soft_cosine(self, index):
        return self.softCosine.softcossim(index)

    def tf_idf_sim_initializer(self, initializer):
        self.tfIdfSim = TfIdf(initializer)

    def tf_idf_sim(self, index):
        return self.tfIdfSim.tfIdfSim(index)

    def word2vec_gensim_initializer(self, initializer):
        self.word2VecGensim = Word2VecGensim(initializer)

    def word2vec_gensim(self, index):
        return self.word2VecGensim.word2VecSim(index)

    def wmd_initializer(self, initializer):
        self.wmd = Wmd(initializer)

    def wmd(self, index):
        return self.wmd.wmd_gensim(index)

    def jaccard_initializer(self, initializer):
        self.jaccard = Jaccard(initializer)

    def jaccard(self, index):
        return self.jaccard.jaccardSim(index)
