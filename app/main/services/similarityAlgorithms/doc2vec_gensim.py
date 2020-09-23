from multiprocessing import cpu_count

from gensim.models.doc2vec import Doc2Vec, TaggedDocument


class Doc2VecGensim:
    def __init__(self, initializer):
        self.documents = initializer.getDocuments()
        train_corpus = list(self.readCorpus(initializer))
        model = self.createModel(train_corpus)
        self.createSimsArray(initializer, model)

    def readCorpus(self, initializer):
        preprocessed_documents = initializer.getPreprocessedDocuments()
        for i in range(len(preprocessed_documents)):
            yield TaggedDocument(preprocessed_documents[i], [i])

    def createModel(self, train_corpus):
        model = Doc2Vec(epochs=40, min_count=2, workers=cpu_count())
        model.build_vocab(train_corpus)
        model.train(train_corpus, total_examples=model.corpus_count,
                    epochs=model.epochs)
        return model

    def createSimsArray(self, initializer, model):
        inferred_vector = model.infer_vector(initializer.getPreprocessedNews())
        self.sims = model.docvecs.most_similar(
            [inferred_vector], topn=len(model.docvecs))

    def doc2VecSim(self, index):
        return self.sims[index][1]
