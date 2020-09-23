from ...models.document_type import DocumentType
from ..common.data_preprocessing import ENtokenizer, EStokenizer, preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class BagOfWords:
    def __init__(self, initializer):
        self.vectorizer = CountVectorizer(analyzer="word", strip_accents='unicode', lowercase=True,
                                          tokenizer=ENtokenizer if initializer.getLanguage() == "en" else EStokenizer,
                                          preprocessor=preprocess, stop_words=None,
                                          max_features=5000)
        documents = initializer.getDocuments(document_type=DocumentType.TWEETS)
        news_keywords = initializer.getKeywords()
        self.vectorizer.fit_transform([news_keywords] + documents)
        self.document_array = self.vectorizer.transform(
            [news_keywords]).toarray()
        self.tweets = initializer.getTweets()

    def bagOfWordSim(self, index):
        tweet_array = self.vectorizer.transform(
            [self.tweets[index].text]).toarray()
        return cosine_similarity(self.document_array, tweet_array)
