import re
import string

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from spacy import load
from unidecode import unidecode

languageDict = {"en": "english", "es": "spanish"}


def clean_text(text):
    text = re.sub(r"[^A-Za-z0-9(),!.?\'\`]", " ", text)
    text = re.sub(r"\'s", " 's ", text)
    text = re.sub(r"\'ve", " 've ", text)
    text = re.sub(r"n\'t", " 't ", text)
    text = re.sub(r"\'re", " 're ", text)
    text = re.sub(r"\'d", " 'd ", text)
    text = re.sub(r"\'ll", " 'll ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ", text)
    text = re.sub(r"\(", " ( ", text)
    text = re.sub(r"\)", " ) ", text)
    text = re.sub(r"\?", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub("\'", " ", text)
    return text


def remove_links(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r'bit.ly/\S+', '', tweet)
    tweet = tweet.strip('[link]')
    return tweet


def remove_users(tweet):
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)',
                   '', tweet)  # remove tweeted at
    return tweet


def preprocess(text):
    text = remove_links(text.lower())
    text = remove_users(text)
    text = clean_text(text)
    for item in list(string.punctuation):
        text = text.replace(item, " ")
    return text


tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)


def tokenizer(text, language):
    sw = stopwords.words(languageDict[language])
    word_list = []
    for w in tknzr.tokenize(text):
        if not w in sw and not (w.isnumeric()):
            word_list.append(w)
    return word_list


def EStokenizer(text):
    return tokenizer(text, "es")


def ENtokenizer(text):
    return tokenizer(text, "en")


lemmatizer = WordNetLemmatizer()
nlp = load('es_core_news_sm')


def lemmatize(token, language):
    if language == "es":
        return nlp(token)[0].lemma_
    else:
        return lemmatizer.lemmatize(token)


def tokenizer_with_lemmatizer(text, language):
    sw = stopwords.words(languageDict[language])
    word_list = []
    for w in tknzr.tokenize(text):
        if not w in sw and not (w.isnumeric()):
            word_list.append(lemmatize(w, language))
    return word_list


def tokenizer_with_stemmer(text, language):
    stemmer = SnowballStemmer(languageDict[language])
    sw = stopwords.words(languageDict[language])
    word_list = []
    for w in tknzr.tokenize(text):
        if not w in sw and not (w.isnumeric()):
            word_list.append(stemmer.stem(w))
    if not re.search('[aeiouyAEIOUY]', ' '.join(word_list)):
        word_list = []
    return word_list


def tokenize_and_preprocess(text, language):
    text = text.lower()
    text = remove_links(text)
    text = remove_users(text)
    for item in list(string.punctuation):
        text = text.replace(item, " ")
    text_tokenized = tokenizer(text, language)
    return text_tokenized
