from gensim.similarities import WmdSimilarity


class Wmd:
    def __init__(self, initializer):
        preprocessed_documents = initializer.getPreprocessedDocuments()
        index = WmdSimilarity(
            preprocessed_documents, initializer.getW2v_model())
        similarities = index[initializer.getPreprocessedNews()]
        self.scores = similarities[1:len(similarities)]

    def wmd_gensim(self, index):
        return self.scores[index]
