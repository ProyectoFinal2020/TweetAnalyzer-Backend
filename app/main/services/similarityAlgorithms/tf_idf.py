from gensim.similarities import Similarity


class TfIdf:
    def __init__(self, initializer):
        preprocessed_documents = initializer.getPreprocessedDocuments()
        dictionary = initializer.getDictionary()
        corpus = [dictionary.doc2bow(text) for text in preprocessed_documents]
        tf_idf = initializer.getTfIdf()
        query_doc_tf_idf = tf_idf[dictionary.doc2bow(preprocessed_documents[0])]
        similarity_object = Similarity(
            'tfidf', tf_idf[corpus], num_features=len(dictionary))
        similarities = similarity_object[query_doc_tf_idf]
        similarity_object.destroy()
        self.scores = similarities[1:len(similarities)]

    def tfIdfSim(self, index):
        return self.scores[index]
