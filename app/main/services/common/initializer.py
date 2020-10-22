from multiprocessing import cpu_count
from typing import List

import gensim.downloader as api
import os
from ...models.document_type import DocumentType
from .data_fetching import getNews
from .data_preprocessing import tokenize_and_preprocess
from .document_summarizer import getKeywords
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import Word2Vec, KeyedVectors
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from ...repositories.unitOfWork import unitOfWork


class Initializer:
    def __init__(self, reportId, topicTitle, language):
        self.language = language
        self.report = getNews(reportId)
        self.tweets = unitOfWork.userStreamingTweetsRepository.getByTopicTitle(topicTitle)
        self.initializeAndPreprocessDocuments(language)
        self.initializeDictionary()
        self.initializeTfIdf()
        self.initializeModel()
        self.initializeSimilarityMatrix()
        self.initializePreprocessedNews()
        self.initializeKeywords()

    def initializeAndPreprocessDocuments(self, language):
        self.documents = [tweet.text for tweet in self.tweets]
        self.documents = [self.report] + self.documents
        self.preprocessed_documents = [
            tokenize_and_preprocess(doc, language) for doc in self.documents]

    def initializeDictionary(self):
        self.dictionary = corpora.Dictionary(self.preprocessed_documents)

    def initializeTfIdf(self):
        self.tfidf = TfidfModel(dictionary=self.dictionary)

    def initializeModel(self):
        if self.language == "en":
            self.w2v_model = api.load("glove-wiki-gigaword-50")
        else:
            self.w2v_model = KeyedVectors.load_word2vec_format(
                    os.getenv('SPANISHWORD2VEC'), binary=True)
                    
    def initializeSimilarityMatrix(self):
        self.similarity_index = WordEmbeddingSimilarityIndex(self.w2v_model)
        self.similarity_matrix = SparseTermSimilarityMatrix(
            self.similarity_index, self.dictionary, self.tfidf, nonzero_limit=100)

    def initializePreprocessedNews(self):
        self.preprocessed_news = self.preprocessed_documents[0]

    def initializeKeywords(self):
        self.keywords = getKeywords(self.report)

    def __getDocsByType(self, documents, document_type):
        toReturn: List[str] = []
        if document_type == DocumentType.TWEETANDNEWS:
            toReturn = documents
        elif document_type == DocumentType.TWEETS:
            toReturn = documents[1:len(documents)]
        return toReturn

    def getTweets(self):
        return self.tweets

    def getDocuments(self, document_type=DocumentType.TWEETANDNEWS):
        return self.__getDocsByType(self.documents, document_type)

    def getPreprocessedDocuments(self, document_type=DocumentType.TWEETANDNEWS):
        return self.__getDocsByType(self.preprocessed_documents, document_type)

    def getDictionary(self):
        return self.dictionary

    def getTfIdf(self):
        return self.tfidf

    def getW2v_model(self):
        return self.w2v_model

    def getSimilarityMatrix(self):
        return self.similarity_matrix

    def getPreprocessedNews(self):
        return self.preprocessed_news

    def getKeywords(self):
        return self.keywords

    def getReport(self):
        return self.report

    def getLanguage(self):
        return self.language
