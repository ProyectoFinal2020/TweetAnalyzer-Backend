from ... import settings
from ..common.data_preprocessing import tokenizer_with_lemmatizer, preprocess
from gensim.models import KeyedVectors


class Jaccard:
    def __init__(self, initializer):
        self.initializer = initializer
        self.most_similars_precalc = dict()
        self.wv = KeyedVectors.load_word2vec_format(
            settings.GOOGLEWORD2VEC if initializer.getLanguage() == "en" else settings.SPANISHWORD2VEC, binary=True)
        self.language = initializer.getLanguage()

    def get_most_similars(self, word):
        try:
            result = [word]
            if word not in self.most_similars_precalc:
                self.most_similars_precalc[word] = self.wv.most_similar(
                    word, topn=3)
            for value in self.most_similars_precalc[word]:
                result.append(value[0])
            return result
        except KeyError:
            return [word]

    def jaccard_similarity(self, index):
        document = tokenizer_with_lemmatizer(preprocess(
            self.initializer.getKeywords()), self.language)
        tweets = self.initializer.getTweets()
        query = tokenizer_with_lemmatizer(
            preprocess(tweets[index].text), self.language)
        for word in query:
            query = query + self.get_most_similars(word)
        for word in document:
            document = document + self.get_most_similars(word)
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection) / len(union)

    def jaccardSim(self, index):
        return self.jaccard_similarity(index)
