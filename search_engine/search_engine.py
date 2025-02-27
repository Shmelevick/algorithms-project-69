import re
from collections import defaultdict
from itertools import chain
from math import log
from pprint import pprint


def preprocess(text):
    return re.sub(r'[^\w\s]', '', text).lower()


def search(docs: list, words: str) -> list:
    """
    Searches for words in the documents and returns their IDs,
    ranked by the total count of word occurrences in the document text.
    """

    result = []
    words = preprocess(words).split()

    for doc in docs:
        cleaned_text = preprocess(doc['text'])
        word_count = 0

        for word in words:
            word_count += cleaned_text.split().count(word)

        if word_count:
            result.append({
                'id': doc['id'],
                'word_count': word_count
            })

    result.sort(key=lambda x: x['word_count'], reverse=True)

    return [item['id'] for item in result]


def get_inverted_index(docs: list) -> dict:
    """
    Builds an inverted index from a list of documents.

    An inverted index maps each unique word found in the documents to a list of 
    document IDs where that word appears.
    """
    result = {}

    words_pit = set(chain.from_iterable(
            (preprocess(dic['text'])).split()
        for dic in docs))

    for word in words_pit:
        result[word] = search(docs, word)

    return result


def get_tf(text: str) -> dict:
    """ Compute TF """
    cleaned_text = preprocess(text).split()
    total_words = len(cleaned_text)
    tf = defaultdict(float)

    for word in cleaned_text:
        tf[word] += 1

    for word in tf:
        tf[word] /= total_words

    return tf


def get_idf(docs):
    """ Compute IDF """
    N = len(docs)
    idf = {}

    for doc in docs:
        words_in_doc = preprocess(doc['text']).split()
        for word in words_in_doc:
            q_of_docs_with_word = len(search(docs, word))
            idf[word] = log(N / (1 + q_of_docs_with_word)) + 1

    return idf


def get_tf_idf(docs):
    """ Compute TF-IDF """
    idf = get_idf(docs)
    tf_idf = {}

    for doc in docs:
        doc_id = doc['id']
        tf = get_tf(doc['text'])
        tf_idf[doc_id] = {
            word: round(tf[word] * idf[word], 4)
            for word in tf
        }

    return tf_idf


# doc1 = "I can't shoot straight unless I've had a pint!"
# doc2 = "Don't shoot shoot shoot that thing at me."
# doc3 = "I'm your shooter."

# docs = [
#     {'id': 'doc1', 'text': doc1},
#     {'id': 'doc2', 'text': doc2},
#     {'id': 'doc3', 'text': doc3},
# ]

# pprint(get_tf_idf(docs))