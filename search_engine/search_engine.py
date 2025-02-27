import re
from collections import defaultdict
from itertools import chain


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


def get_tf(doc: list, all_terms:dict = None):
    """ Compute TF """
    cleaned_text = preprocess(doc['text'])
    unique_terms = cleaned_text.split()

    for word in unique_terms:
        all_terms[word]['quant_in_doc'] += cleaned_text.split().count(word)
    
    return all_terms


def get_tf_idf(docs):
    """ Compute TF-IDF """
    N

    for doc in docs:
        unique_words_in_doc = set(preprocess(doc['text']).split())
        for word in unique_words_in_doc:

        pass


doc1 = "I can't shoot straight unless I've had a pint!"
doc2 = "Don't shoot shoot shoot that thing at me."
doc3 = "I'm your shooter."

docs = [
    {'id': 'doc1', 'text': doc1},
    {'id': 'doc2', 'text': doc2},
    {'id': 'doc3', 'text': doc3},
]

print(get_tf_idf(docs))