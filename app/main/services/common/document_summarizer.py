from gensim.summarization import keywords


def getKeywords(document):
    kw = keywords(document, split=True, scores=True,
                  lemmatize=True, deacc=True)
    keywords_list = []
    for keyword in kw:
        keywords_list.append((keyword[0]))
    return ' '.join(keywords_list) if len(keywords_list) is not 0 else document
