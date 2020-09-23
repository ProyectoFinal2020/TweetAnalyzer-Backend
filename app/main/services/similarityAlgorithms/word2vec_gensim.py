from ... import settings
from gensim.models import KeyedVectors


class Word2VecGensim:
    def __init__(self, initializer):
        self.model = KeyedVectors.load_word2vec_format(
            settings.GOOGLEWORD2VEC if initializer.getLanguage() == "en" else settings.SPANISHWORD2VEC, binary=True)
        preprocessed_documents = initializer.getPreprocessedDocuments()
        self.tokenized_documents = []
        for i in range(len(preprocessed_documents)):
            words = list(
                filter(lambda x: x in self.model.vocab, preprocessed_documents[i]))
            self.tokenized_documents.append(words)
        if not self.tokenized_documents[0]:
            self.tokenized_documents[0] = preprocessed_documents[0]

    def word2VecSim(self, index):
        if len(self.tokenized_documents[index]) > 0:
            try:
                return self.model.n_similarity(self.tokenized_documents[0], self.tokenized_documents[index])
            except KeyError:
                return 0
        return 0
