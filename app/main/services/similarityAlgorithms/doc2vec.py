from multiprocessing import cpu_count

from ..common.data_preprocessing import preprocess, tokenizer_with_stemmer
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


class Doc2VecN_Sim:
    def __init__(self, initializer):
        self.initializer = initializer
        self.report = tokenizer_with_stemmer(preprocess(
            initializer.getReport()), initializer.getLanguage())
        self.documents = initializer.getDocuments()
        self.processed_documents = []
        self.train_corpus = list(self.readCorpus(initializer.getLanguage()))
        self.createModel()

    def readCorpus(self, language):
        for i in range(len(self.documents)):
            tokens = tokenizer_with_stemmer(
                preprocess(self.documents[i]), language)
            self.processed_documents.append(tokens)
            yield TaggedDocument(tokens, [i])

    def createModel(self):
        self.model = Doc2Vec(dm=1, min_count=1, window=10, workers=cpu_count(),
                             vector_size=150, sample=1e-4, negative=10)
        self.model.build_vocab(self.train_corpus)
        self.model.train(self.train_corpus, total_examples=self.model.corpus_count,
                         epochs=self.model.epochs)

    def doc2VecSim(self, index):
        tweet = self.processed_documents[index + 1]
        if len(tweet) == 0:
            return 0
        else:
            return self.model.wv.n_similarity(self.report, tweet)
