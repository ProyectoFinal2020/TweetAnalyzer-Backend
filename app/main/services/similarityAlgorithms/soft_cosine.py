from gensim.similarities import SoftCosineSimilarity


class SoftCosine:
    def __init__(self, initializer):
        tfidf = initializer.getTfIdf()
        dictionary = initializer.getDictionary()
        query = tfidf[dictionary.doc2bow(initializer.getPreprocessedNews())]
        preprocessed_documents = initializer.getPreprocessedDocuments()
        index = SoftCosineSimilarity(
            tfidf[[dictionary.doc2bow(document)
                   for document in preprocessed_documents]],
            initializer.getSimilarityMatrix())
        similarities = index[query]
        self.scores = similarities[1:len(similarities)]

    def softcossim(self, index):
        return self.scores[index]
